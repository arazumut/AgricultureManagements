from django import forms
from .models import WorkLog, Equipment

class WorkLogForm(forms.ModelForm):
    class Meta:
        model = WorkLog
        fields = ['worker', 'task', 'start_time', 'end_time', 'payment', 'is_paid', 'notes']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time > end_time:
            raise forms.ValidationError('Bitiş zamanı başlangıç zamanından önce olamaz.')
        
        return cleaned_data

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'equipment_type', 'model', 'manufacturer', 'serial_number', 
                 'purchase_date', 'purchase_price', 'status', 'notes', 'is_active']
        widgets = {
            'purchase_date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        } 