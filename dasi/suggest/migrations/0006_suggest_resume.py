# Generated by Django 5.0.2 on 2024-05-21 10:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0010_alter_career_company_name_alter_career_job_name_and_more'),
        ('suggest', '0005_suggest_commute_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggest',
            name='resume',
            field=models.ForeignKey(default=-1, on_delete=django.db.models.deletion.SET_DEFAULT, to='resume.resume'),
        ),
    ]
