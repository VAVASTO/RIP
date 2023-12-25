from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import status as drf_status
from pages.serializers import BouquetSerializer
from pages.serializers import ApplicationSerializer
from pages.serializers import BouquetApplication
from pages.serializers import ServiceApplicationSerializer
from drf_yasg.utils import swagger_auto_schema
from pages.models import BouquetType
from rest_framework.decorators import api_view
from pages.models import Users
from pages.models import ServiceApplication
from datetime import datetime
from minio import Minio

from django.http import JsonResponse
from enum import Enum
import hashlib
import secrets

from pages.redis_view import (
    set_key,
    get_value,
    delete_value
)

class UsersENUM(Enum):
    MANAGER_ID = 1
    USER_ID = 2
    
client = Minio(endpoint="localhost:9000",   # адрес сервера
               access_key='minio',          # логин админа
               secret_key='minio124',       # пароль админа
               secure=False)

def check_user(request):
    response = login_view_get(request._request)
    if response.status_code == 200:
        user = Users.objects.get(user_id=response.data.get('user_id').decode())
        return user.role == 'USR'
    return False

def check_authorize(request):
    response = login_view_get(request._request)
    if response.status_code == 200:
        user = Users.objects.get(user_id=response.data.get('user_id'))
        return user
    return None

def check_moderator(request):
    response = login_view_get(request._request)
    if response.status_code == 200:
        user = Users.objects.get(user_id=response.data.get('user_id'))
        return user.role == 'MOD'
    return False

@api_view(['POST'])
def registration(request, format=None):
    required_fields = ['name', 'phone', 'email', 'position', 'status', 'login', 'password']
    missing_fields = [field for field in required_fields if field not in request.data]

    if missing_fields:
        return Response({'Ошибка': f'Не хватает обязательных полей: {", ".join(missing_fields)}'}, status=status.HTTP_400_BAD_REQUEST)

    if Users.objects.filter(email=request.data['email']).exists() or Users.objects.filter(login=request.data['login']).exists():
        return Response({'Ошибка': 'Пользователь с таким email или login уже существует'}, status=status.HTTP_400_BAD_REQUEST)

    Users.objects.create(
        name=request.data['name'],
        phone=request.data['phone'],
        email=request.data['email'],
        position = request.data['position'],
        status = request.data['status'],
        login=request.data['login'],
        password=request.data['password'],
    )
    return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
def login_view(request, format=None):
    print(request.COOKIES)
    existing_session = request.COOKIES.get('session_key')
    if existing_session and get_value(existing_session):
        return Response({'user_id': get_value(existing_session), 'session_key': existing_session, 'username': Users.objects.get(id=get_value(existing_session)).name})

    login_ = request.data.get("login")
    password = request.data.get("password")
    
    if not login_ or not password:
        return Response({'error': 'Необходимы логин и пароль'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = Users.objects.get(login=login_)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    if password == user.password:
        random_part = secrets.token_hex(8)
        session_hash = hashlib.sha256(f'{user.user_id}:{login_}:{random_part}'.encode()).hexdigest()
        set_key(session_hash, user.user_id)
        response = JsonResponse({'user_id': user.user_id, 'session_key': session_hash, 'username': user.name})
        response.set_cookie('session_key', session_hash, max_age=86400)
        return response

    return Response(status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def logout_view(request):
    print(request.headers)
    session_key = request.COOKIES.get('session_key')

    if session_key:
        if not get_value(session_key):
            return JsonResponse({'error': 'Вы не авторизованы'}, status=status.HTTP_401_UNAUTHORIZED)
        delete_value(session_key)
        response = JsonResponse({'message': 'Вы успешно вышли из системы'})
        response.delete_cookie('session_key')
        return response
    else:
        return JsonResponse({'error': 'Вы не авторизованы'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET'])
def login_view_get(request, format=None):
    existing_session = request.COOKIES.get('session_key')
    if existing_session and get_value(existing_session):
        return Response({'user_id': get_value(existing_session)})
    return Response(status=status.HTTP_401_UNAUTHORIZED)

@swagger_auto_schema(method='get', operation_summary="Get Bouquet List", responses={200: BouquetSerializer(many=True)})
@api_view(["GET"])
def get_bouquet_list(request, format=None):
    query = request.GET.get('q')
    price = request.GET.get('price')
    print(query)  # Print the query to debug
    
    if query:
        bouquet_type_list = BouquetType.objects.filter(name__icontains=query, status='in_stock').order_by("bouquet_id")
    else:
        bouquet_type_list = BouquetType.objects.filter(status='in_stock').order_by("bouquet_id")
    
    if price:
        bouquet_type_list = bouquet_type_list.filter(price=price)

    serializer = BouquetSerializer(bouquet_type_list, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='get', operation_summary="Get Bouquet Detail", responses={200: BouquetSerializer()})
@api_view(["Get"])
def get_bouquet_detail(application, pk, format=None):
    bouquet = get_object_or_404(BouquetType, pk=pk)
    if application.method == 'GET':
        serializer = BouquetSerializer(bouquet)
        return Response(serializer.data)
    
@swagger_auto_schema(method='post', operation_summary="Create Bouquet", request_body=BouquetSerializer, responses={201: BouquetSerializer()})
@api_view(["Post"])
def create_bouquet(application, format=None):
    serializer = BouquetSerializer(data=application.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='POST', operation_summary="Add Bouquet to Application", request_body=BouquetSerializer, responses={200: 'OK', 404: 'Bouquet not found'})
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

@swagger_auto_schema(method='PUT', operation_summary="Change Bouquet Properties", request_body=BouquetSerializer, responses={200: BouquetSerializer(), 400: 'Bad Request'})
@api_view(["PUT"])
def change_bouquet_props(application, pk, format=None):
    bouquet = get_object_or_404(BouquetType, pk=pk)
    serializer = BouquetSerializer(bouquet, data=application.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='DELETE', operation_summary="Delete Bouquet", responses={204: 'No Content'})
@api_view(["Delete"])
def delete_bouquet(application, pk, format=None):
    bouquet = get_object_or_404(BouquetType, pk=pk)
    bouquet.status = "out_of_stock"
    bouquet.save()
    return Response(status=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(method='GET', operation_summary="Get Applications List", responses={200: ApplicationSerializer(many=True)})
@api_view(["Get"])
def get_applications_list(application, format=None):
    user = check_authorize(application)
    if not user:
        return Response(status=drf_status.HTTP_403_FORBIDDEN)
    
    if user.position == "moderator":

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

    else:
        start_date = application.GET.get('start_date', None)
        end_date = application.GET.get('end_date', None)
        status = application.GET.get('status', None)
        
        applications_list = ServiceApplication.objects.filter(status="formed")

        if start_date:
            applications_list = applications_list.filter(receiving_date__gte=start_date)
            if end_date:
                applications_list = applications_list.filter(receiving_date__lte=end_date)
        if status:
            applications_list = applications_list.filter(status=status)

        applications_list = applications_list.order_by('-receiving_date')
        serializer = ApplicationSerializer(applications_list, many=True)
        return Response(serializer.data)

@swagger_auto_schema(method='GET', operation_summary="Get Application Detail", responses={200: ServiceApplicationSerializer()})
@api_view(["Get"])
def get_application_detail(application, pk, format=None):
    service_application = get_object_or_404(ServiceApplication, pk=pk)
    serializer = ServiceApplicationSerializer(service_application)

    return Response(serializer.data)

@swagger_auto_schema(method='PUT', operation_summary="Change Bouquet Quantity", responses={200: ServiceApplicationSerializer(), 400: 'Bad Request'})
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
    
@swagger_auto_schema(method='DELETE', operation_summary="Delete Bouquet from Application", responses={200: ServiceApplicationSerializer()})
@api_view(["DELETE"])
def delete_bouquet_from_application(application, application_id, bouquet_id, format=None):
    service_application = get_object_or_404(ServiceApplication, pk=application_id)

    bouquet_application = get_object_or_404(BouquetApplication, application=service_application, bouquet_id=bouquet_id)

    bouquet_application.delete()

    serializer = ServiceApplicationSerializer(service_application)
    return Response(serializer.data, status=status.HTTP_200_OK)

@swagger_auto_schema(method='DELETE', operation_summary="Delete Service Application", responses={204: 'No Content'})
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

@swagger_auto_schema(method='PUT', operation_summary="Change Status (Manager)", responses={200: 'OK', 403: 'Forbidden', 400: 'Bad Request'})
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

@swagger_auto_schema(method='PUT', operation_summary="Change Status (Packer)", responses={200: 'OK', 403: 'Forbidden', 400: 'Bad Request'})
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

@swagger_auto_schema(method='PUT', operation_summary="Change Status (Courier)", responses={200: 'OK', 403: 'Forbidden', 400: 'Bad Request'})
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

@swagger_auto_schema(method='PUT', operation_summary="Change Status (Moderator)", responses={200: 'OK', 403: 'Forbidden', 400: 'Bad Request'})
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


@swagger_auto_schema(method='PUT', operation_summary="Update Service Application", responses={200: 'OK', 201: 'Created'})
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
    
