# Generated by Django 5.0.4 on 2024-04-29 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="body_fat",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="user",
            name="weight",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
