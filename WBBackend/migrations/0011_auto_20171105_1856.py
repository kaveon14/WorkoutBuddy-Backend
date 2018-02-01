# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-11-05 18:56
from __future__ import unicode_literals

import WBBackend.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WBBackend', '0010_auto_20171105_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profileimage',
            name='local_profile_image',
            field=models.ImageField(max_length=2000, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='progressphoto',
            name='local_photo',
            field=models.ImageField(max_length=2000, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='progressphoto',
            name='photo',
            field=models.ImageField(max_length=500, upload_to=WBBackend.models.user_directory_progress_photo__path),
        ),
    ]