# products/forms.py

from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'origin', 'price', 'image']  # Các trường để đăng sản phẩm
