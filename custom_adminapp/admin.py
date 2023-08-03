from django.contrib import admin
from .models import Brand,Category,Product,VariantImage, Variant



# Register your models here.



admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(VariantImage)
admin.site.register(Variant)



