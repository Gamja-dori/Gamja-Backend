# Generated by Django 5.0.2 on 2024-05-22 21:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('suggest', '0025_delete_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=100)),
                ('total_amount', models.IntegerField()),
                ('aid', models.CharField(default='', max_length=20)),
                ('tid', models.CharField(default='', max_length=20)),
                ('payment_method_type', models.CharField(default='', max_length=10)),
                ('card_info', models.TextField(blank=True, default='', null=True)),
                ('amount_info', models.TextField(blank=True, default='', null=True)),
                ('created_at', models.CharField(default='', max_length=20)),
                ('approved_at', models.CharField(default='', max_length=20)),
                ('suggest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='suggest.suggest')),
            ],
            options={
                'db_table': 'payments',
            },
        ),
    ]
