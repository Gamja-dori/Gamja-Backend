# Generated by Django 5.0.2 on 2024-05-21 11:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('suggest', '0006_suggest_resume'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suggest',
            name='enterprise',
        ),
        migrations.RemoveField(
            model_name='suggest',
            name='resume',
        ),
        migrations.RemoveField(
            model_name='suggest',
            name='senior',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
        migrations.DeleteModel(
            name='Suggest',
        ),
    ]