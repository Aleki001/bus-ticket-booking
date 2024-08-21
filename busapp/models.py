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
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE, default=True)
    customer_name = models.CharField(max_length=100, default="user")
    customer_email = models.EmailField(null=True)
    customer_phone = models.CharField(max_length=10, default=0)
    customer_id_number = models.CharField(max_length=20, default=1)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.bus} - Travel date {self.bus.travel_date}"





