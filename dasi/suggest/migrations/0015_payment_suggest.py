# Generated by Django 5.0.2 on 2024-05-22 17:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggest', '0014_rename_status_suggest_progress'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='suggest',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.SET_DEFAULT, to='suggest.suggest'),
        ),
    ]