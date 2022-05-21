from urllib import request
from django.forms import IntegerField
from rest_framework import serializers
from airlines_app.models import Airline, Plane, Pilot


class PilotSerializer(serializers.ModelSerializer):
    # pilot_user = serializers.StringRelatedField(read_only=True)
    plane_name = serializers.CharField(source='plane.title')
    
    class Meta:
        model = Pilot
        # exclude = ['plane']
        fields = '__all__'


class PlaneSerializer(serializers.ModelSerializer):
    Has_Pilot = PilotSerializer(many=True, read_only=True)
    airline_name = serializers.CharField(source='airline.title')
    class Meta:
        model = Plane
        fields = '__all__'


class AirlineSerializer(serializers.ModelSerializer):
    Has_Plane = PlaneSerializer(many=True, read_only=True)
    
    class Meta:
        model = Airline
        fields = '__all__'
