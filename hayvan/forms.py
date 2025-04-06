from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Animal, HealthRecord, ReproductionRecord, Birth, Offspring

class AnimalForm(forms.ModelForm):
    """Form for creating and updating animal records"""
    
    class Meta:
        model = Animal
        fields = [
            'tag_number', 'animal_type', 'breed', 'gender', 'birth_date',
            'mother_tag_number', 'father_tag_number', 'arrival_date', 'source',
            'weight', 'purchase_price', 'image', 'notes'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'arrival_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Mark required fields
        for field_name in ['tag_number', 'animal_type', 'breed', 'gender', 'birth_date']:
            self.fields[field_name].required = True
            
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        # Add placeholder for tag number
        self.fields['tag_number'].widget.attrs['placeholder'] = _('Küpe numarasını giriniz')

class HealthRecordForm(forms.ModelForm):
    """Form for creating health records"""
    
    class Meta:
        model = HealthRecord
        fields = [
            'procedure_date', 'procedure_type', 'diagnosis', 'treatment',
            'medication', 'dosage', 'veterinarian', 'cost', 'notes'
        ]
        widgets = {
            'procedure_date': forms.DateInput(attrs={'type': 'date'}),
            'treatment': forms.Textarea(attrs={'rows': 3}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Mark required fields
        for field_name in ['procedure_date', 'procedure_type']:
            self.fields[field_name].required = True
            
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ReproductionRecordForm(forms.ModelForm):
    """Form for creating reproduction records"""
    
    class Meta:
        model = ReproductionRecord
        fields = [
            'insemination_date', 'insemination_type', 'father_tag_number',
            'semen_source', 'technician', 'cost', 'pregnancy_status',
            'pregnancy_check_date', 'expected_birth_date', 'notes'
        ]
        widgets = {
            'insemination_date': forms.DateInput(attrs={'type': 'date'}),
            'pregnancy_check_date': forms.DateInput(attrs={'type': 'date'}),
            'expected_birth_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Mark required fields
        self.fields['insemination_type'].required = True
            
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class BirthForm(forms.ModelForm):
    """Form for creating birth records"""
    
    class Meta:
        model = Birth
        fields = [
            'birth_date', 'reproduction_record', 'difficulty',
            'offspring_count', 'male_count', 'female_count',
            'stillborn_count', 'veterinarian', 'notes'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Mark required fields
        for field_name in ['birth_date', 'offspring_count']:
            self.fields[field_name].required = True
            
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        # Set initial values for counts
        if not self.instance.pk:  # Only for new instances
            self.fields['male_count'].initial = 0
            self.fields['female_count'].initial = 0
            self.fields['stillborn_count'].initial = 0
    
    def clean(self):
        cleaned_data = super().clean()
        offspring_count = cleaned_data.get('offspring_count', 0)
        male_count = cleaned_data.get('male_count', 0)
        female_count = cleaned_data.get('female_count', 0)
        stillborn_count = cleaned_data.get('stillborn_count', 0)
        
        # Check if the sum of counts matches offspring count
        total = male_count + female_count + stillborn_count
        if total != offspring_count:
            raise forms.ValidationError(
                _('Erkek, dişi ve ölü doğum sayılarının toplamı, toplam yavru sayısına eşit olmalıdır.'),
                code='invalid_counts'
            )
        
        return cleaned_data

class OffspringForm(forms.ModelForm):
    """Form for creating offspring records"""
    
    class Meta:
        model = Offspring
        fields = [
            'tag_number', 'gender', 'birth_weight', 'description'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 2}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Mark required fields
        self.fields['gender'].required = True
            
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control' 