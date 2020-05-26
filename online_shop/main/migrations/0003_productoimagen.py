# Generated by Django 3.0.6 on 2020-05-25 21:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_productotag'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductoImagen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ImageField(upload_to='imagenes-del-producto')),
                ('thumbnail', models.ImageField(null=True, upload_to='producto-thumbnail')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='imagenes', to='main.Producto')),
            ],
        ),
    ]
