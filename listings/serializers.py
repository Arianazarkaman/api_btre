from rest_framework import serializers
from .models import Listing


class CustomListingSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Listing
        fields = '__all__'