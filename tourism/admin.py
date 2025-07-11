from django.contrib import admin
from .models import Hotel, Booking, TouristDestination, TourismLocation
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

# Register the User model only if it is not already registered
if not admin.site.is_registered(User):
    admin.site.register(User, UserAdmin)

# Register your models here.

class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "hotel", "check_in", "check_out", "status", "payment_status")
    list_filter = ("status", "payment_status")
    actions = ["approve_bookings", "cancel_bookings"]

    def approve_bookings(self, request, queryset):
        queryset.update(status="approved")
        self.message_user(request, "Selected bookings have been approved.")

    def cancel_bookings(self, request, queryset):
        queryset.update(status="cancelled")
        self.message_user(request, "Selected bookings have been cancelled.")

    approve_bookings.short_description = "Approve selected bookings"
    cancel_bookings.short_description = "Cancel selected bookings"

# Register models
admin.site.register(Hotel)
admin.site.register(Booking, BookingAdmin)
admin.site.register(TouristDestination)
admin.site.register(TourismLocation)
