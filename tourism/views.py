from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.views.static import serve
from rest_framework import generics
from .models import Booking, Hotel, TouristDestination
from .serializers import BookingSerializer, HotelSerializer, TouristDestinationSerializer
from django.contrib.auth import login
from .forms import RegisterForm
import os
import stripe
from tourism.models import Hotel
from .models import Hotel

#  Stripe Configuration
stripe.api_key = settings.STRIPE_SECRET_KEY

from django.shortcuts import render, redirect
from .forms import RegisterForm

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        
        if form.is_valid():
            form.save() 

            return redirect("/")  
    else:
        form = RegisterForm()
    return render(request, "tourism/register.html", {"form": form})

#  Home View
def home(request):
    return render(request, "tourism/home.html")

#  About View
def about(request):
    return render(request, "tourism/about.html")

#  Contact Form with Email Support
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(subject, full_message, settings.EMAIL_HOST_USER, ['your-email@example.com'])
            messages.success(request, "Your message has been sent successfully!")
        except:
            messages.error(request, "Failed to send message. Please try again later.")

        return redirect("contact")

    return render(request, "tourism/contact.html")

#  Hotel Listing View
def hotels_view(request):
    hotels = Hotel.objects.all()  # Fetch all hotels from the database
    return render(request, 'tourism/hotels.html', {'hotels': hotels})

#  Destination Listing View
def destinations(request):
    destinations = TouristDestination.objects.all()
    return render(request, "tourism/destinations.html", {"destinations": destinations})

#  Display Tourism Locations on a Map
def tourism_map(request):
    return render(request, 'tourism/tourism_map.html')



# Serve Media Files in Development
def serve_media(request, path):
    media_root = settings.MEDIA_ROOT
    file_path = os.path.join(media_root, path)
    
    if os.path.exists(file_path):
        return serve(request, path, document_root=media_root)
    else:
        return HttpResponse("File not found", status=404)

#  Hotel Booking View (Only for Logged-in Users)
@login_required
def book_hotel(request, hotel_id):
    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == "POST":
        check_in = request.POST.get("check_in")
        check_out = request.POST.get("check_out")
        guests = request.POST.get("guests", 1)

        # Create booking
        booking = Booking.objects.create(
            user=request.user,
            hotel=hotel,
            check_in=check_in,
            check_out=check_out,
            guests=guests,
            status="pending",
        )

        messages.success(request, "Booking successful! Awaiting confirmation.")
        return redirect("booking_confirmation", booking_id=booking.id)

    return render(request, "tourism/book_hotel.html", {"hotel": hotel})

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, "tourism/booking_confirmation.html", {"booking": booking})

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if booking.status != "cancelled":
        booking.cancel_booking()
        messages.success(request, "Your booking has been cancelled.")

    return redirect("user_bookings")

@login_required
def process_payment(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    try:
        # Create Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': booking.hotel.name},
                    'unit_amount': int(booking.hotel.price_per_night * 100),  # Convert to cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(f'/payment/success/{booking.id}/'),
            cancel_url=request.build_absolute_uri(f'/payment/cancel/{booking.id}/'),
        )
        return redirect(session.url)

    except Exception as e:
        messages.error(request, f"Payment failed: {str(e)}")
        return redirect("booking_confirmation", booking_id=booking.id)
    
@login_required
def payment_success(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.mark_as_paid(payment_id="STRIPE_PAYMENT_ID")
    messages.success(request, "Payment successful! Your booking is now confirmed.")
    return redirect("booking_confirmation", booking_id=booking_id)  # Changed to use parameter

@login_required
def payment_cancel(request, booking_id):
    messages.warning(request, "Payment was cancelled. Please try again.")
    return redirect("booking_confirmation", booking_id=booking_id)  # Fixed undefined variable

def booking_success(request):
    return render(request, 'tourism/booking_success.html')

class DestinationListCreateView(generics.ListCreateAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationSerializer

class HotelListCreateView(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class BookingListCreateView(generics.ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class DestinationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = TouristDestination.objects.all()
    serializer_class = TouristDestinationSerializer

class HotelDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

class BookingDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

def forgot_password(request):
    return render(request, 'tourism/forgotpassword.html')

def login_view(request):
    return render(request, 'tourism/login.html')

# start up
