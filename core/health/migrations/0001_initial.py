# Generated by Django 3.2.14 on 2023-02-06 22:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('md_fullname', models.CharField(blank=True, max_length=200, null=True)),
                ('md_specialize', models.CharField(blank=True, max_length=100, null=True)),
                ('md_contactphone', models.CharField(blank=True, max_length=20, null=True)),
                ('md_mail', models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vacuna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vax_name', models.CharField(blank=True, max_length=50, null=True)),
                ('vax_desc', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('place', models.CharField(blank=True, max_length=500, null=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='health.doctor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Receta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prescription', models.CharField(blank=True, max_length=100, null=True)),
                ('prescription_img', models.ImageField(upload_to='recetas_pics')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Health',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('height', models.FloatField()),
                ('weight', models.FloatField()),
                ('sedentary_work', models.CharField(blank=True, choices=[('si', 'Sí'), ('no', 'No')], max_length=3, null=True)),
                ('smoker', models.CharField(blank=True, choices=[('si', 'Sí'), ('no', 'No')], max_length=3, null=True)),
                ('insurance', models.CharField(blank=True, max_length=100, null=True)),
                ('blood_type', models.CharField(blank=True, max_length=5, null=True)),
                ('main_md', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='health.doctor')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Enf_Preexistentes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('user', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
