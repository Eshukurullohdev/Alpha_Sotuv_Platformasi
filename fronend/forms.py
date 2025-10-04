from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "img", "narx", "type", "tavsif"]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Product name"}),
            "narx": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Price"}),
            "type": forms.Select(attrs={"class": "form-select"}),
            "tavsif": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Description"}),
        }
