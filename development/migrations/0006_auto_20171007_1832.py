# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-07 18:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('development', '0005_auto_20171006_1700'),
    ]

    operations = [
        migrations.RenameField(
            model_name='commonwealthauction',
            old_name='auction_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='commonwealthauction',
            old_name='auction_time',
            new_name='time',
        ),
        migrations.RenameField(
            model_name='landmarkauction',
            old_name='auction_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='tacheauctionandsales',
            old_name='auction_date',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='townauction',
            old_name='auction_date',
            new_name='date',
        ),
    ]
