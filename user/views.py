from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile
from .forms import CustomUserChangeForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from busapp.models import Booking, Bus
from django.contrib.auth.models import User
from django.db.models.functions import TruncWeek
from django.db import models




def register_user(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created. You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/register.html', {'form':form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                return redirect('admin_account')
            else:
                login(request, user)
                return redirect('user_account')
        else:
            return render(request, 'user/login.html', {'error': 'Invalid credentials!! Try again.'})
    else:
        return render(request, 'user/login.html')
 

@login_required
def custom_logout(request):
    logout(request)
    return redirect("login")



@login_required
def user_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Updating the session with the new password hash
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('user_account')
        else:
            return render(request, 'busapp/user/change_password.html', {'form': form})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'busapp/user/change_password.html', {'form': form})


@login_required
def admin_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # Updating the session with the new password hash
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('admin_account')
        else:
            return render(request, 'busapp/admin/change_password.html', {'form': form})
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'busapp/admin/change_password.html', {'form': form})


@login_required
def admin_profile(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            profile_pic = form.cleaned_data.get('profile_pic')
            if profile_pic:
                profile.profile_pic = profile_pic
                profile.save()
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('admin_profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'busapp/admin/admin_profile.html', {'form': form, 'profile': profile})



@login_required
def user_account(request):
    user = request.user
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)

    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            profile_pic = form.cleaned_data.get('profile_pic')
            if profile_pic:
                profile.profile_pic = profile_pic
                profile.save()
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('user_account')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'busapp/user/account.html', {'form': form, 'profile': profile})


@login_required
def admin_account(request):
    recent_bookings = Booking.objects.order_by('-booking_date')[:5]
    recent_users = User.objects.all().order_by('date_joined')[:5]
    total_bookings = Booking.objects.all().count()
    total_users = User.objects.all().count()

    # Data for Bookings Over Time (Weekly Line Chart)
    bookings_over_time = (
        Booking.objects.annotate(week=TruncWeek('booking_date'))
        .values('week')
        .annotate(count=models.Count('id'))
        .order_by('week')
    )
    weeks = [booking['week'].strftime("%U %Y") for booking in bookings_over_time]
    booking_counts = [booking['count'] for booking in bookings_over_time]

    # Data for Buses Overview (Pie Chart)
    bus_statuses = Bus.objects.values('status').annotate(count=models.Count('id'))
    status_labels = [bus['status'] for bus in bus_statuses]
    status_counts = [bus['count'] for bus in bus_statuses]

    # Pie chart colors
    pie_colors = ["#4caf50", "#ff9800", "#f44336"]  # Green, Orange, Red for better distinction

    context = {
        'bookings': recent_bookings,
        'total_bookings': total_bookings,
        'total_users': total_users,
        'recent_users': recent_users,
        'weeks': weeks,
        'booking_counts': booking_counts,
        'status_labels': status_labels,
        'status_counts': status_counts,
        'pie_colors': pie_colors,
    }
    
    return render(request, 'busapp/admin/account.html', context)