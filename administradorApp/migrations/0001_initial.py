# Generated by Django 4.2.6 on 2023-11-14 01:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('alimentoMascotas', 'Alimento de Mascotas'), ('bebestibles', 'Bebestibles'), ('carbon', 'Carbón'), ('abarrotes', 'Abarrotes')], max_length=50)),
                ('descripccion', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correo', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Rol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('administrador', 'Administrador'), ('supervisor', 'Supervisor'), ('cliente', 'Cliente'), ('vendedor', 'Vendedor')], default='Administrador', max_length=50)),
                ('descripcion', models.CharField(max_length=150, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellido', models.CharField(max_length=20)),
                ('telefono', models.CharField(max_length=50)),
                ('cuenta', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='administradorApp.cuenta')),
            ],
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=250)),
                ('stock', models.IntegerField()),
                ('precio', models.FloatField()),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administradorApp.categoria')),
            ],
        ),
        migrations.AddField(
            model_name='cuenta',
            name='rol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='administradorApp.rol'),
        ),
    ]
