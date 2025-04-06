from django.contrib import admin
from .models import Land, Parcel, SoilAnalysis, IrrigationRecord

@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_area', 'location', 'owner', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'location', 'address')
    date_hierarchy = 'created_at'

@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = ('land', 'parcel_no', 'area', 'soil_type', 'has_irrigation', 'is_active')
    list_filter = ('has_irrigation', 'is_active', 'soil_type')
    search_fields = ('parcel_no', 'land__name')

@admin.register(SoilAnalysis)
class SoilAnalysisAdmin(admin.ModelAdmin):
    list_display = ('parcel', 'analysis_date', 'ph_value', 'organic_matter')
    list_filter = ('analysis_date',)
    search_fields = ('parcel__parcel_no', 'parcel__land__name')
    date_hierarchy = 'analysis_date'

@admin.register(IrrigationRecord)
class IrrigationRecordAdmin(admin.ModelAdmin):
    list_display = ('parcel', 'irrigation_date', 'irrigation_method', 'water_amount')
    list_filter = ('irrigation_date', 'irrigation_method')
    search_fields = ('parcel__parcel_no', 'parcel__land__name')
    date_hierarchy = 'irrigation_date'
