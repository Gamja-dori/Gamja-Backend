# Generated by Django 5.0.2 on 2024-02-29 07:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('recommend', '0002_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recommendresult',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.enterpriseuser'),
        ),
        migrations.AddField(
            model_name='recommendedresume',
            name='recommend_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommend.recommendresult'),
        ),
    ]
