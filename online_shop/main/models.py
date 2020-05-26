from django.db import models

class ProductosActivos(models.Manager):
    def get_queryset(self):
        return  super(ProductosActivos,self).get_queryset().filter(activo=True)

class Producto(models.Model):
    nombre = models.CharField('Nombre',max_length=60)
    descripcion =  models.TextField('Descripción',blank=True)
    precio = models.DecimalField('Precio',max_digits=6,decimal_places=2)
    slug = models.SlugField(max_length=48)
    activo = models.BooleanField(default=True)
    en_stock = models.BooleanField(default=True)
    actualizacion = models.DateTimeField('Ultima Actualización',auto_now=True)


    class Meta:
        verbose_name_plural=('Productos')

    def __str__(self):
        return self.nombre
    objects = ProductosActivos()


class ProductoImagen(models.Model):
    producto = models.ForeignKey(
                Producto,
                on_delete= models.CASCADE,
                related_name="imagenes")

    imagen = models.ImageField(upload_to='imagenes-del-producto')
    thumbnail =  models.ImageField(upload_to='producto-thumbnails',null=True,blank=True)
    class Meta:
        verbose_name = ('Imagen de Producto')
        verbose_name_plural=('Imagenes de Productos')


class ProductoTag(models.Model):
    productos = models.ManyToManyField(Producto,blank=True)
    nombre = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48)
    descripcion =  models.TextField('Descripción',blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural=('Tag de Productos')

    def __str__(self):
        return self.nombre
