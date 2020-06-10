from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

class ProductoTagManager(models.Manager):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)

class ProductoTag(models.Model):
    nombre = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48)
    descripcion =  models.TextField('Descripción',blank=True)
    activo = models.BooleanField(default=True)
    objects = ProductoTagManager()

    class Meta:
        verbose_name_plural=('Tag de Productos')

    def __str__(self):
        return self.nombre

    def natural_key(self):
        return (self.slug,)


class ProductosActivos(models.Manager):
    def activo(self):
        return self.filter(activo=True)

class Producto(models.Model):
    nombre = models.CharField('Nombre',max_length=60)
    tags = models.ManyToManyField('ProductoTag', blank=True)
    descripcion =  models.TextField('Descripción',blank=True)
    precio = models.DecimalField('Precio',max_digits=6,decimal_places=2)
    slug = models.SlugField(max_length=48)
    activo = models.BooleanField(default=True)
    en_stock = models.BooleanField(default=True)
    actualizacion = models.DateTimeField('Ultima Actualización',auto_now=True)
    #objects = ProductosActivos()


    class Meta:
        verbose_name_plural=('Productos')

    def __str__(self):
        return self.nombre


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


#User model configuration
class UserManager(BaseUserManager):

    def create_user(self,email,password=None):
        if not email:
            raise ValueError('El correo electrónico no puede dejarse en blanco.')

        email= self.normalize_email(email)
        user = self.model(email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password):
        user = self.create_user(
                    email=email,
                    password=password)

        user.is_staff = True
        user.is_admin = True
        user.is_superuser= True
        user.save(using=self._db)
        return user

class Usuario(AbstractBaseUser,PermissionsMixin):
        email   =  models.EmailField(max_length=60,unique=True)
        nombre = models.CharField(max_length=100,blank=True)
        apellido = models.CharField(max_length=100,blank=True)


        USERNAME_FIELD  = 'email'
        REQUIRED_FIELDS = []

        objects = UserManager()

        date_joined  =  models.DateTimeField(verbose_name="Fecha de ingreso",auto_now_add=True)
        last_login   =  models.DateTimeField(verbose_name="Ultima fecha de Sesión",auto_now=True)
        is_admin     =  models.BooleanField(verbose_name="¿Es Administrador?",default=False)
        is_active    =  models.BooleanField(verbose_name="¿Esta Acivo?",default=True)
        is_staff     =  models.BooleanField(verbose_name="¿Es parte del Staff?",default=False)
        is_superuser =  models.BooleanField(verbose_name="¿Es Super Usuario?",default=False)

        def  __str__(self):
            return f'{self.nombre}'

        def has_perm(self,perm,obj=None):
            return self.is_admin


        def has_module_perms(self,app_label):
            return True

class Direccion(models.Model):

    PAISES_SOPORTADOS = (
       ('mx','Mexico'),
       ('eu','EUA')
    )

    usuario = models.ForeignKey('Usuario',related_name="direcciones",on_delete=models.CASCADE)
    nombre = models.CharField(max_length=60)
    direccion1 = models.CharField('Dirección Linea 1',max_length=60)
    direccion2 = models.CharField('Dirección Linea 2',max_length=60,blank=True)
    codigo_postal = models.CharField('ZIP / Código Postal',max_length=12)
    ciudad = models.CharField(max_length=60)
    pais = models.CharField(max_length=3,choices=PAISES_SOPORTADOS)

    class Meta:
        verbose_name_plural = ('Direcciones')

    def __str__(self):
        return  ",".join(
        [     self.nombre,
              self.direccion1,
              self.direccion2,
              self.codigo_postal,
              self.ciudad,
              self.pais,
          ])
