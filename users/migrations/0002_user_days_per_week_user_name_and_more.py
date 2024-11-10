# Generated by Django 5.1.1 on 2024-11-09 22:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='days_per_week',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='subscription_valid_until',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
