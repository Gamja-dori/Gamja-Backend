# Generated by Django 5.0.2 on 2024-06-14 16:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0010_alter_career_company_name_alter_career_job_name_and_more'),
        ('suggest', '0026_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggest',
            name='resume',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.CASCADE, to='resume.resume'),
        ),
    ]
