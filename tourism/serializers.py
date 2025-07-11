from rest_framework import serializers
from .models import TouristDestination, Hotel, Booking

class TouristDestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TouristDestination
        fields = '__all__'

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
