from django import forms
from .models import Land, Parcel, SoilAnalysis, IrrigationRecord
from django.core.validators import MinValueValidator

class LandForm(forms.ModelForm):
    """Form for Land model"""
    class Meta:
        model = Land
        fields = ['name', 'total_area', 'location', 'address', 'latitude', 'longitude', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        
    def clean_total_area(self):
        total_area = self.cleaned_data.get('total_area')
        if total_area and total_area <= 0:
            raise forms.ValidationError("Alan değeri sıfırdan büyük olmalıdır.")
        return total_area

class ParcelForm(forms.ModelForm):
    """Form for Parcel model"""
    class Meta:
        model = Parcel
        fields = ['parcel_no', 'area', 'soil_type', 'has_irrigation', 'coordinates', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'coordinates': forms.Textarea(attrs={'rows': 3, 'placeholder': 'GeoJSON formatında koordinatlar (opsiyonel)'}),
        }
        
    def clean_area(self):
        area = self.cleaned_data.get('area')
        if area and area <= 0:
            raise forms.ValidationError("Alan değeri sıfırdan büyük olmalıdır.")
        return area

class SoilAnalysisForm(forms.ModelForm):
    """Form for SoilAnalysis model"""
    class Meta:
        model = SoilAnalysis
        fields = [
            'analysis_date', 'ph_value', 'organic_matter', 'phosphorus', 
            'potassium', 'calcium', 'magnesium', 'iron', 'zinc', 
            'report_file', 'description'
        ]
        widgets = {
            'analysis_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        
    def clean_ph_value(self):
        ph_value = self.cleaned_data.get('ph_value')
        if ph_value and (ph_value < 0 or ph_value > 14):
            raise forms.ValidationError("pH değeri 0-14 arasında olmalıdır.")
        return ph_value

class IrrigationRecordForm(forms.ModelForm):
    """Form for IrrigationRecord model"""
    class Meta:
        model = IrrigationRecord
        fields = [
            'irrigation_date', 'irrigation_duration', 'water_amount', 
            'irrigation_method', 'description'
        ]
        widgets = {
            'irrigation_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        
    def clean_water_amount(self):
        water_amount = self.cleaned_data.get('water_amount')
        if water_amount and water_amount <= 0:
            raise forms.ValidationError("Su miktarı sıfırdan büyük olmalıdır.")
        return water_amount 