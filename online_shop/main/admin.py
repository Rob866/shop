from django.contrib import admin
from .models import Producto,ProductoTag,ProductoImagen,Direccion,Basket,BasketLine
from django.utils.html import format_html
from main import models
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm,ReadOnlyPasswordHashField

class ProductoAdmin(admin.ModelAdmin):

    list_display = ('nombre','slug','en_stock','precio',)
    list_filter = ('activo','en_stock','actualizacion',)
    list_editable = ('en_stock',)
    prepopulated_fields = {"slug": ("nombre",)}
    autocomplete_fields = ('tags',)
    search_fields = ('nombre',)

class ProductoImagenAdmin(admin.ModelAdmin):
    list_display = ('thumbnail_tag','producto_nombre',)
    readonly_fields = ('thumbnail',)
    search_fields = ('product__nombre',)


    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="%s"/>' % obj.thumbnail.url
            )
        return "-"
    thumbnail_tag.short_description = "Thumbnail"

    def producto_nombre(self, obj):
        return obj.producto.nombre


class ProductoTagAdmin(admin.ModelAdmin):

    list_display = ('nombre','descripcion', 'slug')
    list_filter = ('activo',)
    search_fields = ('nombre',)
    prepopulated_fields = {"slug": ("nombre",)}
    #autocomplete_fields = ('productos',)

class CustomUserChangeForm(UserChangeForm):

    password = ReadOnlyPasswordHashField(label= ("Password"),
        help_text= ("Las contraseñas sin procesar no se almacenan, por lo que no hay forma de ver la contraseña de este usuario, "
                    "pero puede cambiar la contraseña mediante este formulario."
                    "<a href=\"../password/\">formulario</a>."))
    class Meta:
        model = models.Usuario
        fields = '__all__'


@admin.register(models.Usuario)
class UserAdmin(DjangoUserAdmin):
    form = CustomUserChangeForm
    fieldsets = (
        ("Credenciales", {"fields": ("email", "password")}),
        (
            "Información Personal",
            {"fields": ("nombre", "apellido")},
        ),
        (
            "Permisos",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                             "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Fechas importantes",
            {"fields": ("last_login", "date_joined")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    list_display = (
        "email",
        "nombre",
        "apellido",
        "is_staff",
    )
    readonly_fields = ['date_joined','last_login',]
    search_fields = ("email", "nombre", "apellido")
    ordering = ("email",)

class DireccionAdmin(admin.ModelAdmin):
    list_display = ('nombre',)

class BasketAdmin(admin.ModelAdmin):
    list_display = ('status',)



admin.site.register(Producto ,ProductoAdmin)
admin.site.register(ProductoImagen,ProductoImagenAdmin)
admin.site.register(ProductoTag,ProductoTagAdmin)
admin.site.register(Direccion,DireccionAdmin)
admin.site.register(Basket,BasketAdmin)
admin.site.register(BasketLine)
