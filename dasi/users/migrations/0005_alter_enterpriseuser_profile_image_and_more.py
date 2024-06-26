# Generated by Django 5.0.2 on 2024-04-09 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_senioruser_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enterpriseuser',
            name='profile_image',
            field=models.ImageField(blank=True, default='', upload_to='profile/enterprise'),
        ),
        migrations.AlterField(
            model_name='senioruser',
            name='profile_image',
            field=models.ImageField(blank=True, default='', upload_to='profile/senior'),
        ),
    ]
