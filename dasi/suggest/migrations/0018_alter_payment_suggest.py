# Generated by Django 5.0.2 on 2024-05-22 17:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggest', '0017_alter_payment_suggest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='suggest',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='suggest.suggest'),
        ),
    ]
