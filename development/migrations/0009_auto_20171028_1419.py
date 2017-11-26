# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-28 14:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('development', '0008_auto_20171027_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='baystateauction',
            name='message_avail',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='commonwealthauction',
            name='message_avail',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='harkinrealestate',
            name='message_avail',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='landmarkauction',
            name='message_avail',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='patriotauctioneer',
            name='message_avail',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='pesco',
            name='message_avail',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sullivanauctioneers',
            name='message_avail',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='tacheauctionandsales',
            name='message_avail',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='townauction',
            name='message_avail',
            field=models.BooleanField(default=False),
        ),
    ]