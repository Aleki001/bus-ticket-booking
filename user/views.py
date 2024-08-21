from django.shortcuts import render, redirect
from django.contrib import messages
from .models import UserProfile
from .forms import CustomUserChangeForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm




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
                print(user.is_staff)
                return redirect('admin_account')
            else:
                login(request, user)
                return redirect('user_account')
        else:
            return render(request, 'busapp/auth/login.html', {'error': 'Invalid credentials!! Try again.'})
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
        form = PasswordChangeForm(request.user)
    return render(request, 'busapp/admin/account.html', {'form': form})


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
        form = PasswordChangeForm(request.user)
    return render(request, 'busapp/admin/account.html', {'form': form})




@login_required
def admin_account(request):
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
            return redirect('admin_account')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomUserChangeForm(instance=user)
    
    return render(request, 'busapp/admin/account.html', {'form': form, 'profile': profile})


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

