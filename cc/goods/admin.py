from django.contrib import admin
from .models import Unit, Shop, Good, Cost

# Register your models here.

admin.site.register(Unit)
admin.site.register(Shop)
admin.site.register(Good)
admin.site.register(Cost)
