# Generated by Django 5.0.2 on 2024-05-19 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggest', '0002_rename_duraton_suggest_duration_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggest',
            name='is_cancelled',
            field=models.BooleanField(default=False),
        ),
    ]
