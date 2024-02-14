# Generated by Django 4.0.10 on 2023-12-14 23:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_customuser_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_banner',
            field=models.ImageField(default=django.utils.timezone.now, upload_to=''),
            preserve_default=False,
        ),
    ]