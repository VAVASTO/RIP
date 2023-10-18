from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from pages.serializers import BouquetSerializer
from pages.serializers import RequestSerializer
from pages.serializers import BouquetRequest
from pages.serializers import BouquetRequestSerializer
from pages.serializers import ServiceRequestSerializer
from pages.models import BouquetType
from rest_framework.decorators import api_view
from pages.models import Users
from pages.models import ServiceRequest
from datetime import datetime

from enum import Enum

class UsersENUM(Enum):
    MODERATOR_ID = 1
    USER_ID = 2
    

@api_view(["Get"])
def get_bouquet_list(request, format=None):
    bouquet_type_list = BouquetType.objects.filter(status="in_stock")
    serializer = BouquetSerializer(bouquet_type_list, many=True)
    return Response(serializer.data)

@api_view(["Get"])
def get_bouquet_detail(request, pk, format=None):
    bouquet = get_object_or_404(BouquetType, pk=pk)
    if request.method == 'GET':
        serializer = BouquetSerializer(bouquet)
        return Response(serializer.data)
    

@api_view(["Post"])
def add_bouquet(request, format=None):
    user_id = UsersENUM.MODERATOR_ID.value
    user_status = Users.objects.get(user_id=user_id).position
    if user_status == "manager":
        serializer = BouquetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"Error": "This user cannot add new bouquets"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["Put"])
def change_bouquet_props(request, pk, format=None):
    user_id = UsersENUM.MODERATOR_ID.value
    user_status = Users.objects.get(user_id=user_id).position
    if user_status == "manager":
        bouquet = get_object_or_404(BouquetType, pk=pk)
        serializer = BouquetSerializer(bouquet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"Error": "This user cannot change bouquets"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["Delete"])
def delete_bouquet(request, pk, format=None):
    user_id = UsersENUM.MODERATOR_ID.value
    user_status = Users.objects.get(user_id=user_id).position
    if user_status == "manager":
        bouquet = get_object_or_404(BouquetType, pk=pk)
        bouquet.status = "out_of_stock"
        bouquet.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({"Error": "This user cannot delete bouquets"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(["Get"])
def get_requests_list(request, format=None):

    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)
    status = request.GET.get('status', None)
    
    requests_list = ServiceRequest.objects.all()

    if start_date:
        requests_list = requests_list.filter(receiving_date__gte=start_date)
        if end_date:
            requests_list = requests_list.filter(receiving_date__lte=end_date)
    if status:
        requests_list = requests_list.filter(status=status)

    serializer = RequestSerializer(requests_list, many=True)
    return Response(serializer.data)

@api_view(["Get"])
def get_request_detail(request, pk, format=None):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    serializer = ServiceRequestSerializer(service_request)

    return Response(serializer.data)

@api_view(["POST"])
def add_bouquet_to_service_request(request, pk, format=None):
    service_request = get_object_or_404(ServiceRequest, pk=pk)

    bouquet_id = request.data.get('bouquet_id')

    try:
        bouquet = BouquetType.objects.get(bouquet_id=bouquet_id)
    except BouquetType.DoesNotExist:
        return Response({'error': 'Bouquet not found'}, status=status.HTTP_404_NOT_FOUND)

    bouquet_request = BouquetRequest.objects.create(
        bouquet=bouquet,
        request=service_request,
        quantity=request.data.get('quantity', 1)
    )

    serializer = ServiceRequestSerializer(service_request)

    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["PUT"])
def change_bouquet_quantity(request, request_id, bouquet_id, format=None):
    service_request = get_object_or_404(ServiceRequest, pk=request_id)

    bouquet_request = get_object_or_404(BouquetRequest, request=service_request, bouquet_id=bouquet_id)

    new_quantity = request.data.get('quantity')
    if new_quantity is not None:
        bouquet_request.quantity = new_quantity
        bouquet_request.save()

        serializer = ServiceRequestSerializer(service_request)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Quantity is required'}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(["DELETE"])
def delete_bouquet_from_service_request(request, request_id, bouquet_id, format=None):
    service_request = get_object_or_404(ServiceRequest, pk=request_id)

    bouquet_request = get_object_or_404(BouquetRequest, request=service_request, bouquet_id=bouquet_id)

    bouquet_request.delete()

    serializer = ServiceRequestSerializer(service_request)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["DELETE"])
def delete_service_request(request, request_id, format=None):
    service_request = get_object_or_404(ServiceRequest, pk=request_id)

    user_id = request.query_params.get('user_id')

    try:
        user = Users.objects.get(user_id=user_id)
        if user.position != 'manager':
            return Response({'error': 'User does not have manager status'}, status=status.HTTP_403_FORBIDDEN)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    service_request.status = 'deleted'
    service_request.save()

    return Response({'message': 'Service request deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

@api_view(["PUT"])
def change_service_request_status(request, request_id, format=None):
    service_request = get_object_or_404(ServiceRequest, pk=request_id)

    user_id = request.query_params.get('user_id')
    print(f"user_id = {user_id}")

    try:
        user = Users.objects.get(user_id=user_id)
        current_status = service_request.status
        new_status = request.data.get('status')

        if current_status == 'draft':
            if user.position != 'manager':
                return Response({'error': 'Manager status required to change status from draft to formed'}, status=status.HTTP_403_FORBIDDEN)

            if not new_status:
                return Response({'error': 'Status not found'}, status=status.HTTP_403_FORBIDDEN)
            service_request.status = 'formed'
            
            service_request.receiving_date = datetime.now()

        elif current_status == 'formed':
            if user.position != 'packer':
                return Response({'error': 'Packer status required to change status from formed to packed or rejected'}, status=status.HTTP_403_FORBIDDEN)
            
            if new_status in ['rejected', 'packed']:
                service_request.packer = user_id
                service_request.status = new_status
            else:
                return Response({'error': 'Invalid status. Allowed values: rejected, packed'}, status=status.HTTP_400_BAD_REQUEST)

        elif current_status == 'packed' or current_status == 'delivering':
            if user.position != 'courier':
                return Response({'error': 'Courier status required to change status from packed to delivering or completed'}, status=status.HTTP_403_FORBIDDEN)
         
            if new_status in ['delivering', 'completed']:
                service_request.courier = user
                service_request.status = new_status

                if new_status == 'completed':
                    service_request.completion_date = datetime.now()
            else:
                return Response({'error': 'Invalid status. Allowed values: delivering, completed'}, status=status.HTTP_400_BAD_REQUEST)

        service_request.save()
        return Response({'message': 'Service request status changed successfully'}, status=status.HTTP_200_OK)

    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def new_service_request(request, format=None):
    current_user_id = request.query_params.get('user_id')
    try:
        current_user = Users.objects.get(user_id=current_user_id)
    except Users.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if current_user.position != 'manager':
        return Response({'error': 'Manager status required to create a new service request'}, status=status.HTTP_403_FORBIDDEN)

    draft_request = ServiceRequest.objects.filter(manager=current_user, status='draft').first()

    if draft_request:
        bouquet_id = request.data.get('bouquet_id')
        quantity = request.data.get('quantity', 1)

        try:
            bouquet = BouquetType.objects.get(bouquet_id=bouquet_id)
        except BouquetType.DoesNotExist:
            return Response({'error': 'Bouquet not found'}, status=status.HTTP_404_NOT_FOUND)

        BouquetRequest.objects.create(bouquet=bouquet, request=draft_request, quantity=quantity)

        return Response({'message': 'Bouquet added to the existing draft request'}, status=status.HTTP_200_OK)
    else:
        client_name = request.data.get('client_name')
        client_phone = request.data.get('client_phone')
        client_address = request.data.get('client_address')
        delivery_date = request.data.get('delivery_date')

        new_request = ServiceRequest.objects.create(
            manager=current_user,
            client_name=client_name,
            client_phone=client_phone,
            client_address=client_address,
            delivery_date=delivery_date,
            status='draft'
        )

        bouquet_id = request.data.get('bouquet_id')
        quantity = request.data.get('quantity', 1)

        try:
            bouquet = BouquetType.objects.get(bouquet_id=bouquet_id)
        except BouquetType.DoesNotExist:
            new_request.delete()  
            return Response({'error': 'Bouquet not found'}, status=status.HTTP_404_NOT_FOUND)

        BouquetRequest.objects.create(bouquet=bouquet, request=new_request, quantity=quantity)

        return Response({'message': 'New service request created with the bouquet'}, status=status.HTTP_201_CREATED)
