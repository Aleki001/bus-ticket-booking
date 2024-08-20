# forms.py
from django import forms
from .models import Route, Bus, CustomUser
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User

class BusSearchForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['route', 'travel_date']
        
class BusSeatSelectionForm(forms.Form):
    bus = forms.ModelChoiceField(queryset=Bus.objects.none(), empty_label="Select a bus")

    def __init__(self, *args, **kwargs):
        route = kwargs.pop('route', None)
        travel_date = kwargs.pop('travel_date', None)
        super().__init__(*args, **kwargs)
        if route and travel_date:
            self.fields['bus'].queryset = Bus.objects.filter(route=route, travel_date=travel_date, available_seats__gt=0)

class CustomerInfoForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    id_number = forms.CharField(max_length=20, label="ID Number")


class RoutesForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['starting_point', 'destination', 'price']
        widgets = {
            'starting_point': forms.TextInput(attrs={'class': 'form-control'}),
            'destination': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class BusForm(forms.ModelForm):
    STATUS_CHOICES = [
        ('AVAILABLE', 'AVAILABLE'),
        ('BOOKED', 'BOOKED'),
    ]

    status = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    route = forms.ModelChoiceField(queryset=Route.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    travel_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

    class Meta:
        model = Bus
        fields = ['number_plate', 'available_seats', 'status', 'route', 'travel_date']
        widgets = {
            'number_plate': forms.TextInput(attrs={'class': 'form-control'}),
            'available_seats': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_pic', 'phone_no']


class CustomUserChangeForm(UserChangeForm):
    profile_pic = forms.ImageField(required=False)
    phone_no = forms.CharField(required=False) 
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_pic', 'phone_no']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['phone_no'].initial = self.instance.userprofile.phone_no

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.userprofile.phone_no = self.cleaned_data['phone_no']
            user.userprofile.save()
        return user





class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
