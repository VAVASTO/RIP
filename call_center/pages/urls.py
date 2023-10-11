from django.urls import path
from pages import views

urlpatterns = [
    path("", views.services, name='services'),
    path("view_service/<int:model_id>/", views.view_service, name='view_service'),
    path("update_cards_page/<int:model_id>/", views.update_cards_page, name='update_cards_page'),
]
