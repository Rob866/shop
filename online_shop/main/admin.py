from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.Producto)
admin.site.register(models.ProductoImagen)
admin.site.register(models.ProductoTag)
