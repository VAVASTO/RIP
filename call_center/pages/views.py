from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from pages.serializers import BouquetSerializer
from pages.serializers import ApplicationSerializer
from pages.serializers import BouquetApplication
from pages.serializers import BouquetApplicationSerializer
from pages.serializers import ServiceApplicationSerializer
from pages.models import BouquetType
from rest_framework.decorators import api_view
from pages.models import Users
from pages.models import ServiceApplication
from datetime import datetime
from minio import Minio

from enum import Enum

class UsersENUM(Enum):
    MANAGER_ID = 1
    USER_ID = 2
    
client = Minio(endpoint="localhost:9000",   # адрес сервера
               access_key='minio',          # логин админа
               secret_key='minio124',       # пароль админа
               secure=False)

@api_view(["Get"])
def get_bouquet_list(application, format=None):
    bouquet_type_list = BouquetType.objects.filter(status="in_stock")
    serializer = BouquetSerializer(bouquet_type_list, many=True)
    return Response(serializer.data)

@api_view(["Get"])
def get_bouquet_detail(application, pk, format=None):
    bouquet = get_object_or_404(BouquetType, pk=pk)
    if application.method == 'GET':
        serializer = BouquetSerializer(bouquet)
        return Response(serializer.data)
    

@api_view(["Post"])
def create_bouquet(application, format=None):
    serializer = BouquetSerializer(data=application.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def add_bouquet(application, pk, quantity, format=None):
    bouquet_id = pk
    draft_application = ServiceApplication.objects.filter(status='draft').first()
    if draft_application:
        print("draft_application")

        draft_application.save()
        print(f"bouquet_id = {bouquet_id}")
        if bouquet_id:
            try:
                bouquet = BouquetType.objects.get(bouquet_id=bouquet_id)
            except BouquetType.DoesNotExist:
                return Response({'error': 'Bouquet not found'}, status=status.HTTP_404_NOT_FOUND)

            BouquetApplication.objects.create(bouquet=bouquet, application=draft_application, quantity=quantity)

        return Response({'message': 'Bouquet added to the existing draft application'}, status=status.HTTP_200_OK)
    else:
        current_user = Users.objects.get(user_id=1)
        new_application = ServiceApplication.objects.create(
            manager=current_user,
            status='draft'
        )

        bouquet_id = application.data.get('bouquet_id')
        print(f"bouquet_id = {bouquet_id}")
        if bouquet_id:
            try:
                bouquet = BouquetType.objects.get(bouquet_id=bouquet_id)
                BouquetApplication.objects.create(bouquet=bouquet, application=new_application, quantity=quantity)
            except BouquetType.DoesNotExist:
                new_application.delete()  
                return Response({'error': 'Bouquet not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': 'New service application created with the bouquet'}, status=status.HTTP_201_CREATED)

@api_view(["PUT"])
def change_bouquet_props(application, pk, format=None):
    bouquet = get_object_or_404(BouquetType, pk=pk)
    serializer = BouquetSerializer(bouquet, data=application.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["Delete"])
def delete_bouquet(application, pk, format=None):
    bouquet = get_object_or_404(BouquetType, pk=pk)
    bouquet.status = "out_of_stock"
    bouquet.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(["Get"])
def get_applications_list(application, format=None):

    start_date = application.GET.get('start_date', None)
    end_date = application.GET.get('end_date', None)
    status = application.GET.get('status', None)
    
    applications_list = ServiceApplication.objects.all()

    if start_date:
        applications_list = applications_list.filter(receiving_date__gte=start_date)
        if end_date:
            applications_list = applications_list.filter(receiving_date__lte=end_date)
    if status:
        applications_list = applications_list.filter(status=status)

    applications_list = applications_list.order_by('-receiving_date')
    serializer = ApplicationSerializer(applications_list, many=True)
    return Response(serializer.data)

@api_view(["Get"])
def get_application_detail(application, pk, format=None):
    service_application = get_object_or_404(ServiceApplication, pk=pk)
    serializer = ServiceApplicationSerializer(service_application)

    return Response(serializer.data)

@api_view(["PUT"])
def change_bouquet_quantity(application, application_id, bouquet_id, format=None):
    service_application = get_object_or_404(ServiceApplication, pk=application_id)

    bouquet_application = get_object_or_404(BouquetApplication, application=service_application, bouquet_id=bouquet_id)

    new_quantity = application.data.get('quantity')
    if new_quantity is not None:
        bouquet_application.quantity = new_quantity
        bouquet_application.save()

        serializer = ServiceApplicationSerializer(service_application)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Quantity is required'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["DELETE"])
def delete_bouquet_from_application(application, application_id, bouquet_id, format=None):
    service_application = get_object_or_404(ServiceApplication, pk=application_id)

    bouquet_application = get_object_or_404(BouquetApplication, application=service_application, bouquet_id=bouquet_id)

    bouquet_application.delete()

    serializer = ServiceApplicationSerializer(service_application)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["DELETE"])
def delete_service_application(application, application_id, format=None):
    service_application = get_object_or_404(ServiceApplication, pk=application_id)

    user_id = application.query_params.get('user_id')

    try:
        user = Users.objects.get(user_id=user_id)
        if user.position != 'manager':
            return Response({'error': 'User does not have manager status'}, status=status.HTTP_403_FORBIDDEN)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    service_application.status = 'deleted'
    service_application.save()

    return Response({'message': 'Service application deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(["PUT"])
def change_status_manager(application, application_id, format=None):
    service_application = get_object_or_404(ServiceApplication, pk=application_id)

    current_status = service_application.status
    new_status = application.data.get('application_status')

    if not new_status:
        return Response({'error': 'Status not found'}, status=status.HTTP_403_FORBIDDEN)
    
    if current_status == 'draft':
        if new_status != 'formed' and new_status != 'deleted':
            return Response({'error': 'Manager status required to change status from draft to formed or deleted'}, status=status.HTTP_403_FORBIDDEN)
        service_application.status = new_status
        service_application.receiving_date = datetime.now()

        service_application.save()
        return Response({'message': 'Service application status changed successfully'}, status=status.HTTP_200_OK)
    
    if current_status == 'formed':       
        if new_status != 'draft' and new_status != 'deleted':
            return Response({'error': 'Manager status required to change status from formed to draft or deleted'}, status=status.HTTP_403_FORBIDDEN)
        service_application.status = new_status

        service_application.save()
        return Response({'message': 'Service application status changed successfully'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid status. Allowed values: draft, formed, deleted'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def change_status_packer(application, application_id, format=None):
    service_application = get_object_or_404(ServiceApplication, pk=application_id)

    current_status = service_application.status
    new_status = application.data.get('application_status')

    if not new_status:
        return Response({'error': 'Status not found'}, status=status.HTTP_403_FORBIDDEN)
    
    if current_status == 'formed':       
        if new_status != 'packed':
            return Response({'error': 'Packer status required to change status from formed to packed or rejected'}, status=status.HTTP_403_FORBIDDEN)
        service_application.status = new_status

        service_application.save()
        return Response({'message': 'Service application status changed successfully'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid status. Allowed values: formed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def change_status_courier(application, application_id, format=None):
    service_application = get_object_or_404(ServiceApplication, pk=application_id)

    current_status = service_application.status
    new_status = application.data.get('application_status')

    if not new_status:
        return Response({'error': 'Status not found'}, status=status.HTTP_403_FORBIDDEN)
    
    if current_status == 'packed':       
        if new_status != 'delivering':
            return Response({'error': 'Courier status required to change status from packed to delivering or completed'}, status=status.HTTP_403_FORBIDDEN)
        service_application.status = new_status

        service_application.save()
        return Response({'message': 'Service application status changed successfully'}, status=status.HTTP_200_OK)
    
    if current_status == 'delivering':       
        if new_status != 'completed':
            return Response({'error': 'Courier status required to change status from packed to delivering or completed'}, status=status.HTTP_403_FORBIDDEN)
        service_application.status = new_status

        service_application.save()
        return Response({'message': 'Service application status changed successfully'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid status. Allowed values: packed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
def change_status_moderator(application, application_id, format=None):
    service_application = get_object_or_404(ServiceApplication, pk=application_id)

    new_status = application.data.get('application_status')

    if not new_status:
        return Response({'error': 'Status not found'}, status=status.HTTP_403_FORBIDDEN)
       
    if new_status != 'cancelled':
        return Response({'error': 'Moderator status required to change status to cancelled'}, status=status.HTTP_403_FORBIDDEN)
    service_application.status = new_status

    service_application.save()
    return Response({'message': 'Service application status changed successfully'}, status=status.HTTP_200_OK)


@api_view(["PUT"])
def update_service_application(application, format=None):
    current_user = Users.objects.get(user_id=1)
    '''
    User status check

    try:
        current_user = Users.objects.get(user_id=current_user_id)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if current_user.position != 'manager':
        return Response({'error': 'Manager status required to create a new service application'}, status=status.HTTP_403_FORBIDDEN)

    Add manager check to filter
    '''
    draft_application = ServiceApplication.objects.filter(status='draft').first()

    client_name = application.data.get('client_name')
    client_phone = application.data.get('client_phone')
    client_address = application.data.get('client_address')
    delivery_date = application.data.get('delivery_date')
    if draft_application:
        print("draft_application")
        if client_name:
            draft_application.client_name = client_name
        if client_phone:
            draft_application.client_phone = client_phone
        if client_address:
            draft_application.client_address = client_address
        if delivery_date:
            draft_application.delivery_date = delivery_date

        draft_application.save()
        return Response({'message': 'Application updated successfully'}, status=status.HTTP_200_OK)

    new_application = ServiceApplication.objects.create(
        manager=current_user,
        client_name=client_name,
        client_phone=client_phone,
        client_address=client_address,
        delivery_date=delivery_date,
        status='draft'
    )

    BouquetApplication.objects.create(application=new_application)

    return Response({'message': 'New service application created'}, status=status.HTTP_201_CREATED)
    
