# Generated by Django 5.0.2 on 2024-02-29 07:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recommend', '0001_initial'),
        ('resume', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendedresume',
            name='resume_id',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='resume.resume'),
        ),
    ]
