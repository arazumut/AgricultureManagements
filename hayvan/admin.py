from django.contrib import admin
from .models import (
    AnimalType, AnimalBreed, Animal, AnimalGroup, 
    HealthRecord, FeedRation, FeedRationDetail, Feeding,
    ReproductionRecord, Birth, Offspring
)

@admin.register(AnimalType)
class AnimalTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(AnimalBreed)
class AnimalBreedAdmin(admin.ModelAdmin):
    list_display = ['name', 'animal_type', 'characteristics']
    list_filter = ['animal_type']
    search_fields = ['name', 'animal_type__name']

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ['tag_number', 'animal_type', 'breed', 'gender', 'birth_date', 'weight', 'is_active', 'get_age']
    list_filter = ['animal_type', 'breed', 'gender', 'is_active']
    search_fields = ['tag_number', 'mother_tag_number', 'father_tag_number']
    readonly_fields = ['created_at', 'updated_at', 'get_age']
    fieldsets = (
        ('Temel Bilgiler', {
            'fields': ('tag_number', 'animal_type', 'breed', 'gender', 'birth_date', 'is_active', 'get_age')
        }),
        ('Aile Bilgileri', {
            'fields': ('mother_tag_number', 'father_tag_number', 'parent_birth')
        }),
        ('Fiziksel Bilgiler', {
            'fields': ('weight', 'image')
        }),
        ('Satın Alma Bilgileri', {
            'fields': ('arrival_date', 'source', 'purchase_price')
        }),
        ('Diğer', {
            'fields': ('notes', 'owner', 'created_at', 'updated_at')
        }),
    )

@admin.register(AnimalGroup)
class AnimalGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']
    filter_horizontal = ['animals']

@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ['animal', 'procedure_date', 'procedure_type', 'diagnosis', 'veterinarian', 'cost']
    list_filter = ['procedure_type', 'procedure_date']
    search_fields = ['animal__tag_number', 'diagnosis', 'treatment', 'veterinarian']
    date_hierarchy = 'procedure_date'

@admin.register(FeedRation)
class FeedRationAdmin(admin.ModelAdmin):
    list_display = ['name', 'animal_type', 'age_group', 'production_purpose']
    list_filter = ['animal_type']
    search_fields = ['name', 'animal_type__name']

@admin.register(FeedRationDetail)
class FeedRationDetailAdmin(admin.ModelAdmin):
    list_display = ['feed_ration', 'feed_name', 'amount', 'unit_price']
    list_filter = ['feed_ration']
    search_fields = ['feed_ration__name', 'feed_name']

@admin.register(Feeding)
class FeedingAdmin(admin.ModelAdmin):
    list_display = ['animal', 'animal_group', 'feed_ration', 'feeding_date', 'amount']
    list_filter = ['feeding_date']
    search_fields = ['animal__tag_number', 'animal_group__name', 'feed_ration__name']
    date_hierarchy = 'feeding_date'

@admin.register(ReproductionRecord)
class ReproductionRecordAdmin(admin.ModelAdmin):
    list_display = ['animal', 'insemination_date', 'insemination_type', 'pregnancy_status', 'expected_birth_date']
    list_filter = ['insemination_date', 'insemination_type', 'pregnancy_status']
    search_fields = ['animal__tag_number', 'father_tag_number', 'semen_source']
    date_hierarchy = 'insemination_date'

@admin.register(Birth)
class BirthAdmin(admin.ModelAdmin):
    list_display = ['animal', 'birth_date', 'offspring_count', 'male_count', 'female_count', 'stillborn_count']
    list_filter = ['birth_date', 'difficulty']
    search_fields = ['animal__tag_number']
    date_hierarchy = 'birth_date'

@admin.register(Offspring)
class OffspringAdmin(admin.ModelAdmin):
    list_display = ['birth', 'tag_number', 'gender', 'birth_weight', 'animal']
    list_filter = ['gender']
    search_fields = ['tag_number', 'birth__animal__tag_number']
