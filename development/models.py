# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from uuid import uuid5, NAMESPACE_URL
import datetime
from django.utils import timezone


# Create your models here.

# Confirmation Model for Authentication of User with bycrypt sha256 Hashing

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     email_confirmed = models.BooleanField(default=False)
#
#
# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#     instance.profile.save()

# Land Mark Auction Model with all columns according to Scripts

class LandMarkAuction(models.Model):
    date = models.DateField(default=timezone.now)
    time = models.CharField(max_length=100, default='NULL')
    status = models.CharField(max_length=100, default='NULL')
    address = models.TextField(default='NULL')
    city = models.CharField(max_length=50, default='NULL')
    state = models.CharField(max_length=50, default='NULL')
    zipcode = models.IntegerField(default=0)
    message = models.TextField(default='')
    message_avail = models.BooleanField(default=False)
    deposit = models.CharField(max_length=20, default='NULL')

    def __str__(self):
        return self.__class__.__name__


class BayStateAuction(models.Model):
    status = models.CharField(max_length=100, default='NULL')
    day = models.CharField(max_length=100, default='NULL')
    date = models.DateField(default=timezone.now)
    time = models.CharField(max_length=100, default='NULL')
    address = models.TextField(default='NULL')
    city = models.CharField(max_length=100, default='NULL')
    state = models.CharField(max_length=100, default='NULL')
    deposit = models.CharField(max_length=100, default='NULL')
    message = models.TextField(default='')
    message_avail = models.BooleanField(default=False)
    zipcode = models.IntegerField(default=0)

    def __str__(self):
        return self.__class__.__name__

    class Meta:
        ordering = ('id',)


class CommonWealthAuction(models.Model):
    status = models.CharField(max_length=100, default='NULL')
    date = models.DateField(default=timezone.now)
    time = models.CharField(max_length=100, default='NULL')
    address = models.TextField(default='NULL')
    state = models.CharField(max_length=20, default='NULL')
    city = models.CharField(max_length=20, default='NULL')
    country = models.CharField(max_length=100, default='NULL')
    deposit = models.CharField(max_length=100, default='NULL')
    message = models.TextField(default='')
    message_avail = models.BooleanField(default=False)
    zipcode = models.IntegerField(default=0)

    def __str__(self):
        return self.__class__.__name__


class HarkinRealEstate(models.Model):
    date = models.DateField(default=timezone.now)
    time = models.CharField(max_length=100, default='NULL')
    status = models.CharField(max_length=100, default='NULL')
    address = models.TextField(default='NULL')
    city = models.CharField(max_length=100, default='NULL')
    state = models.CharField(max_length=100, default='NULL')
    zipcode = models.IntegerField(default=0)
    deposit = models.CharField(max_length=100, default='NULL')
    message = models.TextField(default='')
    message_avail = models.BooleanField(default=False)

    def __str__(self):
        return self.__class__.__name__


class Pesco(models.Model):
    date = models.DateField(default=timezone.now)
    time = models.CharField(max_length=100, default='NULL')
    status = models.CharField(max_length=100, default='NULL')
    address = models.CharField(max_length=100, default='NULL')
    city = models.CharField(max_length=100, default='NULL')
    state = models.CharField(max_length=100, default='NULL')
    zipcode = models.IntegerField(default=0)
    terms = models.TextField(default='')
    message = models.TextField(default='')
    message_avail = models.BooleanField(default=False)

    def __str__(self):
        return self.__class__.__name__


class TownAuction(models.Model):
    date = models.DateField(default=timezone.now)
    time = models.CharField(max_length=100, default='NULL')
    status = models.CharField(max_length=100, default='NULL')
    address = models.TextField(default='NULL')
    city = models.CharField(max_length=100, default='NULL')
    state = models.CharField(max_length=100, default='NULL')
    zipcode = models.IntegerField(default=0)
    country = models.CharField(max_length=100, default='NULL')
    deposit = models.CharField(max_length=100, default='NULL')
    message = models.TextField(default='')
    message_avail = models.BooleanField(default=False)

    class Meta:
        ordering = ('id',)


class TacheAuctionAndSales(models.Model):
    date = models.DateField(default=timezone.now)
    time = models.CharField(max_length=100, default='NULL')
    status = models.CharField(max_length=100, default='NULL')
    address = models.TextField(default='NULL')
    city = models.CharField(max_length=100, default='NULL')
    state = models.CharField(max_length=100, default='NULL')
    zipcode = models.IntegerField(default=0)
    deposit = models.CharField(max_length=100, default='NULL')
    message = models.TextField(default='')
    message_avail = models.BooleanField(default=False)

    def __str__(self):
        return self.__class__.__name__


class SullivanAuctioneers(models.Model):
    url = models.CharField(max_length=100, default='NULL')
    status = models.CharField(max_length=100, default='NULL')
    date = models.DateField(default=timezone.now)
    address = models.TextField(default='NULL')
    terms = models.CharField(max_length=100, default='NULL')
    message = models.TextField(default='')
    message_avail = models.BooleanField(default=False)

    def __str__(self):
        return self.__class__.__name__


class PatriotAuctioneer(models.Model):
    date = models.DateField(default=timezone.now)
    time = models.CharField(max_length=100, default='NULL')
    status = models.CharField(max_length=100, default='NULL')
    address = models.TextField(default='NULL')
    city = models.CharField(max_length=100, default='NULL')
    state = models.CharField(max_length=100, default='NULL')
    zipcode = models.IntegerField(default=0)
    terms = models.CharField(max_length=100, default='NULL')
    message = models.TextField(default='')
    message_avail = models.BooleanField(default=False)

    def __str__(self):
        return self.__class__.__name__


# Contact model for webpage Contact information support

class Contact(models.Model):
    name = models.CharField(max_length=100, blank=False)
    email = models.EmailField()
    subject = models.CharField(max_length=100, default='')
    text = models.TextField(default='')

    def __str__(self):
        return self.name
