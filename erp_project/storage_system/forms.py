from django import forms

from .models import Customer, Product


class CustomForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('username', 'cellphone', 'wechat', 'birthday', 'address', 'user_info')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'price', 'image', 'status', 'category', 'storage', 'info')