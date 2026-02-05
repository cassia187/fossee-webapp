from django.contrib import admin
from .models import Dataset, Equipment
# Register your models here.

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['filename', 'user', 'uploaded_at', 'total_count']
    list_filter = ['user', 'uploaded_at']

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'equipment_type', 'flowrate', 'pressure', 'temperature']
    list_filter = ['equipment_type']