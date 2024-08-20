from django.urls import path
from . import views

urlpatterns = [
    # home urls
    path("", views.index, name="index"),
    path('bus-search', views.bus_search, name="bus_search"),
    # booking urls
    path('book/customer-info/', views.customer_info, name='customer_info'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('daraja/stk_push', views.stk_push_callback, name="stk_push_callback"),
    path('booking/pay', views.pay, name="confirm_payment"),
    path('bookings', views.all_bookings, name="bookings"),
    # routes urls
    path('routes', views.routes, name="routes"),
    path('routes/delete/<int:pk>/', views.delete_route, name="delete_route"),
    path('route/edit/<int:route_id>/', views.edit_route, name='edit_route'),
    # buses urls
    path('buses/', views.list_buses, name='list_buses'),
    path('bus/edit/<int:bus_id>/', views.edit_bus, name='edit_bus'),
    path('buses/delete/<int:pk>/', views.delete_bus, name="delete_bus"),
    # auth urls
    path('signup/', views.register_user, name='register_user'),
    path('login/', views.login_view, name='login'),
    path('user-account/', views.user_account, name="user_account"),
    path('admin-account/', views.admin_account, name="admin_account"),
    path('logout/', views.custom_logout, name='logout'),
    path('user-change-password/', views.user_change_password, name="user-change-password"),
    path('admin-change-password/', views.admin_change_password, name="admin-change-password"),

]