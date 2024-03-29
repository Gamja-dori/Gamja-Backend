# Generated by Django 5.0.2 on 2024-03-04 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RecommendedResume',
            fields=[
                ('recommended_resume_id', models.AutoField(primary_key=True, serialize=False)),
                ('percentage', models.IntegerField()),
                ('comment', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'recommended_resumes',
            },
        ),
        migrations.CreateModel(
            name='RecommendResult',
            fields=[
                ('recommend_id', models.AutoField(primary_key=True, serialize=False)),
                ('query', models.CharField(max_length=255)),
            ],
            options={
                'db_table': 'recommend_results',
            },
        ),
    ]
