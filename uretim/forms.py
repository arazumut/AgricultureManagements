from django import forms
from .models import Product, Seed, PlantingPlan, Planting, Harvest, FertilizationRecord, PesticideApplication
from arazi.models import Parcel

class ProductForm(forms.ModelForm):
    """Form for Product model"""
    class Meta:
        model = Product
        fields = ['name', 'type', 'variety', 'growing_time', 'planting_interval', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'planting_interval': forms.TextInput(attrs={'placeholder': 'Örn: Nisan-Mayıs veya her zaman'}),
        }

class SeedForm(forms.ModelForm):
    """Form for Seed model"""
    class Meta:
        model = Seed
        fields = ['product', 'brand', 'certificate_no', 'lot_no', 'supplier', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class PlantingPlanForm(forms.ModelForm):
    """Form for PlantingPlan model"""
    class Meta:
        model = PlantingPlan
        fields = ['parcel', 'product', 'planned_planting_date', 'planned_harvest_date', 'planned_amount', 'description']
        widgets = {
            'planned_planting_date': forms.DateInput(attrs={'type': 'date'}),
            'planned_harvest_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PlantingPlanForm, self).__init__(*args, **kwargs)
        
        if user:
            # Filter parcels by user
            self.fields['parcel'].queryset = Parcel.objects.filter(land__owner=user, is_active=True)

class PlantingForm(forms.ModelForm):
    """Form for Planting model"""
    class Meta:
        model = Planting
        fields = [
            'planting_plan', 'parcel', 'product', 'seed', 'planting_date',
            'planting_area', 'seed_amount', 'planting_method', 'planting_depth',
            'row_spacing', 'estimated_harvest_date', 'description'
        ]
        widgets = {
            'planting_date': forms.DateInput(attrs={'type': 'date'}),
            'estimated_harvest_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(PlantingForm, self).__init__(*args, **kwargs)
        
        if user:
            # Filter parcels and plans by user
            self.fields['parcel'].queryset = Parcel.objects.filter(land__owner=user, is_active=True)
            self.fields['planting_plan'].queryset = PlantingPlan.objects.filter(
                parcel__land__owner=user, is_completed=False
            )
        
        # Add product-specific seed filtering
        if 'product' in self.data:
            try:
                product_id = int(self.data.get('product'))
                self.fields['seed'].queryset = Seed.objects.filter(product_id=product_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.product:
            self.fields['seed'].queryset = Seed.objects.filter(product=self.instance.product)
        else:
            self.fields['seed'].queryset = Seed.objects.none()

class HarvestForm(forms.ModelForm):
    """Form for Harvest model"""
    class Meta:
        model = Harvest
        fields = [
            'harvest_date', 'harvest_amount', 'moisture_content', 'quality_class',
            'harvest_method', 'stored_amount', 'sold_amount', 'description'
        ]
        widgets = {
            'harvest_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        harvest_amount = cleaned_data.get('harvest_amount')
        stored_amount = cleaned_data.get('stored_amount')
        sold_amount = cleaned_data.get('sold_amount')
        
        # Validate that stored + sold amounts don't exceed harvest amount
        if harvest_amount and stored_amount and sold_amount:
            if stored_amount + sold_amount > harvest_amount:
                raise forms.ValidationError(
                    "Depolanan ve satılan miktar toplamı, hasat miktarını aşamaz."
                )
        
        return cleaned_data

class FertilizationRecordForm(forms.ModelForm):
    """Form for FertilizationRecord model"""
    class Meta:
        model = FertilizationRecord
        fields = [
            'fertilization_date', 'fertilizer_name', 'fertilizer_type',
            'application_rate', 'total_amount', 'application_method', 'description'
        ]
        widgets = {
            'fertilization_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class PesticideApplicationForm(forms.ModelForm):
    """Form for PesticideApplication model"""
    class Meta:
        model = PesticideApplication
        fields = [
            'application_date', 'pesticide_name', 'pesticide_type',
            'active_ingredient', 'application_dose', 'total_amount',
            'application_method', 'waiting_period', 'target_pest', 'description'
        ]
        widgets = {
            'application_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        } 