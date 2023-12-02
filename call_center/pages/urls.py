from django.contrib import admin
from django.urls import path
from pages import views
from rest_framework import routers
from django.urls import include, path

urlpatterns = [
    path(r"bouquets/", views.get_bouquet_list, name='bouquet_type_list'),
    path(r'bouquets/<int:pk>/', views.get_bouquet_detail, name='bouquet_type_detail'),
    path(r'bouquets/create/', views.create_bouquet, name='add_bouquet'),
    path(r'bouquets/<int:pk>/edit/', views.change_bouquet_props, name='change_bouquet_props'),
    path(r'bouquets/<int:pk>/delete/', views.delete_bouquet, name='delete_bouquet'),
    path(r'bouquets/<int:pk>/<int:quantity>/add/', views.add_bouquet, name='add_bouquet'),

    path(r"applications/", views.get_applications_list, name='reqests_list'),
    path(r"applications/<int:pk>/", views.get_application_detail, name='get_application_detail'),
    path(r'applications/<int:application_id>/bouquets/<int:bouquet_id>/', views.change_bouquet_quantity, name='change_bouquet_quantity'),
    path(r'applications/<int:application_id>/bouquets_delete/<int:bouquet_id>/', views.delete_bouquet_from_application, name='delete_bouquet'),
    path(r'applications/<int:application_id>/delete/', views.delete_service_application, name='delete_service_application'),
    path(r'applications/<int:application_id>/change_status_manager/', views.change_status_manager, name='change_service_application_status_manager'),
    path(r'applications/<int:application_id>/change_status_packer/', views.change_status_packer, name='change_service_application_status_packer'),
    path(r'applications/<int:application_id>/change_status_courier/', views.change_status_courier, name='change_service_application_status_courier'),
    path(r'applications/<int:application_id>/change_status_moderator/', views.change_status_moderator, name='change_service_application_status_moderator'),
    path(r'applications/update_service_application/', views.update_service_application, name='new_service_application'),

    path(r'users/registration/', views.registration, name='registration'),
    path(r'users/login/', views.login_view, name='login'),
    path(r'users/logout/', views.logout_view, name='logout'),

    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
]
