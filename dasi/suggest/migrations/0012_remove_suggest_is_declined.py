# Generated by Django 5.0.2 on 2024-05-21 22:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('suggest', '0011_alter_payment_tid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suggest',
            name='is_declined',
        ),
    ]
