# Generated by Django 5.0.2 on 2024-05-20 01:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggest', '0003_suggest_is_cancelled'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggest',
            name='is_read',
            field=models.BooleanField(default=False),
        ),
    ]
