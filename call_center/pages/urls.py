from django.contrib import admin
from django.urls import path
from pages import views
from rest_framework import routers
from django.urls import include, path

urlpatterns = [
    path(r"bouquets/", views.get_bouquet_list, name='bouquet_type_list'),
    path(r'bouquets/<int:pk>/', views.get_bouquet_detail, name='bouquet_type_detail'),
    path(r'bouquets/add/', views.add_bouquet, name='add_bouquet'),
    path(r'bouquets/<int:pk>/edit/', views.change_bouquet_props, name='change_bouquet_props'),
    path(r'bouquets/<int:pk>/delete/', views.delete_bouquet, name='delete_bouquet'),

    path(r"requests/", views.get_requests_list, name='reqests_list'),
    path(r"requests/<int:pk>/", views.get_request_detail, name='get_request_detail'),
    path(r"requests/<int:pk>/add_bouquet/", views.add_bouquet_to_service_request, name='add_bouquet_to_request'),
    path(r'requests/<int:request_id>/bouquets/<int:bouquet_id>/', views.change_bouquet_quantity, name='change_bouquet_quantity'),
    path(r'requests/<int:request_id>/bouquets_delete/<int:bouquet_id>/', views.delete_bouquet_from_service_request, name='delete_bouquet'),
    path(r'requests/<int:request_id>/delete/', views.delete_service_request, name='delete_service_request'),
    path(r'requests/<int:request_id>/change_status/', views.change_service_request_status, name='change_service_request_status'),
    path(r'requests/new_service_request/', views.new_service_request, name='new_service_request'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
