# Generated by Django 5.0.6 on 2024-06-20 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0004_match_referee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerscore',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]