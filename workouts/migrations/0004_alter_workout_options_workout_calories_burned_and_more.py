# Generated by Django 5.1.1 on 2024-11-10 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0003_alter_workout_options_remove_workout_calories_burned_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workout',
            options={},
        ),
        migrations.AddField(
            model_name='workout',
            name='calories_burned',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='workout',
            name='date',
            field=models.DateField(),
        ),
    ]
