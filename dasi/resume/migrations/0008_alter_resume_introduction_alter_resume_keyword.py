# Generated by Django 5.0.2 on 2024-04-13 22:32

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("resume", "0007_alter_resume_career_year_alter_resume_commute_type_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="resume",
            name="introduction",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="resume",
            name="keyword",
            field=models.TextField(blank=True, default="", null=True),
        ),
    ]
