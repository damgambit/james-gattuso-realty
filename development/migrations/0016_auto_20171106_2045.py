# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-06 20:45
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('development', '0015_auto_20171106_2004'),
    ]

    operations = [

        migrations.AlterField(
            model_name='baystateauction',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 6, 20, 45, 24, 843560, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='harkinrealestate',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 6, 20, 45, 24, 847302, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='landmarkauction',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 6, 20, 45, 24, 837906, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='patriotauctioneer',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 6, 20, 45, 24, 855135, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pesco',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 6, 20, 45, 24, 849162, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sullivanauctioneers',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 6, 20, 45, 24, 854156, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tacheauctionandsales',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 6, 20, 45, 24, 852836, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='townauction',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 6, 20, 45, 24, 851331, tzinfo=utc)),
        ),
    ]
