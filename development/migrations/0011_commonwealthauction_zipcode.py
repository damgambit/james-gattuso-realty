# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-29 11:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('development', '0010_auto_20171029_1054'),
    ]

    operations = [
        migrations.AddField(
            model_name='commonwealthauction',
            name='zipcode',
            field=models.IntegerField(default=0),
        ),
    ]