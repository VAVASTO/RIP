from django.contrib import admin
from .models import BouquetRequest, BouquetType, Users, ServiceRequest

admin.site.register(BouquetRequest)
admin.site.register(BouquetType)
admin.site.register(Users)
admin.site.register(ServiceRequest)
