from django.urls import path
from . import views
from .views import book_hotel, booking_success
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('home/', views.home, name='home'),  
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("register/", views.register, name="register"),
    path("destinations/", views.destinations, name="destinations"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("tourism_map/", views.tourism_map, name="tourism_map"),
    path('hotels/', views.hotels_view, name='hotels'),  
    path('book/<int:hotel_id>/', book_hotel, name='book_hotel'),
    path('booking-success/', booking_success, name='booking_success'),
    path("book-hotel/<int:hotel_id>/", book_hotel, name="book_hotel"),
    path("booking/confirmation/<int:booking_id>/", views.booking_confirmation, name="booking_confirmation"),
    path("booking/cancel/<int:booking_id>/", views.cancel_booking, name="cancel_booking"),
    path("payment/process/<int:booking_id>/", views.process_payment, name="process_payment"),
    path("payment/success/<int:booking_id>/", views.payment_success, name="payment_success"),
    path("payment/cancel/<int:booking_id>/", views.payment_cancel, name="payment_cancel"), 
    path('forgot-password/', views.forgot_password, name='forgot_password'),
]

from django.shortcuts import render

def booking_success(request):
    return render(request, 'tourism/booking_success.html')
