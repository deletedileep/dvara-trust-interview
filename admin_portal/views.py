from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse, get_list_or_404, get_object_or_404
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from .models import *
from django.db import IntegrityError
from django.contrib import messages
from django.forms import ModelForm, modelformset_factory
from .forms import *
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from urllib.parse import quote
from django.core.paginator import Paginator
from django.template.loader import render_to_string, get_template
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from public.tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text

import urllib.request, urllib.parse, json, datetime, itertools, functools, hashlib, os, smtplib, ssl, threading, os, sys, zipfile
import xml.dom.minidom, subprocess, csv, re, socket
# Create your views here.

PAGE_SIZE = 20

def get_system_settings():
    system_settings = System_Settings.objects.values().first()
    return system_settings

def is_admin(request):
    return True if request.user.is_staff else False

def dashboard(request):
    # check user is admin
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+quote(request.path, safe=''))
    users_obj = User.objects.all().count()
    data = {'users_obj': users_obj}
    return render(request, 'dashboard.html', {'data': data } )


def pages_view(request):
    # check user is admin
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)

    status = ''
    search_text = ''

    #  | Q(pay_amount__contains=search_text)
    if request.method == 'GET' and "search" in request.GET and request.GET['search']!='':
        search_text = request.GET['search']
        page_data = Pages.objects.filter(\
                 Q(page_name__contains=search_text)\
                 | Q(page_title__contains=search_text) | Q(page_slug__contains=search_text)\
                 | Q(page_content__contains=search_text) | Q(page_header__contains=search_text)\
                 | Q(page_rating=search_text)
                )
    else:
        page_data = Pages.objects.all()

    if request.method == 'GET' and "status" in request.GET and request.GET['status']!='' and request.GET['status'].isnumeric():
        status = int(request.GET['status'] or 0)
        if status==1:
            page_data = page_data.filter(page_status=True)
        elif status==0:
            page_data = page_data.filter(page_status=False)

    page = request.GET.get("page",1)
    paginator = Paginator(page_data, PAGE_SIZE)
    page_data = paginator.page(page)
    data = {
        'pages_data': page_data,
        'search': search_text,
        'status': status,
    }
    return render(request, 'cms/view_pages_list.html', data)

def add_page(request):
    # check user is admin
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form_p = PageForm(request.POST, request.FILES)
        try:
            # check whether it's valid:
            if form_p.is_valid():
                # get basemodel values
                form_p.instance.modified_by = request.user
                form_p.save()
                messages.success(request, 'Page added successfully', extra_tags='green')
                return redirect('pages_view')
            # invalid something!
            else:
                return render(request, 'cms/add_page.html', {'mode': 'Add', 'form_p': form_p})
        except IntegrityError as e:
            messages.error(request, 'There was a problem editing the Page - please try again', extra_tags='red')
            return render(request, 'cms/add_page.html', {'mode': 'Add', 'form_p': form_p})
    # if a GET (or any other method) we'll create a blank form
    else:
        form_p = PageForm()
        return render(request, 'cms/add_page.html', {'mode': 'Add', 'form_p': form_p})

def edit_page(request, pk):
    # check user is admin
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)
    # load product group
    p = Pages.objects.get(pk=pk)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form_p = PageForm(request.POST, request.FILES, instance=p)
        try:
            # check whether it's valid:
            if form_p.is_valid():
                # get basemodel values
                form_p.instance.modified_by = request.user
                form_p.save()
                messages.success(request, 'Page edited successfully', extra_tags='green')
                return redirect('pages_view')
            # invalid something!
            else:
                return render(request, 'cms/add_page.html', {'mode': 'Edit', 'form_p': form_p})
        except IntegrityError as e:
            messages.error(request, 'There was a problem editing the Page - please try again', extra_tags='red')
            return render(request, 'cms/add_page.html', {'mode': 'Edit', 'form_p': form_p})
    # if a GET (or any other method) we'll load the user for editing
    else:
        form_p = PageForm(instance=p)
        return render(request, 'cms/add_page.html', {'mode': 'Edit', 'form_p': form_p})

def delete_page(request, pk):
    # check user is admin
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)

    # load user and agent
    p = Pages.objects.get(pk=pk)
    p.delete(keep_parents=True)
    messages.success(request, 'Page deleted successfully', extra_tags='green')
    return redirect('pages_view')


def banners_view(request):
    # check user is admin
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)

    status = ''
    search_text = ''

    #  | Q(pay_amount__contains=search_text)
    if request.method == 'GET' and "search" in request.GET and request.GET['search']!='':
        search_text = request.GET['search']
        banner_data = Banners.objects.filter(\
                 Q(banner_name__contains=search_text)\
                 | Q(banner_title__contains=search_text) | Q(banner_slug__contains=search_text)\
                 | Q(banner_content__contains=search_text) | Q(banner_header__contains=search_text)\
                 | Q(banner_rating=search_text)
                )
    else:
        banner_data = Banners.objects.all()

    if request.method == 'GET' and "status" in request.GET and request.GET['status']!='' and request.GET['status'].isnumeric():
        status = int(request.GET['status'] or 0)
        if status==1:
            banner_data = banner_data.filter(banner_status=True)
        elif status==0:
            banner_data = banner_data.filter(banner_status=False)

    page = request.GET.get("page",1)
    paginator = Paginator(banner_data, PAGE_SIZE)
    banner_data = paginator.page(page)
    data = {
        'banners_data': banner_data,
        'search': search_text,
        'status': status,
    }
    return render(request, 'cms/view_banners_list.html', data)

def add_banner(request):
    # check user is admin
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form_p = BannerForm(request.POST, request.FILES)
        try:
            # check whether it's valid:
            if form_p.is_valid():
                # get basemodel values
                form_p.instance.modified_by = request.user
                form_p.save()
                messages.success(request, 'Banner added successfully', extra_tags='green')
                return redirect('banners_view')
            # invalid something!
            else:
                return render(request, 'cms/add_banner.html', {'mode': 'Add', 'form_p': form_p})
        except IntegrityError as e:
            messages.error(request, 'There was a problem editing the Banner - please try again', extra_tags='red')
            return render(request, 'cms/add_banner.html', {'mode': 'Add', 'form_p': form_p})
    # if a GET (or any other method) we'll create a blank form
    else:
        form_p = BannerForm()
        return render(request, 'cms/add_banner.html', {'mode': 'Add', 'form_p': form_p})

def edit_banner(request, pk):
    # check user is admin
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)
    # load product group
    p = Banners.objects.get(pk=pk)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form_p = BannerForm(request.POST, request.FILES, instance=p)
        try:
            # check whether it's valid:
            if form_p.is_valid():
                # get basemodel values
                form_p.instance.modified_by = request.user
                form_p.save()
                messages.success(request, 'Banner edited successfully', extra_tags='green')
                return redirect('banners_view')
            # invalid something!
            else:
                return render(request, 'cms/add_banner.html', {'mode': 'Edit', 'form_p': form_p})
        except IntegrityError as e:
            messages.error(request, 'There was a problem editing the Banner - please try again', extra_tags='red')
            return render(request, 'cms/add_banner.html', {'mode': 'Edit', 'form_p': form_p})
    # if a GET (or any other method) we'll load the user for editing
    else:
        form_p = BannerForm(instance=p)
        return render(request, 'cms/add_banner.html', {'mode': 'Edit', 'form_p': form_p})

def delete_banner(request, pk):
    # check user is admin
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)

    # load user and agent
    p = Banners.objects.get(pk=pk)
    p.delete(keep_parents=True)
    messages.success(request, 'Banner deleted successfully', extra_tags='green')
    return redirect('banners_view')


def menubars_view(request):
    # check user is admin
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)

    status = ''
    search_text = ''

    #  | Q(pay_amount__contains=search_text)
    if request.method == 'GET' and "search" in request.GET and request.GET['search']!='':
        search_text = request.GET['search']
        menubar_data = MenuBarItems.objects.filter(\
                 Q(menubar_name__contains=search_text)\
                 | Q(menubar_title__contains=search_text) | Q(menubar_slug__contains=search_text)\
                 | Q(menubar_content__contains=search_text) | Q(menubar_header__contains=search_text)\
                 | Q(menubar_rating=search_text)
                )
    else:
        menubar_data = MenuBarItems.objects.all()

    if request.method == 'GET' and "status" in request.GET and request.GET['status']!='' and request.GET['status'].isnumeric():
        status = int(request.GET['status'] or 0)
        if status==1:
            menubar_data = menubar_data.filter(menubar_status=True)
        elif status==0:
            menubar_data = menubar_data.filter(menubar_status=False)

    page = request.GET.get("page",1)
    paginator = Paginator(menubar_data, PAGE_SIZE)
    menubar_data = paginator.page(page)
    data = {
        'menubars_data': menubar_data,
        'search': search_text,
        'status': status,
    }
    return render(request, 'cms/view_menubars_list.html', data)

def add_menubar_link(request):
    # check user is admin
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form_p = MenubarForm(request.POST)
        try:
            # check whether it's valid:
            if form_p.is_valid():
                # get basemodel values
                form_p.instance.modified_by = request.user
                form_p.save()
                messages.success(request, 'Menubar added successfully', extra_tags='green')
                return redirect('menubars_view')
            # invalid something!
            else:
                return render(request, 'cms/add_menubar.html', {'mode': 'Add', 'form_p': form_p})
        except IntegrityError as e:
            messages.error(request, 'There was a problem editing the Menubar - please try again', extra_tags='red')
            return render(request, 'cms/add_menubar.html', {'mode': 'Add', 'form_p': form_p})
    # if a GET (or any other method) we'll create a blank form
    else:
        form_p = MenubarForm()
        return render(request, 'cms/add_menubar.html', {'mode': 'Add', 'form_p': form_p})

def edit_menubar_link(request, pk):
    # check user is admin
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)
    # load product group
    p = MenuBarItems.objects.get(pk=pk)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form_p = MenubarForm(request.POST, request.FILES, instance=p)
        try:
            # check whether it's valid:
            if form_p.is_valid():
                # get basemodel values
                form_p.instance.modified_by = request.user
                form_p.save()
                messages.success(request, 'Menubar edited successfully', extra_tags='green')
                return redirect('menubars_view')
            # invalid something!
            else:
                return render(request, 'cms/add_menubar.html', {'mode': 'Edit', 'form_p': form_p})
        except IntegrityError as e:
            messages.error(request, 'There was a problem editing the Menubar - please try again', extra_tags='red')
            return render(request, 'cms/add_menubar.html', {'mode': 'Edit', 'form_p': form_p})
    # if a GET (or any other method) we'll load the user for editing
    else:
        form_p = MenubarForm(instance=p)
        return render(request, 'cms/add_menubar.html', {'mode': 'Edit', 'form_p': form_p})

def delete_menubar_link(request, pk):
    # check user is admin
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)

    # load user and agent
    p = MenuBarItems.objects.get(pk=pk)
    p.delete(keep_parents=True)
    messages.success(request, 'Menubar deleted successfully', extra_tags='green')
    return redirect('menubars_view')

def ajax_active(request):
    if 'approve_user' in request.GET and 'id' in request.GET and 'status' in request.GET and request.GET['id'].isnumeric():
        user_id = request.GET.get("id")
        status = request.GET.get("status")
        if user_id is not None and user_id !='':
            if status == '1':
                obj_data = User.objects.filter(pk=user_id).update(is_active=True)
            else:
                obj_data = User.objects.filter(pk=user_id).update(is_active=False)
    if 'approve_banner' in request.GET and 'id' in request.GET and 'status' in request.GET and request.GET['id'].isnumeric():
        row_id = request.GET.get("id")
        status = request.GET.get("status")
        if row_id is not None and row_id !='':
            if status == '1':
                obj_data = Banners.objects.filter(pk=row_id).update(status=True)
            else:
                obj_data = Banners.objects.filter(pk=row_id).update(status=False)
    if 'approve_menubar' in request.GET and 'id' in request.GET and 'status' in request.GET and request.GET['id'].isnumeric():
        row_id = request.GET.get("id")
        status = request.GET.get("status")
        if row_id is not None and row_id !='':
            if status == '1':
                obj_data = MenuBarItems.objects.filter(pk=row_id).update(status=True)
            else:
                obj_data = MenuBarItems.objects.filter(pk=row_id).update(status=False)
    if 'approve_page' in request.GET and 'id' in request.GET and 'status' in request.GET and request.GET['id'].isnumeric():
        row_id = request.GET.get("id")
        status = request.GET.get("status")
        if row_id is not None and row_id !='':
            if status == '1':
                obj_data = Pages.objects.filter(pk=row_id).update(page_status=True)
            else:
                obj_data = Pages.objects.filter(pk=row_id).update(page_status=False)

    return JsonResponse({'status':True})


def public_users_list_view(request):
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)
    search_text = ''
    user_type = ''
    registered = ''
    parent = ''
    staff = User.objects.filter(is_superuser=False).filter(is_staff=True).prefetch_related('userdetails')

    if request.method == 'POST':
        if 'user' in request.POST and 'message' in request.POST and request.POST['message']!='':
            users_list = request.POST.getlist('user');
            message = request.POST['message'];
            users_data = User.objects.prefetch_related('userdetails').filter(pk__in=users_list)
            # print(users_data)
            for user_row in users_data:
                if hasattr(user_row, 'userdetails') and user_row.userdetails:
                    if user_row.userdetails.phone is not None and message is not None:
                        send_sms(user_row.userdetails.phone, message)
            # print(request.POST.getlist('user'))
            # print(request.POST['message'])

            messages.success(request, 'Message sent successfully', extra_tags='green')
            return redirect('users_list_view')
        else:
            messages.success(request, 'Users and message required!', extra_tags='green')
            return redirect('users_list_view')
    else:
        users_data = User.objects.filter(is_superuser=False).filter(is_staff=False).prefetch_related('userdetails')

        if request.method == 'GET' and "search" in request.GET and request.GET['search']!='':
            search_text = request.GET['search']
            users_data = users_data.filter(\
                    Q(username__contains=search_text) | Q(first_name__contains=search_text) | Q(email__contains=search_text)\
                    )

        if request.method == 'GET' and "type" in request.GET and request.GET['type']!='':
            user_type = request.GET['type']

        if request.method == 'GET' and "parent" in request.GET and request.GET['parent']!='':
            parent = request.GET['parent']
            children_users = UserDetails.objects.filter(parent__user__username=parent).values('user')
            
            print(children_users)
            users_data = users_data.filter(id__in=children_users)
            # Parent__username=parent
            # users_data = users_data.filter(username__iexact=parent)

        if request.method == 'GET' and "registered" in request.GET and request.GET['registered']!='':
            registered = request.GET['registered']
            registered_dates = registered.split(' - ')
            # if False:
            if len(registered_dates)==2:
                start_date = datetime.datetime.strptime(registered_dates[0], "%d/%m/%Y").strftime("%Y-%m-%d")
                end_date = datetime.datetime.strptime(registered_dates[1], "%d/%m/%Y").strftime("%Y-%m-%d")
                # print(end_date)
                if start_date == end_date:
                    users_data = users_data.filter(date_joined__date=end_date)
                else:
                    users_data = users_data.filter(date_joined__range=[start_date, end_date])

        users_data = users_data.order_by('-id')
        per_page = PAGE_SIZE
        if 'per_page' in request.GET:
            per_page = request.GET['per_page']
        page = request.GET.get("page",1)
        paginator = Paginator(users_data, per_page)
        users_data = paginator.page(page)

        context = {
            'users_data':users_data,
            'parent':parent,
            'staff':staff,
            'type':user_type,
            'per_page': str(per_page),
            'search':search_text,
            'registered':registered,
        }
        return render(request, 'users/view_users_list.html', context)

def staff_users_list_view(request):
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)
    search_text = ''
    user_type = ''
    registered = ''
    parent = ''
    staff = User.objects.filter(is_superuser=False).filter(is_staff=True).prefetch_related('userdetails')

    if request.method == 'POST':
        if 'user' in request.POST and 'message' in request.POST and request.POST['message']!='':
            users_list = request.POST.getlist('user');
            message = request.POST['message'];
            users_data = User.objects.filter(is_superuser=False).filter(is_staff=True).prefetch_related('userdetails').filter(pk__in=users_list)
            # print(users_data)
            for user_row in users_data:
                if hasattr(user_row, 'userdetails') and user_row.userdetails:
                    if user_row.userdetails.phone is not None and message is not None:
                        send_sms(user_row.userdetails.phone, message)
            # print(request.POST.getlist('user'))
            # print(request.POST['message'])

            messages.success(request, 'Message sent successfully', extra_tags='green')
            return redirect('users_list_view')
        else:
            messages.success(request, 'Users and message required!', extra_tags='green')
            return redirect('users_list_view')
    else:
        users_data = User.objects.filter(is_superuser=False).filter(is_staff=True).prefetch_related('userdetails')

        if request.method == 'GET' and "search" in request.GET and request.GET['search']!='':
            search_text = request.GET['search']
            users_data = users_data.filter(\
                    Q(username__contains=search_text) | Q(first_name__contains=search_text) | Q(email__contains=search_text)\
                    )

        if request.method == 'GET' and "type" in request.GET and request.GET['type']!='':
            user_type = request.GET['type']

        if request.method == 'GET' and "parent" in request.GET and request.GET['parent']!='':
            parent = request.GET['parent']
            users_data = users_data.filter(username__iexact=parent)

        if request.method == 'GET' and "registered" in request.GET and request.GET['registered']!='':
            registered = request.GET['registered']
            registered_dates = registered.split(' - ')
            # if False:
            if len(registered_dates)==2:
                start_date = datetime.datetime.strptime(registered_dates[0], "%d/%m/%Y").strftime("%Y-%m-%d")
                end_date = datetime.datetime.strptime(registered_dates[1], "%d/%m/%Y").strftime("%Y-%m-%d")
                # print(end_date)
                if start_date == end_date:
                    users_data = users_data.filter(date_joined__date=end_date)
                else:
                    users_data = users_data.filter(date_joined__range=[start_date, end_date])

        users_data = users_data.order_by('-id')
        per_page = PAGE_SIZE
        if 'per_page' in request.GET:
            per_page = request.GET['per_page']
        page = request.GET.get("page",1)
        paginator = Paginator(users_data, per_page)
        users_data = paginator.page(page)

        context = {
            'users_data':users_data,
            'parent':parent,
            'staff':staff,
            'type':user_type,
            'per_page': str(per_page),
            'search':search_text,
            'registered':registered,
        }
        return render(request, 'users/view_users_list.html', context)

def users_list_view(request):
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)
    search_text = ''
    user_type = ''
    registered = ''
    parent = ''
    staff = User.objects.filter(is_superuser=False).filter(is_staff=True).prefetch_related('userdetails')

    if request.method == 'POST':
        if 'user' in request.POST and 'message' in request.POST and request.POST['message']!='':
            users_list = request.POST.getlist('user');
            message = request.POST['message'];
            users_data = User.objects.prefetch_related('userdetails').filter(pk__in=users_list)
            # print(users_data)
            for user_row in users_data:
                if hasattr(user_row, 'userdetails') and user_row.userdetails:
                    if user_row.userdetails.phone is not None and message is not None:
                        send_sms(user_row.userdetails.phone, message)
            # print(request.POST.getlist('user'))
            # print(request.POST['message'])

            messages.success(request, 'Message sent successfully', extra_tags='green')
            return redirect('users_list_view')
        else:
            messages.success(request, 'Users and message required!', extra_tags='green')
            return redirect('users_list_view')
    else:
        users_data = User.objects.all().prefetch_related('userdetails')

        if request.method == 'GET' and "search" in request.GET and request.GET['search']!='':
            search_text = request.GET['search']
            users_data = users_data.filter(\
                    Q(username__contains=search_text) | Q(first_name__contains=search_text) | Q(email__contains=search_text)\
                    )

        if request.method == 'GET' and "type" in request.GET and request.GET['type']!='':
            user_type = request.GET['type']

        if request.method == 'GET' and "parent" in request.GET and request.GET['parent']!='':
            parent = request.GET['parent']
            users_data = users_data.filter(username__iexact=parent)

        if request.method == 'GET' and "registered" in request.GET and request.GET['registered']!='':
            registered = request.GET['registered']
            registered_dates = registered.split(' - ')
            # if False:
            if len(registered_dates)==2:
                start_date = datetime.datetime.strptime(registered_dates[0], "%d/%m/%Y").strftime("%Y-%m-%d")
                end_date = datetime.datetime.strptime(registered_dates[1], "%d/%m/%Y").strftime("%Y-%m-%d")
                # print(end_date)
                if start_date == end_date:
                    users_data = users_data.filter(date_joined__date=end_date)
                else:
                    users_data = users_data.filter(date_joined__range=[start_date, end_date])

        users_data = users_data.order_by('-id')
        per_page = PAGE_SIZE
        if 'per_page' in request.GET:
            per_page = request.GET['per_page']
        page = request.GET.get("page",1)
        paginator = Paginator(users_data, per_page)
        users_data = paginator.page(page)

        context = {
            'users_data':users_data,
            'parent':parent,
            'staff':staff,
            'type':user_type,
            'per_page': str(per_page),
            'search':search_text,
            'registered':registered,
        }
        return render(request, 'users/view_users_list.html', context)

def add_user(request):
    # check user is admin
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)

    current_site = get_current_site(request)
    system_settings = get_system_settings()

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request
        form_p = NewUserForm(request.POST)
        form = OnlyDetailsForm(request.POST, request.FILES)
        try:
            # check whether it's valid:
            if form_p.is_valid():
                # get basemodel values
                form_p.instance.modified_by = request.user
                user = form_p.save(commit=False)

                # form = OnlyDetailsForm(request.POST, request.FILES)
                if form.is_valid():
                    user.save()
                    userdetails = form.save(commit=False)
                    print(user)
                    userdetails.user = user
                    userdetails.save()

                    # to_email = form.cleaned_data.get('email')
                    # to_mobile = userdetails.phone
                    # subject = 'Thank you for your Choosing '+system_settings['system_title']
                    # message = """Welcome to <b>{}</b>.<br/> thanks for registered with us.<br/>User Name: <b>{}</b> <br/> kindly click below link for login \
                    #         {}<br/>
                    #         Note : PASSWORD is same as entered while registered""".format(system_settings['system_title'], user.username, current_site.domain)

                    # from_email = system_settings['system_email_user']
                    # to_list = [to_email, system_settings['system_email_user']]
                    # send_sms(to_mobile,'Hi '+user.username+', Thanks for Regestring in '+system_settings['system_title']+' - http://'+request.META['HTTP_HOST'])
                    # send_mail(subject, message, from_email, to_list, fail_silently=True,html_message=message)
                    messages.success(request, 'User added successfully', extra_tags='green')
                    return redirect('users_list_view')
                else:
                    messages.success(request, 'User adding failed!', extra_tags='red')
                    return render(request, 'users/add_user.html', {'mode': 'Add', 'form_p': form_p, 'form': form})
                    
            # invalid something!
            else:
                return render(request, 'users/add_user.html', {'mode': 'Add', 'form_p': form_p, 'form': form})
        except IntegrityError as e:
            messages.error(request, 'There was a problem adding user - please try again', extra_tags='red')
            return render(request, 'users/add_user.html', {'mode': 'Add', 'form_p': form_p, 'form': form})
    # if a GET (or any other method) we'll create a blank form
    else:
        form_p = NewUserForm()
        form = OnlyDetailsForm()
        return render(request, 'users/add_user.html', {'mode': 'Add', 'form_p': form_p, 'form': form})

def edit_user(request, pk):
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)

    p = None
    # load product group
    user_data = User.objects.prefetch_related('userdetails').get(pk=pk)
    if hasattr(user_data, 'userdetails') and user_data.userdetails:
        print('userdetails exists')
    else:
        print('userdetails not exists')

    if request.method == 'POST':
        if hasattr(user_data, 'userdetails') and user_data.userdetails:
            form_p = OnlyDetailsForm(request.POST, request.FILES, instance=user_data.userdetails)
            try:
                if form_p.is_valid():
                    form_p.instance.modified_by = request.user
                    form_p.save()
                    messages.success(request, 'User edited successfully', extra_tags='green')
                    return redirect('users_list_view')
                # invalid something!
                else:
                    return render(request, 'users/add_user.html', {'mode': 'Edit', 'form_p': form_p})
            except IntegrityError as e:
                messages.error(request, 'There was a problem editing the user - please try again', extra_tags='red')
                return render(request, 'users/add_user.html', {'mode': 'Edit', 'form_p': form_p})
        else:
            form_p = OnlyDetailsForm(request.POST, request.FILES)
            try:
                if form_p.is_valid():
                    form_p.instance.modified_by = request.user
                    userdetails = form_p.save(commit=False)
                    userdetails.user = user_data
                    userdetails.save()
                    messages.success(request, 'User edited successfully', extra_tags='green')
                    return redirect('users_list_view')
                # invalid something!
                else:
                    return render(request, 'users/add_user.html', {'mode': 'Edit', 'form_p': form_p})
            except IntegrityError as e:
                messages.error(request, 'There was a problem editing the user - please try again', extra_tags='red')
                return render(request, 'users/add_user.html', {'mode': 'Edit', 'form_p': form_p})
    # if a GET (or any other method) we'll load the user for editing
    else:
        if hasattr(user_data, 'userdetails') and user_data.userdetails:
            form_p = OnlyDetailsForm(instance=user_data.userdetails)
        else:
            form_p = OnlyDetailsForm()
        return render(request, 'users/add_user.html', {'mode': 'Edit', 'form_p': form_p})

def edit_user_pass(request, pk):
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)

    # load product group
    p = User.objects.get(pk=pk)
    if request.method == 'POST':
        form_p = NewUserForm(request.POST, instance=p)
        try:
            if form_p.is_valid():
                form_p.instance.modified_by = request.user
                form_p.save()
                messages.success(request, 'User Password edited successfully', extra_tags='green')
                return redirect('users_list_view')
            # invalid something!
            else:
                return render(request, 'users/edit_user_pass.html', {'mode': 'Edit', 'form_p': form_p})
        except IntegrityError as e:
            messages.error(request, 'There was a problem while editing user securities - please try again', extra_tags='red')
            return render(request, 'users/edit_user_pass.html', {'mode': 'Edit', 'form_p': form_p})
    # if a GET (or any other method) we'll load the user for editing
    else:
        form_p = NewUserForm(instance=p)
        return render(request, 'users/edit_user_pass.html', {'mode': 'Edit', 'form_p': form_p})

def delete_user(request, pk):
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)

    r_object = get_object_or_404(User, pk=pk)
    r_object.delete(keep_parents=True)
    messages.success(request, 'User deleted successfully', extra_tags='green')
    return redirect('users_list_view')


def view_user_details(request, user_id):
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)

    users_data = User.objects.filter(pk=user_id).first()
    context = {
        'users_data':users_data,
    }
    return render(request, 'users/users_detail_view.html', context)

def system_settings_view(request):
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)

    system_settings = get_system_settings()
    context = {
        'system_settings':system_settings,
    }
    return render(request, 'settings/view_settings.html', context)

def edit_site_settings(request, pk):
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)
    view_title = "Site Settings"

    p = System_Settings.objects.get(pk=pk)
    if request.method == 'POST':
        form_p = Site_SettingsForm(request.POST, request.FILES, instance=p)
        try:
            if form_p.is_valid():
                form_p.instance.modified_by = request.user
                form_p.save()
                messages.success(request, view_title+' edited successfully', extra_tags='green')
                return redirect('system_settings_view')
            else:
                return render(request, 'settings/add_settings.html', {'mode': 'Edit', 'form_p': form_p, 'view_title':view_title})
        except IntegrityError as e:
            messages.error(request, 'There was a problem editing the '+view_title+' - please try again', extra_tags='red')
            return render(request, 'settings/add_settings.html', {'mode': 'Edit', 'form_p': form_p, 'view_title':view_title})
    else:
        form_p = Site_SettingsForm(instance=p)
        return render(request, 'settings/add_settings.html', {'mode': 'Edit', 'form_p': form_p, 'view_title':view_title})

def edit_email_settings(request, pk):
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)
    view_title = "Email Settings"

    p = System_Settings.objects.get(pk=pk)
    if request.method == 'POST':
        form_p = Email_SettingsForm(request.POST, request.FILES, instance=p)
        try:
            if form_p.is_valid():
                form_p.instance.modified_by = request.user
                form_p.save()
                messages.success(request, view_title+' edited successfully', extra_tags='green')
                return redirect('system_settings_view')
            else:
                return render(request, 'settings/add_settings.html', {'mode': 'Edit', 'form_p': form_p, 'view_title':view_title})
        except IntegrityError as e:
            messages.error(request, 'There was a problem editing the '+view_title+' - please try again', extra_tags='red')
            return render(request, 'settings/add_settings.html', {'mode': 'Edit', 'form_p': form_p, 'view_title':view_title})
    else:
        form_p = Email_SettingsForm(instance=p)
        return render(request, 'settings/add_settings.html', {'mode': 'Edit', 'form_p': form_p, 'view_title':view_title})

def edit_payment_settings(request, pk):
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)
    view_title = "Payment Settings"

    p = System_Settings.objects.get(pk=pk)
    if request.method == 'POST':
        form_p = Payment_SettingsForm(request.POST, request.FILES, instance=p)
        try:
            if form_p.is_valid():
                form_p.instance.modified_by = request.user
                form_p.save()
                messages.success(request, view_title+' edited successfully', extra_tags='green')
                return redirect('system_settings_view')
            else:
                return render(request, 'settings/add_settings.html', {'mode': 'Edit', 'form_p': form_p, 'view_title':view_title})
        except IntegrityError as e:
            messages.error(request, 'There was a problem editing the '+view_title+' - please try again', extra_tags='red')
            return render(request, 'settings/add_settings.html', {'mode': 'Edit', 'form_p': form_p, 'view_title':view_title})
    else:
        form_p = Payment_SettingsForm(instance=p)
        return render(request, 'settings/add_settings.html', {'mode': 'Edit', 'form_p': form_p, 'view_title':view_title})

def edit_android_settings(request, pk):
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)
    view_title = "Android Settings"

    p = System_Settings.objects.get(pk=pk)
    if request.method == 'POST':
        form_p = Android_SettingsForm(request.POST, request.FILES, instance=p)
        try:
            if form_p.is_valid():
                form_p.instance.modified_by = request.user
                form_p.save()
                messages.success(request, view_title+' edited successfully', extra_tags='green')
                return redirect('system_settings_view')
            else:
                return render(request, 'settings/add_settings.html', {'mode': 'Edit', 'form_p': form_p, 'view_title':view_title})
        except IntegrityError as e:
            messages.error(request, 'There was a problem editing the '+view_title+' - please try again', extra_tags='red')
            return render(request, 'settings/add_settings.html', {'mode': 'Edit', 'form_p': form_p, 'view_title':view_title})
    else:
        form_p = Android_SettingsForm(instance=p)
        return render(request, 'settings/add_settings.html', {'mode': 'Edit', 'form_p': form_p, 'view_title':view_title})

def edit_sms_settings(request, pk):
    if not is_admin(request):
        return redirect('/admin_portal/login?go='+request.path)
    view_title = "SMS Settings"

    p = System_Settings.objects.get(pk=pk)
    if request.method == 'POST':
        form_p = Sms_SettingsForm(request.POST, request.FILES, instance=p)
        try:
            if form_p.is_valid():
                form_p.instance.modified_by = request.user
                form_p.save()
                messages.success(request, view_title+' edited successfully', extra_tags='green')
                return redirect('system_settings_view')
            else:
                return render(request, 'settings/add_sms_settings.html', {'mode': 'Edit', 'form_p': form_p, 'view_title':view_title})
        except IntegrityError as e:
            messages.error(request, 'There was a problem editing the '+view_title+' - please try again', extra_tags='red')
            return render(request, 'settings/add_sms_settings.html', {'mode': 'Edit', 'form_p': form_p, 'view_title':view_title})
    else:
        form_p = Sms_SettingsForm(instance=p)
        return render(request, 'settings/add_sms_settings.html', {'mode': 'Edit', 'form_p': form_p, 'view_title':view_title})

