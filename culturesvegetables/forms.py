from django import forms
from django.core.exceptions import ValidationError
from .models import CultureVegetable
import re

def validate_single_emoji(value):
    emoji_pattern = re.compile(
        r'^[\U0001F300-\U0001FAFF\U00002600-\U000027BF]$'
    )
    if not emoji_pattern.match(value):
        raise ValidationError("Insira apenas 1 emoji válido.")

COMMON_EMOJI_INPUT_CLASSES = (
    "bg-white border border-gray-300 placeholder-gray-400 text-gray-900 "
    "text-2xl rounded-lg block w-full p-2.5 text-center shadow-sm "
    "focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-sky-500 "
    "transition duration-150 ease-in-out"
)

COMMON_EMOJI_INLINE_STYLES = (
    'font-family: system-ui, "Apple Color Emoji", "Segoe UI Emoji", '
    '"Noto Color Emoji", sans-serif;'
)


class CultureVegetableForm(forms.ModelForm):
    emoji = forms.CharField(
        max_length=10,
        required=True,
        validators=[validate_single_emoji],
        label="Emoji",
        help_text="Escolha um único emoji (ex.: 🌽, 🍌, 🥕).",
        widget=forms.TextInput(attrs={
            "id": "emoji",
            "placeholder": "🌱",
            "required": True,
            "autocomplete": "off",
            "spellcheck": "false",
            "autocapitalize": "none",
            "inputmode": "text",
            "maxlength": "10",
            "aria-label": "Emoji da cultura",
            "title": "Digite apenas 1 emoji",
            "class": COMMON_EMOJI_INPUT_CLASSES,
            "style": COMMON_EMOJI_INLINE_STYLES,
        }),
    )

    class Meta:
        model = CultureVegetable
        fields = [
            'name',
            'emoji',
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


class CultureVegetableEditForm(forms.ModelForm):
    emoji = forms.CharField(
        max_length=10,
        required=True,
        validators=[validate_single_emoji],
        label="Emoji",
        help_text="Escolha um único emoji (ex.: 🌽, 🍌, 🥕).",
        widget=forms.TextInput(attrs={
            "id": "emoji_edit",
            "placeholder": "🌱",
            "required": True,
            "autocomplete": "off",
            "spellcheck": "false",
            "autocapitalize": "none",
            "inputmode": "text",
            "maxlength": "10",
            "aria-label": "Emoji da cultura",
            "title": "Digite apenas 1 emoji",
            "class": COMMON_EMOJI_INPUT_CLASSES + " mb-2",
            "style": COMMON_EMOJI_INLINE_STYLES,
        }),
    )

    class Meta:
        model = CultureVegetable
        fields = [
            'name',
            'emoji',
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
                'id': 'name_edit',
                'placeholder': 'Banana...',
                'required': True,
                'class': 'bg-white border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5 mb-2'
            }),
            'phase_initial_kc': forms.NumberInput(attrs={
                'id': 'phase_initial_kc_edit',
                'placeholder': 'Ex: 0.75000',
                'step': '0.00001',
                'required': True,
                'class': 'bg-white border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5 mb-2'
            }),
            'phase_vegetative_kc': forms.NumberInput(attrs={
                'id': 'phase_vegetative_kc_edit',
                'placeholder': 'Ex: 0.85000',
                'step': '0.00001',
                'required': True,
                'class': 'bg-white border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5 mb-2'
            }),
            'phase_flowering_kc': forms.NumberInput(attrs={
                'id': 'phase_flowering_kc_edit',
                'placeholder': 'Ex: 0.95000',
                'step': '0.00001',
                'required': True,
                'class': 'bg-white border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5 mb-2'
            }),
            'phase_fruiting_kc': forms.NumberInput(attrs={
                'id': 'phase_fruiting_kc_edit',
                'placeholder': 'Ex: 1.10000',
                'step': '0.00001',
                'required': True,
                'class': 'bg-white border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5 mb-2'
            }),
            'phase_maturation_kc': forms.NumberInput(attrs={
                'id': 'phase_maturation_kc_edit',
                'placeholder': 'Ex: 0.90000',
                'step': '0.00001',
                'required': True,
                'class': 'bg-white border border-gray-300 text-gray-900 text-sm rounded-lg block w-full p-2.5 mb-4'
            }),
        }
