# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-27 19:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('development', '0007_auto_20171026_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='baystateauction',
            name='message',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='commonwealthauction',
            name='message',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='harkinrealestate',
            name='message',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='landmarkauction',
            name='message',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='patriotauctioneer',
            name='message',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='pesco',
            name='message',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='sullivanauctioneers',
            name='message',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='tacheauctionandsales',
            name='message',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='townauction',
            name='message',
            field=models.TextField(default=''),
        ),
    ]
