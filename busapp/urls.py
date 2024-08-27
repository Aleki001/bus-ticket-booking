from django.urls import path
from . import views

urlpatterns = [
    # home urls
    path("", views.index, name="index"),
    path('bus-search', views.bus_search, name="bus_search"),
    # booking urls
    path('book/customer-info/', views.customer_info, name='customer_info'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('booking/pay', views.pay, name="confirm_payment"),
    path('mpesa/callback/', views.callback, name="mpesa-callback"),
    path('bookings', views.all_bookings, name="bookings"),
    path('user-bookings', views.user_bookings, name="user_bookings"),
    # routes urls
    path('routes', views.routes, name="routes"),
    path('routes/delete/<int:pk>/', views.delete_route, name="delete_route"),
    path('route/edit/<int:route_id>/', views.edit_route, name='edit_route'),
    # buses urls
    path('buses/', views.list_buses, name='list_buses'),
    path('bus/edit/<int:bus_id>/', views.edit_bus, name='edit_bus'),
    path('buses/delete/<int:pk>/', views.delete_bus, name="delete_bus"),

]