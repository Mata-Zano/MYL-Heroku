# Generated by Django 4.2.6 on 2023-12-15 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administradorApp', '0012_alter_cuenta_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='cuenta',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]