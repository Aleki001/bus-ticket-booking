from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth.models import User



class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_pic', 'phone_no', 'id_number']


class CustomUserChangeForm(UserChangeForm):
    profile_pic = forms.ImageField(required=False)
    phone_no = forms.CharField(required=False) 
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'profile_pic', 'phone_no', 'id_number']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance:
            self.fields['phone_no'].initial = self.instance.userprofile.phone_no
            self.fields['id_number'].initial = self.instance.userprofile.id_number

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user.userprofile.phone_no = self.cleaned_data['phone_no']
            user.userprofile.id_number = self.cleaned_data['id_number']
            user.userprofile.save()
        return user





class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
