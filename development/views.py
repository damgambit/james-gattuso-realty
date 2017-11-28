# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponseRedirect, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from development.forms import SignUpForm, LoginForm, ForgetForm, ResetForm, ContactForm, NotesForm, SearchForm
from development.models import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.db.models import Q
from development.tokens import account_activation_token
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from itertools import chain
from drf_multiple_model.views import MultipleModelAPIView
from development.pagination import StandardResultsSetPagination
from rest_framework.renderers import JSONRenderer
from development.serializers import ( BayStateAuctionSerializer,
                                    TownAuctionSerializer,
                                    TimelineSerializer,
                                    PaginatedTimelineSerializer,
                                    LandMarkAuctionSerliazer,
                                     CommonWealthAuctionSerliazer)
import openpyxl
import mimetypes
import os
import time
import pandas as pd
from rest_framework import filters
# from django_filters import rest_framework as filters
from openpyxl.writer.excel import save_virtual_workbook
from openpyxl.styles import Font
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
from operator import attrgetter
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics, mixins
import datetime
from collections import namedtuple

bsa = BayStateAuction.objects.all()
tas = TacheAuctionAndSales.objects.all()
ta = TownAuction.objects.all()
pe = Pesco.objects.all()
lma = LandMarkAuction.objects.all()
hre = HarkinRealEstate.objects.all()
cwa = CommonWealthAuction.objects.all()
d1 = datetime.datetime.strptime('01/01/2001', '%m/%d/%Y')

Timeline = namedtuple('Timeline', ('baystateauction', 'townauction'))

from models import *
import csv


def parcer():
    f = open('./csv_file/towneauction.csv', 'r')
    # Auction Date,Time,Status,Address,City,State,Zip Code,County,Page / Liber,Deposit
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 'Auction Date':
            continue
        c = TownAuction.objects.get_or_create(date=datetime.datetime.strptime(str(row[0]), '%m/%d/%y'),
                                              time=row[1],
                                              status=row[2],
                                              address=row[3],
                                              city=row[4],
                                              state=row[5],
                                              zipcode=row[6],
                                              country=row[7],
                                              deposit=row[9]
                                              )
    f.close()


    f = open('./csv_file/baystateauction.csv', 'r')
    reader = csv.reader(f)
    # Status,Day,Date,Time,Address,City,State,Deposit
    for row in reader:
        if row[0] == 'Status':
            continue
        c = BayStateAuction.objects.get_or_create(date=datetime.datetime.strptime(str(row[2]) + ' 2017', '%B %d %Y'),
                                                  time=row[3],
                                                  status=row[0],
                                                  address=row[4],
                                                  city=row[5],
                                                  state=row[6],
                                                  deposit=row[7]
                                                  )
    f.close()

    f = open('./csv_file/pesco.csv', 'r')
    #Date,Time,Title,Address,City,State,zipcode,Terms
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 'Date':
            continue
        c = Pesco.objects.get_or_create(date=row[0],
                time=row[1],
                status=row[2],
                address=row[3],
                city=row[4],
                state=row[5],
                zipcode=row[6],
                terms=row[7]
            )
    f.close()
    
    f = open('./csv_file/landmarkauction.csv', 'r')
    # Auction Date,Time,Status,Address,City,State,Zip Code
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 'Auction Date':
            continue
        c = LandMarkAuction.objects.get_or_create(date=row[0],
                                                  time=row[1],
                                                  status=row[2],
                                                  address=row[3],
                                                  city=row[4],
                                                  state=row[5],
                                                  zipcode=row[6],
                                                  )
    f.close()



    f = open('./csv_file/commonwealthauction.csv', 'r')
    # status,Auction_Date,Auction_time,Address,County,Deposit
    reader = csv.reader(f)
    for row in reader:
        if row[0] == 'status':
            continue
        c = CommonWealthAuction.objects.get_or_create(
              date=datetime.datetime.strftime(
                  datetime.datetime.strptime(row[1], "%m/%d/%Y"), "%Y-%m-%d"),
              time=row[2],
              status=row[0],
              address=row[3],
              country=row[4],
              deposit=row[5]
                                                      )
    f.close()



# Create your views here.
@login_required(login_url='login')
def index(request):
    context = {
        'name': request.user,
    }
    return render(request, 'index.html', context)


def login_view(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect("/")  # Redirect to a success page.
        else:
            context = {
                'form': form,
                'name': 'Login'
            }
    else:
        context = {
            'form': form,
            'name': "Login"
        }
    # print('parcing')
    # parcer()
    return render(request, 'login.html', context)


def SignUp(request):
    context = {}
    err = False
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():

            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None and user.is_active:
                login(request, user)
                return redirect('/')
            else:
                context = {
                    'form': SignUpForm,
                    'name': 'SignUp'
                }

        else:
            context = {
                'form': SignUpForm,
                'name': 'SignUp',
                'err': True,
                'msg': form.errors
            }
        return render(request, 'register.html', context)
    else:
        form = SignUpForm()
        context = {
            'form': form,
            'name': 'SignUp',
            'has_error': False,
        }
    return render(request, 'register.html', context)


@login_required(login_url='login')
def propertyx(request):
    obj = list(chain(bsa, cwa, tas, ta, pe, lma, hre))
    if request.method == 'POST':
        form = NotesForm(request.POST)
        form_search = SearchForm(request.POST)
        if form.is_valid():
            _id = form.cleaned_data.get('id')
            _cname = form.cleaned_data.get('cname')
            text = form.cleaned_data.get('text')
            if _cname == 'BayStateAuction' and bsa.filter(id=_id).exists():
                mess = bsa.get(id=_id)
            elif _cname == 'CommonWealthAuction' and cwa.filter(id=_id).exists():
                mess = cwa.get(id=_id)
            elif _cname == 'TacheAuctionAndSales' and tas.filter(id=_id).exists():
                mess = tas.get(id=_id)
            elif _cname == 'TownAuction' and ta.filter(id=_id).exists():
                mess = ta.get(id=_id)
            elif _cname == 'Pesco' and pe.filter(id=_id).exists():
                mess = pe.get(id=_id)
            elif _cname == 'LandMarkAuction' and lma.filter(id=_id).exists():
                mess = lma.get(id=_id)
            else:
                mess = hre.get(id=_id)
            mess.message = text
            mess.message_avail = True
            mess.save()
            page = request.GET.get('page')
            paginator = Paginator(obj, 10)
            count = paginator.num_pages
            form = NotesForm()
            form_search = SearchForm()
            try:
                paginator = paginator.page(page)
            except PageNotAnInteger:
                paginator = paginator.page(1)
            except EmptyPage:
                paginator = paginator.page(paginator.num_pages)
            context = {
                'page': paginator,
                'num_page': count,
                'forms': form,
                'form_search': form_search,
                'stat': 'All',
            }
            return render_to_response("table.html", context)
        elif form_search.is_valid():
            search_data = form_search.cleaned_data.get('search_data')
            return redirect('search', search_data=search_data)
    form = NotesForm(None)
    form_search = SearchForm(None)
    page = request.GET.get('page')
    paginator = Paginator(obj, 10)
    count = paginator.num_pages
    try:
        paginator = paginator.page(page)
    except PageNotAnInteger:
        paginator = paginator.page(1)
    except EmptyPage:
        paginator = paginator.page(paginator.num_pages)
    context = {
        'page': paginator,
        'num_page': count,
        'forms': form,
        'form_search': form_search,
        'stat': 'All',
    }
    return render(request, "table.html", context)


def logout_view(request):
    logout(request)
    return redirect('login')


def forget_password(request):
    form = ForgetForm(request.POST or None)
    if form.is_valid():
        user = form.check_user()
        current_site = get_current_site(request)
        subject = "Password Reset Request"
        message = render_to_string('password_reset_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.id)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        msg = "Password Link is Sent to your Email ID: " + user.email
        messages.add_message(request, messages.SUCCESS, msg)
        return HttpResponseRedirect('login')

    else:
        context = {
            'form': form,
            'name': 'Forget Password'
        }
    return render(request, 'forget_password.html', context)


def password_reset_form(request, uid64, token):
    context = {}
    try:
        uid = force_text(urlsafe_base64_decode(uid64))
        user = User.objects.get(id=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = ResetForm(request.POST or None)
            if form.is_valid():
                if form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
                    password1 = form.cleaned_data.get('password1')
                    password2 = form.cleaned_data.get('password2')
                    user.set_password(password2)
                    user.save()
                    # user = authenticate(username=user.username, password=password)
                    msg = "Password Reseted Successfully !!"
                    messages.add_message(request, messages.SUCCESS, msg)
                    return HttpResponseRedirect('login')
                else:
                    return HttpResponseRedirect('/')
            else:
                msg = "Your Link Destroyed try again later !!"
                messages.add_message(request, messages.INFO, msg)
                return redirect('login')
        else:
            form = ResetForm()
            context = {
                'form': form,
                'name': 'Reset Password'
            }
        return render(request, 'password_reset_form.html', context)
    else:
        return redirect('/')


def password_reset_complete(request):
    return render(request, 'password_reset_complete.html', {})


def password_reset_confirm(request):
    return render(request, 'password_reset_sent.html', {})


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = "Username exist!!"
    return JsonResponse(data)


@login_required(login_url='login')
def list_all(request):
    return render(request, 'table.html', {})


@login_required(login_url='login')
def home(request):
    return render(request, 'home.html', {})

@login_required(login_url='login')
def about(request):
    return render(request, 'about.html', {})


def contact(request):
    return render(request, 'contact.html', {})


def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            msg = "Your Form is Submitted we will contact you shortly!!!"
            messages.add_message(request, messages.SUCCESS, msg)
            return HttpResponseRedirect('/contact')
        else:
            msg = "Oppps Some Error in Submission"
            messages.add_message(request, messages.WARNING, msg)
            return HttpResponseRedirect('/contact')
    else:
        form = ContactForm()
        context = {
            'form': form,
        }
    return render(request, 'contact_us.html', context)


def password_validation(request):
    password1 = request.GET.get('password1')
    password2 = request.GET.get('password2')
    data = {}
    if password1 != password2:
        data['error_msg'] = "Password and Confirm Password are not same!!"
        data['error'] = True
    return JsonResponse(data)

@login_required(login_url='login')
def get_all(request, type = 'json'):

    is_active = request.GET.get('active', None)
    is_postponed = request.GET.get('postponed', None)
    is_cancel = request.GET.get('cancel', None)
    date_from = request.GET.get('date_from', None)
    date_to = request.GET.get('date_to', None)

    if is_active == "true":
        is_active = True
    else:
        is_active = False
    if is_postponed == "true":
        is_postponed = True  
    else:  
        is_postponed = False    
    if is_cancel == "true":
        is_cancel = True
    else:
        is_cancel = False
        
    if date_from == '':
        date_from = datetime.datetime(1600, 1, 1, 0, 0).date()
    else: 
        date_from = datetime.datetime.strptime(date_from, '%m/%d/%Y').date()

    if date_to == '':
        date_to = datetime.datetime(2099, 1, 1, 0, 0).date()
    else:
        date_to = datetime.datetime.strptime(date_to, '%m/%d/%Y').date()

    filtering = is_active or is_postponed or is_cancel
    
    print(not filtering)
    print(is_active, is_cancel, is_postponed)

    bsav = []
    tasv = []
    tav = []
    pev = []
    lmav = []
    hrev = []
    cwav = []

    if not filtering:
        print("[*] sending all")

        bsav += list(BayStateAuction.objects.filter(date__range=[date_from, date_to]).values()) 
        tav += list(TownAuction.objects.filter(date__range=[date_from, date_to]).values()) 
        cwav += list(CommonWealthAuction.objects.filter(date__range=[date_from, date_to]).values()) 
        pev += list(Pesco.objects.filter(date__range=[date_from, date_to]).values()) 
        tasv += list(TacheAuctionAndSales.objects.filter(date__range=[date_from, date_to]).values()) 
        lmav += list(LandMarkAuction.objects.filter(date__range=[date_from, date_to]).values())

    if filtering:
        if is_active:
            print("[*] sending active")

            bsav += list(BayStateAuction.objects.filter(status__icontains='Continued', 
                date__range=[date_from, date_to]).values())
            tasv += list(TacheAuctionAndSales.objects.filter(status__icontains='ON TIME',
                date__range=[date_from, date_to]).values())
            tav += list(TownAuction.objects.filter(status__icontains='On_Time', 
                date__range=[date_from, date_to]).values())
            pev += list(Pesco.objects.filter(date__range=[date_from, date_to]).values())
            lmav += list(LandMarkAuction.objects.filter(status__icontains='Currently', 
                date__range=[date_from, date_to]).values()) 
            cwav += list(CommonWealthAuction.objects.filter(status__icontains='3rd Party Purchase', 
                date__range=[date_from, date_to]).values())
        if is_postponed:
            print("[*] sending postponed")
            bsav += list(BayStateAuction.objects.filter(status__icontains='POSTPONED', 
                date__range=[date_from, date_to]).values())
            tasv += list(TacheAuctionAndSales.objects.filter(status__icontains='POSTPONED',
                date__range=[date_from, date_to]).values())
            tav += list(TownAuction.objects.filter(status__icontains='Postponed', 
                date__range=[date_from, date_to]).values())
        if is_cancel:
            print("[*] sending cancel")
            bsav += list(BayStateAuction.objects.filter(status__icontains='Cancel',
                date__range=[date_from, date_to]).values())
            tav += list(TownAuction.objects.filter(status__icontains='Cancel',
                date__range=[date_from, date_to]).values())
        
    
    data = bsav + tasv + tav + pev + lmav + cwav

    df = pd.DataFrame(data)

    active_counter = len(df[df['status'].str.contains("Continued")]) + \
             len(df[df['status'].str.contains("ON TIME")]) + \
             len(df[df['status'].str.contains("On_Time")]) + \
             len(df[df['status'].str.contains("Currently")]) + \
             len(df[df['status'].str.contains("3rd Party Purchase")]) + \
             len(df[df['status'] == ''])
    print(active_counter)

    postponed_counter = len(df[df['status'].str.contains("POSTPONED")]) + \
             len(df[df['status'].str.contains("Postponed")]) 
             
    print(postponed_counter)

    cancel_counter = len(df[df['status'].str.contains("Cancel")])
    print(cancel_counter)

    data1 = {}
    data1['active_counter'] = active_counter
    data1['postponed_counter'] = postponed_counter
    data1['cancel_counter'] = cancel_counter
    data1['data'] = data

    if type == 'json':
        return JsonResponse(data1, safe=False)
    if type == 'list':
        return data


@login_required(login_url='login')
def get_all_today(request):


    
    date = time.strftime('%Y-%m-%d')

    bsav = []
    tasv = []
    tav = []
    pev = []
    lmav = []
    hrev = []
    cwav = []

    print("[*] sending all")

    bsav += list(BayStateAuction.objects.filter(date__icontains=date).values()) 
    tav += list(TownAuction.objects.filter(date__icontains=date).values()) 
    cwav += list(CommonWealthAuction.objects.filter(date__icontains=date).values()) 
    pev += list(Pesco.objects.filter(date__icontains=date).values()) 
    tasv += list(TacheAuctionAndSales.objects.filter(date__icontains=date).values()) 
    lmav += list(LandMarkAuction.objects.filter(date__icontains=date).values())

    
    data = bsav + tasv + tav + pev + lmav + cwav

    return JsonResponse(data, safe=False)


def get_xlsx(request):

    data = get_all(request, type='list')
    df = pd.DataFrame(data).drop(['id', 'message'], axis=1)



    print(df.head())

    writer = pd.ExcelWriter('output.xlsx', engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Sheet1', index=False)
    writer.save()

    filename = 'output.xlsx'

    file_full_path = "output.xlsx"

    with open(file_full_path,'r') as f:
        data = f.read()

    response = HttpResponse(data, content_type=mimetypes.guess_type(file_full_path)[0])
    response['Content-Disposition'] = "attachment; filename={0}".format(filename)
    response['Content-Length'] = os.path.getsize(file_full_path)

    return response


def get_xlsx_from_file(request):
    filename = 'output.xlsx'

    file_full_path = "output.xlsx"

    with open(file_full_path,'r') as f:
        data = f.read()

    response = HttpResponse(data, content_type=mimetypes.guess_type(file_full_path)[0])
    response['Content-Disposition'] = "attachment; filename={0}".format(filename)
    response['Content-Length'] = os.path.getsize(file_full_path)

    return response

