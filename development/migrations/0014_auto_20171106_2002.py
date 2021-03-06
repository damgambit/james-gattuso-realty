# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-06 20:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('development', '0013_auto_20171031_2157'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='baystateauction',
            options={'ordering': ('id',)},
        ),
        migrations.AlterModelOptions(
            name='townauction',
            options={'ordering': ('id',)},
        ),
        migrations.RenameField(
            model_name='pesco',
            old_name='title',
            new_name='status',
        ),
        migrations.AddField(
            model_name='commonwealthauction',
            name='city',
            field=models.CharField(default='NULL', max_length=20),
        ),
        migrations.AlterField(
            model_name='baystateauction',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 6, 20, 2, 40, 74509, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='commonwealthauction',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='commonwealthauction',
            name='zipcode',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='harkinrealestate',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 6, 20, 2, 40, 77170, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='harkinrealestate',
            name='zipcode',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='landmarkauction',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 6, 20, 2, 40, 72897, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='patriotauctioneer',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 6, 20, 2, 40, 82620, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pesco',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 6, 20, 2, 40, 78436, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='pesco',
            name='terms',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='pesco',
            name='zipcode',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sullivanauctioneers',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 6, 20, 2, 40, 82041, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tacheauctionandsales',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 6, 20, 2, 40, 81104, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='tacheauctionandsales',
            name='zipcode',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='townauction',
            name='date',
            field=models.DateField(default=datetime.datetime(2017, 11, 6, 20, 2, 40, 79944, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='townauction',
            name='zipcode',
            field=models.IntegerField(default=0),
        ),
    ]
