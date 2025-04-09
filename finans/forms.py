from django import forms
from .models import AccountCategory

class AccountCategoryForm(forms.ModelForm):
    class Meta:
        model = AccountCategory
        fields = ['name', 'category_type', 'description', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        } 