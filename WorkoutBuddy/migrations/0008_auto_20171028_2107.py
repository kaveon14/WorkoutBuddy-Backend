# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-28 21:07
from __future__ import unicode_literals

import WorkoutBuddy.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WorkoutBuddy', '0007_progressphoto_user_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customexerciseimage',
            name='exercise_image',
            field=models.ImageField(max_length=500, null=True, upload_to=WorkoutBuddy.models.user_directory_exercise_image_path),
        ),
        migrations.AlterField(
            model_name='customexerciseimage',
            name='local_exercise_image',
            field=models.ImageField(max_length=500, null=True, upload_to=''),
        ),
    ]
