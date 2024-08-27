from django.db import models
from django.utils import timezone


class Route(models.Model):
    starting_point = models.CharField(max_length=50)
    destination = models.CharField(max_length=50)
    price = models.BigIntegerField(default=0)
    
    def __str__(self):
        return self.starting_point + " - " + self.destination


class Bus(models.Model):
    number_plate = models.CharField(max_length=50)
    available_seats = models.IntegerField()
    status = models.CharField(max_length=30, default="AVAILABLE")
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='buses', default=1)
    travel_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.number_plate
    
    def remaining_seats(self):
        return self.available_seats  # Return the number of available seats
    
    
    
class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, default=True)
    customer_name = models.CharField(max_length=100, default="user")
    customer_email = models.EmailField(null=True)
    customer_phone = models.CharField(max_length=10, default=0)
    customer_id_number = models.CharField(max_length=20, default=1)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    checkout_request_id = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.customer_name} - {self.bus} - Travel date {self.bus.travel_date}"



class Payment(models.Model):
    merchant_request_id = models.CharField(max_length=100, unique=True, null=True)
    checkout_request_id = models.CharField(max_length=100, unique=True, null=True)
    result_code = models.IntegerField(null=True, default=0)
    result_description = models.CharField(max_length=255, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    mpesa_receipt_number = models.CharField(max_length=100, null=True)
    balance = models.CharField(max_length=100, null=True, blank=True)  # Balance might not always be provided
    transaction_date = models.DateTimeField(null=True)  # Defaulting to null for better handling of empty dates
    phone_number = models.CharField(max_length=15, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.mpesa_receipt_number} - {self.amount} - {self.transaction_date}'

    def save(self, *args, **kwargs):
        # Ensure transaction_date is not set to a default invalid value
        if isinstance(self.transaction_date, int) and self.transaction_date == 0:
            self.transaction_date = None
        super(Payment, self).save(*args, **kwargs)


