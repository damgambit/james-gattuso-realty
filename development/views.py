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
        if row[0] = 'Auction Date':
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
    print('parcing')
    parcer()
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
def active(request):
    obj = list(chain(bsa.filter(status__icontains='Continued'), cwa.filter(status__icontains='3rd Party Purchase'),
                     tas.filter(status__icontains='ON TIME'), ta.filter(status__icontains='On_Time'),
                     pe.filter(status__icontains=''), lma.filter(status__icontains='Currently'),
                     hre.filter(status__icontains='')))
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
            try:
                paginator = paginator.page(page)
            except PageNotAnInteger:
                paginator = paginator.page(1)
            except EmptyPage:
                paginator = paginator.page(paginator.num_pages)
            context = {
                'page': paginator,
                'num_page': count,
                'forms': form
            }
            return render(request, "table.html", context)
        elif form_search.is_valid():
            search_data = form_search.cleaned_data.get('search_data')
            obj = list(chain(bsa.filter(status__icontains=search_data),
                             cwa.filter(status__icontains=search_data), tas.filter(status__icontains=search_data),
                             ta.filter(status__icontains=search_data), pe.filter(status__icontains=search_data),
                             lma.filter(status__icontains=search_data), hre.filter(status__icontains=search_data)))
            if not obj:
                return redirect('property', error=True, search_data=search_data)
            else:
                return redirect('search', search_data=search_data)
    page = request.GET.get('page')
    paginator = Paginator(obj, 10)
    count = paginator.num_pages
    form = NotesForm(None)
    form_search = SearchForm(None)
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
        'stat': 'Active'
    }
    return render(request, "table.html", context)


@login_required(login_url='login')
def postponed(request):
    if request.is_ajax():
        bsas = BayStateAuctionSerializer(bsa.filter(status__icontains='POSTPONED'), many=True)
        tasl = TownAuctionSerializer(ta.filter(status__icontains='Postponed'), many=True)
        bsas = JSONRenderer().render(bsas.data)
        tasl = JSONRenderer().render(tasl.data)
        obj = JSONRenderer().render([bsas, tasl])
        data = {'obj': obj}
        return JsonResponse(data)


@login_required(login_url='login')
def cancelled(request):
    if request.is_ajax():
        bsas = BayStateAuctionSerializer(bsa.filter(status__icontains='Cancel'), many=True)
        tasl = TownAuctionSerializer(ta.filter(status__icontains='Cancel'), many=True)
        bsas = JSONRenderer().render(bsas.data)
        tasl = JSONRenderer().render(tasl.data)
        obj = JSONRenderer().render([bsas, tasl])
        data = {'obj': obj}
        return JsonResponse(data)


def export_xlsx_all(request, type = "Active"):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Zunaventures'

    row_num = 0

    columns = [
        (u"Date", 20),
        (u"Time", 20),
        (u"Status", 70),
        (u"Address", 100),
        (u"City", 50),
        (u"State", 20),
        (u"Zipcode", 20),
        (u"Deposit", 20),
    ]
    for col_num in range(len(columns)):
        c = ws.cell(row=row_num + 1, column=col_num + 1)
        c.value = columns[col_num][0]
        ft = Font(bold=True)
        c.font = ft

    if type == 'Active':
        queryset = list(
            chain(bsa.filter(status__icontains='Continued'), cwa.filter(status__icontains='3rd Party Purchase'),
                  tas.filter(status__icontains='ON TIME'), ta.filter(status__icontains='On_Time'),
                  pe.filter(title__icontains=''), lma.filter(status__icontains='Currently'),
                  hre.filter(status__icontains='')))
        filename = 'zunaventures_active.xlsx'
    elif type == 'Postponed':
        queryset = list(chain(bsa.filter(status__icontains='POSTPONED'), cwa.filter(status__icontains='Postponed'),
                              tas.filter(status__icontains='POSTPONED'), ta.filter(status__icontains='Postponed'),
                              pe.filter(title__icontains='POSTPONED'), lma.filter(status__icontains='POSTPONED'),
                              hre.filter(status__icontains='POSTPONED')))
        filename = 'zunaventures_postponed.xlsx'
    elif type == 'Cancelled':
        queryset = list(chain(bsa.filter(status__icontains='Cancel'), cwa.filter(status__icontains='Cancel'),
                              tas.filter(status__icontains='Cancel'), ta.filter(status__icontains='Cancel'),
                              pe.filter(title__icontains='Cancel'), lma.filter(status__icontains='Cancel'),
                              hre.filter(status__icontains='Cancel')))
        filename = 'zunaventures_cancelled.xlsx'
    elif type == 'All':
        queryset = list(chain(bsa, cwa, tas, ta, pe, lma, hre))
        filename = 'zunaventures_all.xlsx'
    else:
        obj = request.GET.get('data')
        if obj == 'status':
            queryset = list(chain(bsa.filter(status__icontains=type), cwa.filter(status__icontains=type),
                                  tas.filter(status__icontains=type), ta.filter(status__icontains=type),
                                  pe.filter(title__icontains=type), lma.filter(status__icontains=type),
                                  hre.filter(status__icontains=type)))
        elif obj == 'state':
            queryset = list(chain(bsa.filter(status__icontains=type), cwa.filter(status__icontains=type),
                                  tas.filter(status__icontains=type), ta.filter(status__icontains=type),
                                  pe.filter(title__icontains=type), lma.filter(status__icontains=type),
                                  hre.filter(status__icontains=type)))
        elif obj == 'address':
            queryset = list(chain(bsa.filter(status__icontains=type), cwa.filter(status__icontains=type),
                                  tas.filter(status__icontains=type), ta.filter(status__icontains=type),
                                  pe.filter(title__icontains=type), lma.filter(status__icontains=type),
                                  hre.filter(status__icontains=type)))

        filename = 'zunaventures_search.xlsx'

    for obj in queryset:
        row_num += 1
        row = [
            obj.date,
            obj.time,
            obj.status,
            obj.address,
            obj.city,
            obj.state,
            obj.zipcode,
            obj.deposit,
        ]
        for col_num in range(len(row)):
            c = ws.cell(row=row_num + 1, column=col_num + 1)
            c.value = row[col_num]
            # c.alignment.wrap_text = True

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=' + filename
    wb.save(response)
    return response


class BayStateAuctionView(generics.ListAPIView):
    queryset = BayStateAuction.objects
    serializer_class = BayStateAuctionSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('status', 'address', 'state')

    # pagination_class = StandardResultsSetPagination

    def partial_update(self, request, pk=None):
        serializer = BayStateAuctionSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)


class TownAuctionView(generics.ListAPIView):
    queryset = TownAuction.objects
    serializer_class = TownAuctionSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('status', 'address', 'state')

    def partial_update(self, request, pk=None):
        serializer = TownAuctionSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)



class TimelineView(MultipleModelAPIView):
    filter_backends = (filters.SearchFilter,)
    search_fields = ('status', 'address', 'state', 'city')
    flat = True
    pagination_class = StandardResultsSetPagination

    def get_queryList(self):
        queryList = ((BayStateAuction.objects.all(), BayStateAuctionSerializer),
                     (TownAuction.objects.all(), TownAuctionSerializer))

        is_active = self.request.query_params.get('active', None)
        is_postponed = self.request.query_params.get('postponed', None)
        is_cancel = self.request.query_params.get('cancel', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        search_data = self.request.query_params.get('search', None)

        print(is_active, is_cancel, is_postponed, date_from, date_to, search_data)
        bsa = BayStateAuction.objects.all()
        tas = TacheAuctionAndSales.objects.all()
        ta = TownAuction.objects.all()
        pe = Pesco.objects.all()
        lma = LandMarkAuction.objects.all()
        hre = HarkinRealEstate.objects.all()
        cwa = CommonWealthAuction.objects.all()


        if search_data:
            print("In Search")
            bsa = bsa.filter(Q(status__icontains=search_data) |
                         Q(address__icontains=search_data) |
                         Q(city__icontains=search_data) |
                         Q(state__icontains=search_data)
                       )
            ta = ta.filter( Q(status__icontains=search_data)|
                        Q(address__icontains=search_data)|
                        Q(city__icontains=search_data)|
                        Q(state__icontains=search_data)
                    )
            cwa = cwa.filter(Q(status__icontains=search_data) |
                         Q(address__icontains=search_data) |
                         Q(city__icontains=search_data) |
                         Q(state__icontains=search_data)
                       )
            lma = lma.filter( Q(status__icontains=search_data)|
                        Q(address__icontains=search_data)|
                        Q(city__icontains=search_data)|
                        Q(state__icontains=search_data)
                    )



        if is_active == "true":
            print("In Active")
            bsa = bsa.filter(status__icontains='Continued')
            ta = ta.filter(status__icontains='On_Time')
        if is_postponed  == "true":
            print("In Postponed")
            bsa = bsa.filter(status__icontains='postponed')
            ta = ta.filter(status__icontains='postponed')
        if is_cancel  == "true":
            print("In Cancel")
            bsa = bsa.filter(status__icontains='cancel')
            ta = ta.filter(status__icontains='cancel')

        if date_from:
            print("In Date From")
            bsa = bsa.filter(date__range=[datetime.datetime.strptime(date_from, '%m/%d/%Y').date(),
                             datetime.datetime(2099, 1, 1, 0, 0).date()])
            ta = ta.filter(date__range=[datetime.datetime.strptime(date_from, '%m/%d/%Y').date(),
                             datetime.datetime(2099, 1, 1, 0, 0).date()])
        if date_to:
            print("In Date To")
            bsa = bsa.filter(date__range=[datetime.datetime(1600, 1, 1, 0, 0).date(),
                             datetime.datetime.strptime(date_to, '%m/%d/%Y').date()])
            ta = ta.filter(date__range=[datetime.datetime(1600, 1, 1, 0, 0).date(),
                                          datetime.datetime.strptime(date_to, '%m/%d/%Y').date()])


        queryList = ((bsa, BayStateAuctionSerializer), (ta, TownAuctionSerializer),
                     (cwa, CommonWealthAuctionSerliazer), (lma, LandMarkAuctionSerliazer))


        return queryList
