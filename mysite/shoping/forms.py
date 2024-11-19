from unicodedata import category

from django import forms
from .models import Category, Product
from django.contrib.auth.models import User


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class CsvPriceSearchForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label="Kategorija",
        widget=forms.Select(attrs={"id": "category-select"})
    )
    product = forms.ModelChoiceField(
        queryset=Product.objects.none(),  # Inicialiai nėra jokių produktų
        required=True,
        label="Produktas",
        widget=forms.Select(attrs={"id": "product-select"})
    )
