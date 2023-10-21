from django.contrib import admin
from .models import BouquetApplication, BouquetType, Users, ServiceApplication

admin.site.register(BouquetApplication)
admin.site.register(BouquetType)
admin.site.register(Users)
admin.site.register(ServiceApplication)
