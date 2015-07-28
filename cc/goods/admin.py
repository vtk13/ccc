from django.contrib import admin
from .models import Unit, Shop, Good, GoodImage, Cost

# Register your models here.

admin.site.register(Unit)
admin.site.register(Shop)


class GoodImageInline(admin.StackedInline):
    model = GoodImage
    extra = 3


class GoodAdmin(admin.ModelAdmin):
    inlines = [GoodImageInline]

admin.site.register(Good, GoodAdmin)

admin.site.register(GoodImage)
admin.site.register(Cost)
