from rest_framework import serializers

from pages.models import BouquetType
from pages.models import Users
from pages.models import ServiceApplication
from pages.models import BouquetApplication

class BouquetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BouquetType
        fields = [
            "bouquet_id",
            "name",
            "description",
            "price",
            "image_url",
            "status",
        ]

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = [
            "user_id",
            "name",
            "phone",
            "email",
            "position",
            "status",
        ]

class ApplicationSerializer(serializers.ModelSerializer):
    manager = UsersSerializer(read_only=True)  
    packer = UsersSerializer(read_only=True)   
    courier = UsersSerializer(read_only=True)  

    class Meta:
        model = ServiceApplication
        fields = [
            "application_id",
            "manager",
            "packer",
            "courier",
            "client_name",
            "client_phone",
            "client_address",
            "receiving_date",
            "delivery_date",
            "completion_date",
            "status",
        ]

class BouquetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BouquetType
        fields = ['bouquet_id', 
                  'name',
                  'price',
                  'image_url']

class BouquetApplicationSerializer(serializers.ModelSerializer):
    bouquet = BouquetTypeSerializer()

    class Meta:
        model = BouquetApplication
        fields = ['bouquet', 
                  'quantity']

class ServiceApplicationSerializer(serializers.ModelSerializer):
    manager = UsersSerializer(read_only=True) 
    packer = UsersSerializer(read_only=True) 
    courier = UsersSerializer(read_only=True) 
    bouquet_details = BouquetApplicationSerializer(many=True, source='bouquetapplication_set')

    class Meta:
        model = ServiceApplication
        fields = ['application_id', 
                  'manager', 
                  'packer', 
                  'courier', 
                  'client_name', 
                  'client_phone',
                  'client_address', 
                  'receiving_date', 
                  'delivery_date', 
                  'completion_date', 
                  'status',
                  'bouquet_details']