from django import forms
from .models import Product


class ListProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['product_shop', 'is_product_live', 'is_product_verified']
