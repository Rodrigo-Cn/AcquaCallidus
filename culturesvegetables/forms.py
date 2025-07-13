from django import forms
from .models import CultureVegetable

class CultureVegetableForm(forms.ModelForm):
    class Meta:
        model = CultureVegetable
        fields = [
            'name',
            'phase_initial_kc',
            'phase_vegetative_kc',
            'phase_flowering_kc',
            'phase_fruiting_kc',
            'phase_maturation_kc',
        ]
        labels = {
            'name': 'Nome',
            'phase_initial_kc': 'KC Germinação',
            'phase_vegetative_kc': 'KC Vegetativo',
            'phase_flowering_kc': 'KC Florescimento',
            'phase_fruiting_kc': 'KC Frutificação',
            'phase_maturation_kc': 'KC Maturação',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'name',
                'placeholder': 'Banana...',
                'required': True,
                'class': 'bg-white border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5'
            }),
            'phase_initial_kc': forms.NumberInput(attrs={
                'id': 'phase_initial_kc',
                'placeholder': 'Ex: 0.75000',
                'step': '0.00001',
                'required': True,
                'class': 'bg-white border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5'
            }),
            'phase_vegetative_kc': forms.NumberInput(attrs={
                'id': 'phase_vegetative_kc',
                'placeholder': 'Ex: 0.85000',
                'step': '0.00001',
                'required': True,
                'class': 'bg-white border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5'
            }),
            'phase_flowering_kc': forms.NumberInput(attrs={
                'id': 'phase_flowering_kc',
                'placeholder': 'Ex: 0.95000',
                'step': '0.00001',
                'required': True,
                'class': 'bg-white border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5'
            }),
            'phase_fruiting_kc': forms.NumberInput(attrs={
                'id': 'phase_fruiting_kc',
                'placeholder': 'Ex: 1.10000',
                'step': '0.00001',
                'required': True,
                'class': 'bg-white border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5'
            }),
            'phase_maturation_kc': forms.NumberInput(attrs={
                'id': 'phase_maturation_kc',
                'placeholder': 'Ex: 0.90000',
                'step': '0.00001',
                'required': True,
                'class': 'bg-white border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5'
            }),
        }
