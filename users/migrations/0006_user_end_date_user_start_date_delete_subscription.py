# Generated by Django 5.1.1 on 2024-11-10 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_alter_subscription_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Subscription',
        ),
    ]