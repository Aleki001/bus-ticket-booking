from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db import transaction
from .models import Bus, Booking, Route, Payment
from .forms import CustomerInfoForm, BusSearchForm, RoutesForm, BusForm
from django.urls import reverse
from urllib.parse import urlencode
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django_daraja.mpesa.core import MpesaClient
from django.views.decorators.csrf import csrf_exempt
import datetime
import json

from django.db import IntegrityError



def bus_search(request):
    route_id = request.GET.get('route')
    travel_date = request.GET.get('travel_date')

    # Get the Route object using the route_id
    route = get_object_or_404(Route, id=route_id)
    request.session['route_id'] = route_id

    # Filter buses by route and travel date
    buses = Bus.objects.filter(route=route, travel_date=travel_date, status="AVAILABLE")

    if request.method == "POST":
        request.session['bus_id'] = request.POST.get('bus_id')
        bus_id = request.session.get('bus_id')
        bus = get_object_or_404(Bus, id=bus_id)
        if bus.status == "AVAILABLE":
            return redirect('customer_info')
        else:
            messages.error(request, 'Sorry, this bus is now full. Please choose another.')
    else:
        return render(request, "busapp/bus_search_results.html", {
            'buses': buses,
            'route': route,  # Pass the entire route object
            'travel_date': travel_date
        })



def index(request):
    form = BusSearchForm()

    if request.method == 'POST':
        form = BusSearchForm(request.POST)
        if form.is_valid():
            route = form.cleaned_data['route'].id  # Assuming route is a ForeignKey
            travel_date = form.cleaned_data['travel_date'].strftime('%Y-%m-%d')  # Format the date

            # Use urlencode to generate the query string
            query_string = urlencode({'route': route, 'travel_date': travel_date})
            url = f"{reverse('bus_search')}?{query_string}"
            return redirect(url)

    return render(request, 'busapp/index.html', {'form': form})


def customer_info(request):
    user = request.user

    if user.is_authenticated:
        # Get data from the user's profile
        profile = user.userprofile
        customer_data = {
            'full_name': user.get_full_name(),
            'email': user.email,
            'phone_number': profile.phone_no,
            'id_number': profile.id_number  
        }
        return create_booking(request, customer_data)
    
    # If the user is not authenticated or their profile lacks necessary info, show the form
    if request.method == 'POST':
        form = CustomerInfoForm(request.POST)
        if form.is_valid():
            return create_booking(request, form.cleaned_data)
    else:
        form = CustomerInfoForm()

    return render(request, 'busapp/booking/customer_info.html', {'form': form})

@transaction.atomic
def create_booking(request, customer_data):
    bus_id = request.session.get('bus_id')
    if not bus_id:
        messages.error(request, 'Bus selection is missing. Please select a bus first.')
        return redirect('index')

    route_id = request.session.get('route_id')
    route = get_object_or_404(Route, id=route_id)

    bus = get_object_or_404(Bus, id=bus_id)

    if bus.available_seats <= 0:
        messages.error(request, 'Sorry, the bus is fully booked.')
        return redirect('route_selection')

    try:
        booking = Booking.objects.create(
            bus=bus,
            route=route,
            customer_name=customer_data.get('full_name'),
            customer_email=customer_data.get('email'),
            customer_phone=customer_data.get('phone_number'),
            customer_id_number=customer_data.get('id_number'),
            status='Pending'  # Set initial status as 'Pending'
        )

        # Store booking_id and other necessary information in the session
        request.session['booking_id'] = booking.id
        request.session['price'] = bus.route.price
        request.session['phone_no'] = customer_data.get('phone_number')

        return redirect('booking_confirmation', booking_id=booking.id)

    except IntegrityError as e:
        messages.error(request, 'Please complete your profile with all required information.')
        return redirect('user_account')

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'busapp/booking/booking_confirmation.html', {'booking': booking})




@csrf_exempt
def pay(request):
    if request.method == 'POST':
        phone_no = request.session.get('phone_no')
        amount = request.session.get('price')

        # Retrieve the booking using the session's stored booking_id
        booking_id = request.session.get('booking_id')
        if not booking_id:
            messages.error(request, "Booking ID is missing. Please start the booking process again.")
            return redirect('index')

        booking = get_object_or_404(Booking, id=booking_id)

        cl = MpesaClient()

        phone_number = phone_no
        account_reference = 'reference'
        transaction_desc = 'Description'
        callback_url = 'https://api.darajambili.com/express-payment'

        try:
            response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
            data = response.json()

            # Accessing response attributes correctly
            if data['ResponseCode'] == '0':
                # Store checkout_request_id in the booking
                checkout_request_id = data['CheckoutRequestID']
                booking.checkout_request_id = checkout_request_id
                booking.save()

                messages.success(request, "An STK Push was sent to your phone, confirm to complete the payment. Thank you :)")
            else:
                messages.error(request, f"Payment failed: {data['ResponseDescription']}")
                booking.status = 'Cancelled'
                booking.save()
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            booking.status = 'Cancelled'
            booking.save()

        # Update bus availability
        bus = booking.bus
        bus.available_seats -= 1
        if bus.available_seats == 0:
            bus.status = 'BOOKED'
        bus.save()

        return redirect('index')
    else:
        amount = request.session.get('price')
        return render(request, 'busapp/booking/payment.html', {'price': amount})


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        
        # Load the JSON data from the request
        result_json = json.loads(request.body.decode('utf-8'))
        
        # Extract the necessary fields from the callback
        stk_callback = result_json.get('Body', {}).get('stkCallback', {})
        result_code = stk_callback.get('ResultCode')
        result_desc = stk_callback.get('ResultDesc')
        merchant_request_id = stk_callback.get('MerchantRequestID')
        checkout_request_id = stk_callback.get('CheckoutRequestID')
        
        # Initialize variables
        amount = None
        mpesa_receipt_number = None
        balance = None
        transaction_date = None
        phone_number = None
        
        # Extract CallbackMetadata Items
        callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
        for item in callback_metadata:
            if item['Name'] == 'Amount':
                amount = item['Value']
            elif item['Name'] == 'MpesaReceiptNumber':
                mpesa_receipt_number = item['Value']
            elif item['Name'] == 'Balance':
                balance = item.get('Value', None)
            elif item['Name'] == 'TransactionDate':
                transaction_date = datetime.strptime(str(item['Value']), "%Y%m%d%H%M%S")
            elif item['Name'] == 'PhoneNumber':
                phone_number = item['Value']
        
        # Save the data to the database
        payment = Payment.objects.create(
            merchant_request_id=merchant_request_id,
            checkout_request_id=checkout_request_id,
            result_code=result_code,
            result_description=result_desc,
            amount=amount,
            mpesa_receipt_number=mpesa_receipt_number,
            balance=balance,
            transaction_date=transaction_date,
            phone_number=phone_number
        )

        # Prepare the JSON response
        response_data = {
            "ResultCode": "0",
            "ResultDesc": "Success"
        }
        response_json = json.dumps(response_data)

        # Return the JSON response
        return HttpResponse(response_json, content_type='application/json')

    return HttpResponse('Method is not allowed', status=405)



@login_required
def routes(request):
    if request.method == "POST":
        form = RoutesForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('routes')
    else:
        form = RoutesForm()
    routes = Route.objects.all()
    return render(request, "busapp/admin/routes.html", {'routes':routes, 'form':form})

@login_required
def edit_route(request, route_id):
    route = get_object_or_404(Route, id=route_id)
    
    if request.method == "POST":
        form = RoutesForm(request.POST, instance=route)
        if form.is_valid():
            form.save()
            return redirect('routes')
    else:
        form = RoutesForm(instance=route)
    
    return render(request, 'busapp/admin/routes.html', {'form': form})

@login_required
def delete_route(request, pk):
    route = get_object_or_404(Route, pk=pk)
    route.delete()
    return redirect('routes')


@login_required
def list_buses(request):
    if request.method == "POST":
        form = BusForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('list_buses')
    else:
        form = BusForm()
    buses = Bus.objects.all()
    return render(request, 'busapp/admin/businfo.html', {'buses': buses, 'form':form})

@login_required
def edit_bus(request, bus_id):
    bus = get_object_or_404(Bus, id=bus_id)
    
    if request.method == "POST":
        form = BusForm(request.POST, instance=bus)
        if form.is_valid():
            form.save()
            return redirect('list_buses')  # Redirect to the bus list view
    else:
        form = BusForm(instance=bus)
    
    return render(request, 'busapp/admin/businfo.html', {'form': form})

@login_required
def delete_bus(request, pk):
    bus = get_object_or_404(Bus, pk=pk)
    bus.delete()
    return redirect('list_buses')



@login_required
def all_bookings(request):
    # Get all bookings 
    bookings = Booking.objects.all()
    # Get popular routes
    popular_routes = Booking.objects.values('route__starting_point', 'route__destination').annotate(count=Count('id')).order_by('-count')

    # Get peak days
    peak_days = Booking.objects.annotate(day=ExtractWeekDay('booking_date')).values('day').annotate(count=Count('id')).order_by('-count')

    # Get peak months
    peak_months = Booking.objects.annotate(month=ExtractMonth('booking_date')).values('month').annotate(count=Count('id')).order_by('-count')

    context = {
        'popular_routes': list(popular_routes),
        'peak_days': list(peak_days),
        'peak_months': list(peak_months),
        'bookings': bookings
    }
    return render(request, "busapp/admin/bookings.html",  context)


@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(customer_email=request.user.email)
    return render(request, "busapp/user/user_bookings.html", {'bookings': bookings})



from django.db.models import Count
from django.db.models.functions import ExtractHour, ExtractWeekDay, ExtractMonth

