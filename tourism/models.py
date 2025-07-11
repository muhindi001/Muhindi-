from django.db import models
from django.contrib.auth.models import User


class TouristDestination(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    rating = models.IntegerField(default=0)  # Ensure this field exists

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("cancelled", "Cancelled"),
    ]

    PAYMENT_STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default="pending")
    payment_id = models.CharField(max_length=255, blank=True, null=True)  # Stripe or PayPal Payment ID

    def approve_booking(self):
        self.status = "approved"
        self.save()

    def cancel_booking(self):
        self.status = "cancelled"
        self.save()

    def mark_as_paid(self, payment_id):
        self.payment_status = "paid"
        self.payment_id = payment_id
        self.save()

    def __str__(self):
        return f"Booking by {self.user.username} at {self.hotel.name} - {self.status}"

class TourismLocation(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    category = models.CharField(max_length=50, choices=[('restaurant', 'Restaurant'), ('hotel', 'Hotel')])
    rating = models.FloatField()
    image_url = models.URLField()

    def __str__(self):
        return self.name