# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-06 17:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('development', '0004_auto_20171006_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='baystateauction',
            name='address',
            field=models.TextField(default='NULL'),
        ),
        migrations.AlterField(
            model_name='baystateauction',
            name='city',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='baystateauction',
            name='date',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='baystateauction',
            name='day',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='baystateauction',
            name='deposit',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='baystateauction',
            name='state',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='baystateauction',
            name='status',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='baystateauction',
            name='time',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='commonwealthauction',
            name='address',
            field=models.TextField(default='NULL'),
        ),
        migrations.AlterField(
            model_name='harkinrealestate',
            name='address',
            field=models.TextField(default='NULL'),
        ),
        migrations.AlterField(
            model_name='harkinrealestate',
            name='city',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='harkinrealestate',
            name='date',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='harkinrealestate',
            name='deposit',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='harkinrealestate',
            name='state',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='harkinrealestate',
            name='status',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='harkinrealestate',
            name='time',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='harkinrealestate',
            name='zipcode',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='landmarkauction',
            name='auction_date',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='patriotauctioneer',
            name='address',
            field=models.TextField(default='NULL'),
        ),
        migrations.AlterField(
            model_name='patriotauctioneer',
            name='city',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='patriotauctioneer',
            name='date',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='patriotauctioneer',
            name='state',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='patriotauctioneer',
            name='status',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='patriotauctioneer',
            name='terms',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='patriotauctioneer',
            name='time',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='patriotauctioneer',
            name='zipcode',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='pesco',
            name='address',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='pesco',
            name='city',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='pesco',
            name='date',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='pesco',
            name='state',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='pesco',
            name='terms',
            field=models.TextField(default='NULL'),
        ),
        migrations.AlterField(
            model_name='pesco',
            name='time',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='pesco',
            name='title',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='pesco',
            name='zipcode',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='sullivanauctioneers',
            name='address',
            field=models.TextField(default='NULL'),
        ),
        migrations.AlterField(
            model_name='sullivanauctioneers',
            name='date',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='sullivanauctioneers',
            name='status',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='sullivanauctioneers',
            name='terms',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='sullivanauctioneers',
            name='url',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='tacheauctionandsales',
            name='address',
            field=models.TextField(default='NULL'),
        ),
        migrations.AlterField(
            model_name='tacheauctionandsales',
            name='auction_date',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='tacheauctionandsales',
            name='city',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='tacheauctionandsales',
            name='deposit',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='tacheauctionandsales',
            name='state',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='tacheauctionandsales',
            name='status',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='tacheauctionandsales',
            name='time',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='tacheauctionandsales',
            name='zipcode',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='townauction',
            name='address',
            field=models.TextField(default='NULL'),
        ),
        migrations.AlterField(
            model_name='townauction',
            name='auction_date',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='townauction',
            name='city',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='townauction',
            name='country',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='townauction',
            name='deposit',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='townauction',
            name='state',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='townauction',
            name='status',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='townauction',
            name='time',
            field=models.CharField(default='NULL', max_length=100),
        ),
        migrations.AlterField(
            model_name='townauction',
            name='zipcode',
            field=models.IntegerField(default=0),
        ),
    ]
