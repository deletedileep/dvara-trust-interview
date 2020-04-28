from django.shortcuts import render
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count, Case, When, IntegerField, Max, Prefetch, OuterRef, Subquery, Aggregate, CharField, Value, Sum, Avg
import urllib.request, urllib.parse, json
import itertools, functools, hashlib, os, smtplib, ssl, threading

# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_client_location(ip, get=None):
    ip_url = "http://ip-api.com/json/"
    full_ip_url = ip_url + ip
    result = None
    result_list = []
    try:
        with urllib.request.urlopen(full_ip_url) as url:
            data = json.loads(url.read().decode())
            if data['status']=='success':
                # country, countryCode, region, regionName, city, zip, lat, lon, timezone, isp, org, as, query
                result = data['city'] + ', ' + data['zip'] + ', ' + data['region'] + ', ' + data['country']
                result_list = data
            # print(data)
    except Exception:
        result = None
        result_list = []

    if get is not None and get =='full':
        return result_list
    else:
        return result

def get_system_settings():
    system_settings = System_Settings.objects.values().first()
    return system_settings

class MessageThread(threading.Thread):
    def __init__(self, mobiles, message):
        self.mobiles = mobiles
        self.message = message
        threading.Thread.__init__(self)

    def run(self):
        system_settings = get_system_settings()
        system_settings['system_sms_other_var']
        system_settings['system_sms_other_val']
        system_settings['system_sms_other1_var']
        system_settings['system_sms_other1_val']
        if system_settings['system_sms_domain'] is not None and system_settings['system_sms_domain']!='':
            sms_gateway_url = system_settings['system_sms_domain']+"?"+system_settings['system_sms_username_var']+"="+urllib.parse.quote(str(system_settings['system_sms_username']))\
                +"&"+system_settings['system_sms_password_var']+"="+urllib.parse.quote(system_settings['system_sms_password'])+"&"\
                +system_settings['system_sms_mobile_var']+"="+urllib.parse.quote(str(self.mobiles))+"&"\
                +system_settings['system_sms_message_var']+"="+urllib.parse.quote(str(self.message))+"&"\
                +system_settings['system_sms_senderid_var']+"="+system_settings['system_sms_senderid']+"&"\
                +str(system_settings['system_sms_type_var'])+"="+str(system_settings['system_sms_type_val'])
            with urllib.request.urlopen(sms_gateway_url) as url:
                data = json.loads(url.read().decode())

def send_sms(mobiles, message):
    if mobiles is not None and message is not None:
        MessageThread(mobiles, message).start()
    else:
        print('Mobile and message is required!')
        return 'Mobile and message is required!'

class EmailThread(threading.Thread):
    def __init__(self, to, subject, text, attach, mtype):
        self.to = to
        self.subject = subject
        self.text = text
        self.attach = attach
        self.mtype = mtype
        threading.Thread.__init__(self)

    def run(self):
        system_settings = get_system_settings()
        system_title = system_settings['system_title']
        is_smtp = system_settings['system_email_smtp']# is SMTP
        if is_smtp:
            ssl_r_tls = system_settings['system_email_use']# SSL - TLS
            email_user = system_settings['system_email_user']
            email_pwd  = system_settings['system_email_pass']
            email_host = system_settings['system_email_host']
            email_port = system_settings['system_email_port']
        else:
            if settings.EMAIL_USE_SSL:
                ssl_r_tls = "SSL"
            else:
                ssl_r_tls = "TLS"
            email_host = settings.EMAIL_HOST
            email_user = email_user = settings.EMAIL_HOST_USER
            email_pwd  = settings.EMAIL_HOST_PASSWORD
            email_port = settings.EMAIL_PORT

        msg = MIMEMultipart("alternative")
        msg["Subject"], msg["From"], msg["To"] = self.subject, email_user, self.to
        # msg['Cc']      = 'deletedileep@gmail.com'
        msg.attach(MIMEText(self.text, self.mtype))

        if ssl_r_tls=='SSL':
            try:
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(email_host, email_port, context=context) as server:
                    server.login(email_user, email_pwd)
                    server.sendmail(email_user, self.to, msg.as_string())
            except:
                print('mail ssl except')
        else:
            try:
                mailServer = smtplib.SMTP(email_host, email_port)
                mailServer.ehlo()
                mailServer.starttls()
                mailServer.ehlo()
                mailServer.login(email_user, email_pwd)
                mailServer.sendmail(email_user, self.to, msg.as_string())
                mailServer.close()
            except:
                print('mail non ssl except')

def index(request):
    system_settings = get_system_settings()
    data = {
    }
    return render(request, 'home.html', data)

def dynamic_page(request, slug):
    if slug is not None:
        page_data = get_object_or_404(Pages, page_slug=slug)
    data = {
        'page_data': page_data,
    }
    return render(request, 'dynamic_page.html', data)
