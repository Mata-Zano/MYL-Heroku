# Generated by Django 4.2.6 on 2023-12-07 04:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administradorApp', '0008_pedido_carrito'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pedido',
            name='carrito',
        ),
        migrations.AddField(
            model_name='usuarios',
            name='carrito',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
    ]
