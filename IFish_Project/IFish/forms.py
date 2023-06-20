from django import forms
from .models import ShippingInfo, Product


class ShippingInfoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ShippingInfoForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            print(field)
            field.field.widget.attrs['class'] = "form-control"

    class Meta:
        model = ShippingInfo
        exclude = ("user",)


class ProductForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            print(field)
            field.field.widget.attrs['class'] = "form-control"

    class Meta:
        model = Product
        fields = '__all__'
