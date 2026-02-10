from django.urls import path
from . import views

urlpatterns = [
    path('api/register/', views.register),
    path('api/login/', views.login),
    path('api/logout/', views.logout),
    path('api/profile/', views.profile),
    path('api/health_check/', views.health_check),
    path('api/upload/', views.upload_dataset),
    path('api/datasets/', views.get_datasets),
    path('api/datasets/<int:dataset_id>/', views.get_dataset_details),
    path('api/datasets/<int:dataset_id>/delete/', views.delete_dataset),
    path('api/datasets/<int:dataset_id>/type_distribution/', views.get_type_distribution),
    path('api/datasets/<int:dataset_id>/report/', views.generate_pdf),
    path('api/datasets/<int:dataset_id>/raw/', views.get_raw_data)
]