# Generated by Django 4.2.6 on 2023-11-30 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('administradorApp', '0002_pedido_detallepedido'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='productos',
            field=models.ManyToManyField(related_name='pedidos', through='administradorApp.DetallePedido', to='administradorApp.producto'),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='detalles', to='administradorApp.pedido'),
        ),
        migrations.AlterField(
            model_name='detallepedido',
            name='producto',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='detalles', to='administradorApp.producto'),
        ),
    ]