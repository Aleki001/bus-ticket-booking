from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, Group, Permission




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
    customer_name = models.CharField(max_length=100, default="user")
    customer_email = models.EmailField(null=True)
    customer_phone = models.CharField(max_length=10, default=0)
    customer_id_number = models.CharField(max_length=20, default=1)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer_name} - {self.bus} - Travel date {self.bus.travel_date}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    instance.userprofile.save()

class CustomUser(AbstractUser):
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    groups = models.ManyToManyField(
        Group,
        related_name='customuser_set',  # Change the related_name to avoid conflict
        blank=True,
        help_text=('The groups this user belongs to. A user will get all permissions '
                   'granted to each of their groups.'),
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',  # Change the related_name to avoid conflict
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='customuser',
    )
