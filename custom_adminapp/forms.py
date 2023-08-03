from custom_adminapp.models import Variant,VariantImage
from django import forms



class VariantForm(forms.ModelForm):
    

    class Meta:
        model = Variant
        exclude = ('product',)

class VariantImageForm(forms.ModelForm):
    class Meta:
        model = VariantImage
        exclude = ('variant',)


