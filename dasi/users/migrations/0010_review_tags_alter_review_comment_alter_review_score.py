# Generated by Django 5.0.2 on 2024-05-23 12:46

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0009_enterpriseuser_company"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="tags",
            field=models.TextField(blank=True, default="[]", null=True),
        ),
        migrations.AlterField(
            model_name="review",
            name="comment",
            field=models.TextField(blank=True, default="", null=True),
        ),
        migrations.AlterField(
            model_name="review",
            name="score",
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=1),
        ),
    ]