# Generated by Django 3.0.6 on 2020-05-25 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=60, verbose_name='Nombre')),
                ('descripcion', models.TextField(blank=True, verbose_name='Descripción')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Precio')),
                ('slug', models.SlugField(max_length=48)),
                ('activo', models.BooleanField(default=True)),
                ('en_stock', models.BooleanField(default=True)),
                ('actualizacion', models.DateTimeField(auto_now=True, verbose_name='Ultima Actualización')),
            ],
            options={
                'verbose_name_plural': 'Productos',
            },
        ),
    ]
