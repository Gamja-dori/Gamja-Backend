# Generated by Django 5.0.2 on 2024-05-19 00:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommend', '0004_remove_recommendresult_user_filterresult_and_more'),
        ('users', '0008_remove_enterpriseuser_profile_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='searchresult',
            name='user',
        ),
        migrations.CreateModel(
            name='SearchHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('query', models.CharField(default='', max_length=255)),
                ('job_group', models.CharField(blank=True, default='', max_length=20)),
                ('job_role', models.CharField(blank=True, default='', max_length=20)),
                ('min_career_year', models.IntegerField(default=0)),
                ('max_career_year', models.IntegerField(default=0)),
                ('skills', models.TextField(blank=True, default='[]', null=True)),
                ('duration_start', models.IntegerField(default=0)),
                ('duration_end', models.IntegerField(default=12)),
                ('min_month_pay', models.IntegerField(default=0)),
                ('max_month_pay', models.IntegerField(default=1000)),
                ('commute_type', models.CharField(blank=True, default='', max_length=20)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.enterpriseuser')),
            ],
            options={
                'db_table': 'search_historys',
            },
        ),
        migrations.DeleteModel(
            name='FilterResult',
        ),
        migrations.DeleteModel(
            name='SearchResult',
        ),
    ]
