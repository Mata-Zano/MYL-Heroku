# Generated by Django 4.2.6 on 2023-12-05 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administradorApp', '0005_usuarios_ciudad_usuarios_comuna_usuarios_direccion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='estado',
            field=models.CharField(choices=[('enProceso', 'En proceso'), ('enviado', 'Enviado'), ('cancelado', 'Cancelado'), ('entregado', 'Entregado')], default='enProceso', max_length=50),
        ),
    ]