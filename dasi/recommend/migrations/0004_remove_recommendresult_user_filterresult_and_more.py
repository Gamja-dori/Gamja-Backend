# Generated by Django 5.0.2 on 2024-04-09 13:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0003_initial'),
        ('users', '0004_alter_senioruser_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendresult',
            name='user',
        ),
        migrations.CreateModel(
            name='FilterResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_group', models.CharField(blank=True, default='', max_length=20)),
                ('job_role', models.CharField(blank=True, default='', max_length=20)),
                ('min_career_year', models.IntegerField(default=0)),
                ('max_career_year', models.IntegerField(default=0)),
                ('skills', models.TextField(blank=True, default='[]', null=True)),
                ('min_month_pay', models.IntegerField(default=0)),
                ('max_month_pay', models.IntegerField(default=1000)),
                ('commute_type', models.CharField(blank=True, default='', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.enterpriseuser')),
            ],
            options={
                'db_table': 'filter_results',
            },
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('query', models.CharField(max_length=255)),
                ('job_group', models.CharField(blank=True, default='', max_length=20)),
                ('job_role', models.CharField(blank=True, default='', max_length=20)),
                ('min_career_year', models.IntegerField(default=0)),
                ('max_career_year', models.IntegerField(default=0)),
                ('skills', models.TextField(blank=True, default='[]', null=True)),
                ('min_month_pay', models.IntegerField(default=0)),
                ('max_month_pay', models.IntegerField(default=1000)),
                ('commute_type', models.CharField(blank=True, default='', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.enterpriseuser')),
            ],
            options={
                'db_table': 'search_results',
            },
        ),
        migrations.DeleteModel(
            name='RecommendedResume',
        ),
        migrations.DeleteModel(
            name='RecommendResult',
        ),
    ]
