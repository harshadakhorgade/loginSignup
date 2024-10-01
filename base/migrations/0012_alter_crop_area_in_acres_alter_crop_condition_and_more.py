# Generated by Django 4.2.15 on 2024-09-03 11:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0011_remove_crop_profile_crop_area_in_acres_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crop',
            name='area_in_acres',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=5),
        ),
        migrations.AlterField(
            model_name='crop',
            name='condition',
            field=models.CharField(default=1, max_length=100),
        ),
        migrations.AlterField(
            model_name='crop',
            name='fertilizer_usage',
            field=models.TextField(default=1),
        ),
        migrations.AlterField(
            model_name='crop',
            name='irrigation_type',
            field=models.CharField(choices=[('Drip', 'Drip'), ('Sprinkle', 'Sprinkle'), ('Pump', 'Pump')], default=1, max_length=50),
        ),
        migrations.AlterField(
            model_name='crop',
            name='photo_or_information',
            field=models.TextField(blank=True, default=1, null=True),
        ),
        migrations.AlterField(
            model_name='crop',
            name='problems',
            field=models.TextField(default=1),
        ),
        migrations.AlterField(
            model_name='crop',
            name='season',
            field=models.CharField(choices=[('Rabi', 'Rabi'), ('Kharif', 'Kharif')], default=1, max_length=50),
        ),
        migrations.AlterField(
            model_name='crop',
            name='username',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
