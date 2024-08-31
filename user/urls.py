from django.urls import path
from . import views
from .views import (
    CustomPasswordResetView,
    CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetCompleteView,
)

urlpatterns = [
    # auth urls
    path('signup/', views.register_user, name='register_user'),
    path('login/', views.login_view, name='login'),
    path('user-account/', views.user_account, name="user_account"),
    path('admin-account/', views.admin_account, name="admin_account"),
    path('admin-profile/', views.admin_profile, name="admin_profile" ),
    path('logout/', views.custom_logout, name='logout'),
    path('user-change-password/', views.user_change_password, name="user-change-password"),
    path('admin-change-password/', views.admin_change_password, name="admin-change-password"),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),

]