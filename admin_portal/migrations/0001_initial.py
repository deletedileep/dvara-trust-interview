# Generated by Django 3.0.5 on 2020-04-28 16:35

import admin_portal.models
import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Banners',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Banner Name')),
                ('text', models.CharField(blank=True, default=None, max_length=255, verbose_name='Banner Text')),
                ('image', models.ImageField(upload_to='images/banners/', verbose_name='Banner Image')),
                ('order', models.IntegerField(blank=True, default=1, verbose_name='Banner Order')),
                ('link', models.CharField(blank=True, max_length=255, verbose_name='Banner Link')),
                ('status', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Banner',
                'verbose_name_plural': 'Banners',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('page_id', models.AutoField(primary_key=True, serialize=False)),
                ('page_name', models.CharField(max_length=250, verbose_name='Page Name')),
                ('page_title', models.CharField(max_length=250, verbose_name='Page Title')),
                ('page_slug', models.SlugField(blank=True, max_length=500, unique=True, verbose_name='Page Slug URL')),
                ('page_meta_title', models.CharField(blank=True, max_length=250, verbose_name='Meta Title')),
                ('page_meta_keywords', models.TextField(default='', verbose_name='Meta Keywords')),
                ('page_meta_description', models.TextField(default='', verbose_name='Meta Description')),
                ('page_header', models.CharField(blank=True, max_length=150, verbose_name='Page Header')),
                ('page_header_image', models.ImageField(blank=True, null=True, upload_to='images/page_headers', verbose_name='Page Header Image')),
                ('page_content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Page Content')),
                ('page_status', models.BooleanField(default=True, verbose_name='Status')),
                ('page_created_on', models.DateTimeField(auto_now_add=True)),
                ('page_updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
        ),
        migrations.CreateModel(
            name='System_Settings',
            fields=[
                ('system_id', models.AutoField(primary_key=True, serialize=False)),
                ('system_title', models.CharField(max_length=250, verbose_name='System Title')),
                ('system_description', models.TextField(default='', verbose_name='Description of your Website')),
                ('system_logo', models.ImageField(blank=True, null=True, upload_to='system', verbose_name='System Logo')),
                ('system_favicon', models.ImageField(blank=True, null=True, upload_to='system', verbose_name='System Favicon')),
                ('system_shareicon', models.ImageField(blank=True, null=True, upload_to='system', verbose_name='System Shareicon')),
                ('system_company', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='Company Name')),
                ('system_emails', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name="Contact Email's")),
                ('system_mobiles', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name="Contact Mobile's")),
                ('system_address', models.TextField(default='', verbose_name='Contact Address')),
                ('system_mapcanvas', models.TextField(default='', verbose_name='Google Map Frame')),
                ('system_home_content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Home Page Content')),
                ('system_testimonials_header', models.CharField(blank=True, max_length=250, null=True, verbose_name='Home Testimonials Header')),
                ('system_video_header', models.CharField(blank=True, max_length=250, null=True, verbose_name='Home Video Header')),
                ('system_contact_page_header', models.ImageField(blank=True, null=True, upload_to='contact', verbose_name='Contact Page Header')),
                ('system_facebook', models.CharField(blank=True, max_length=250, null=True, verbose_name='Facebook Link')),
                ('system_twitter', models.CharField(blank=True, max_length=250, null=True, verbose_name='Twitter Link')),
                ('system_youtube', models.CharField(blank=True, max_length=250, null=True, verbose_name='Youtube Link')),
                ('system_google', models.CharField(blank=True, max_length=250, null=True, verbose_name='Google Link')),
                ('system_insta', models.CharField(blank=True, max_length=250, null=True, verbose_name='Insta Link')),
                ('system_linkedin', models.CharField(blank=True, max_length=250, null=True, verbose_name='Linkedin Link')),
                ('system_email_smtp', models.BooleanField(default=False, verbose_name='Email SMTP')),
                ('system_email_use', models.CharField(blank=True, choices=[('SSL', 'SSL'), ('TLS', 'TLS')], default='SSL', max_length=250, null=True, verbose_name='Email Use')),
                ('system_email_host', models.CharField(blank=True, max_length=250, null=True, verbose_name='Email Host')),
                ('system_email_user', models.CharField(blank=True, max_length=250, null=True, verbose_name='Email User')),
                ('system_email_pass', models.CharField(blank=True, max_length=250, null=True, verbose_name='Email Pass')),
                ('system_email_port', models.CharField(blank=True, default='465', max_length=250, null=True, verbose_name='Email Port')),
                ('system_payu_key', models.CharField(blank=True, max_length=250, null=True, verbose_name='PayU Key')),
                ('system_payu_salt', models.CharField(blank=True, max_length=250, null=True, verbose_name='PayU Salt')),
                ('system_payu_header', models.CharField(blank=True, max_length=250, null=True, verbose_name='PayU Auth Header')),
                ('system_payu_url', models.CharField(blank=True, default='https://sandboxsecure.payu.in/_payment', max_length=250, null=True, verbose_name='PayU URL')),
                ('system_android_server_key', models.CharField(blank=True, max_length=250, null=True, verbose_name='Server Key')),
                ('system_android_sender_id', models.CharField(blank=True, max_length=250, null=True, verbose_name='Sender ID')),
                ('system_android_app_name', models.CharField(blank=True, max_length=250, null=True, verbose_name='App Name')),
                ('system_android_app_url', models.URLField(blank=True, max_length=250, null=True, verbose_name='App or Playstore URL')),
                ('system_sms_url', models.TextField(blank=True, default='', null=True, verbose_name='SMS Gateway URL')),
                ('system_sms_domain', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SMS Domain URL')),
                ('system_sms_username', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SMS Username')),
                ('system_sms_password', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SMS Password')),
                ('system_sms_senderid', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SMS Sender ID')),
                ('system_sms_username_var', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SMS Username Variable')),
                ('system_sms_password_var', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SMS Password Variable')),
                ('system_sms_mobile_var', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SMS Mobile Variable')),
                ('system_sms_message_var', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SMS Message Variable')),
                ('system_sms_senderid_var', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SMS senderId Variable')),
                ('system_sms_type_var', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SMS Type Variable')),
                ('system_sms_type_val', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SMS Type Value')),
                ('system_sms_other_var', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SMS Other Variable')),
                ('system_sms_other_val', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SMS Other Value')),
                ('system_sms_other1_var', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SMS Other1 Variable')),
                ('system_sms_other1_val', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='SMS Other1 Value')),
                ('system_analytics', models.TextField(blank=True, default='', null=True, verbose_name='Google or Alexa analytics script')),
                ('system_status', models.BooleanField(default=True)),
                ('system_created_on', models.DateTimeField(auto_now_add=True)),
                ('system_updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'System Setting',
                'verbose_name_plural': 'System Settings',
            },
            bases=(admin_portal.models.SingleInstanceMixin, models.Model),
        ),
        migrations.CreateModel(
            name='UserDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Mobile No. +91')),
                ('address', models.TextField(default='', verbose_name='Address')),
                ('state', models.CharField(default='', max_length=100, verbose_name='State')),
                ('city', models.CharField(default='', max_length=100, verbose_name='City')),
                ('pin_code', models.PositiveIntegerField(blank=True, null=True, verbose_name='Pin Code')),
                ('parent', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='admin_portal.UserDetails')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MenuBarItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Name')),
                ('title', models.CharField(default='', max_length=250, verbose_name='Title')),
                ('link', models.CharField(max_length=250, verbose_name='Link')),
                ('item_class', models.CharField(blank=True, max_length=250, null=True, verbose_name='Class')),
                ('order', models.IntegerField(default=1, null=True)),
                ('status', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('parent_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='admin_portal.MenuBarItems', verbose_name='Parent Menu')),
            ],
            options={
                'verbose_name': 'Menu Bar Item',
                'verbose_name_plural': 'Menu Bar Items',
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='InOutLogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(max_length=64)),
                ('username', models.CharField(max_length=256, null=True)),
                ('session_key', models.CharField(blank=True, max_length=100, null=True)),
                ('ip', models.CharField(blank=True, max_length=250, null=True)),
                ('browser', models.CharField(blank=True, max_length=250, null=True)),
                ('bVersion', models.CharField(blank=True, max_length=250, null=True)),
                ('os', models.CharField(blank=True, max_length=250, null=True)),
                ('device', models.CharField(blank=True, max_length=250, null=True)),
                ('ipType', models.CharField(blank=True, max_length=250, null=True)),
                ('hostName', models.CharField(blank=True, max_length=250, null=True)),
                ('ua', models.CharField(blank=True, max_length=250, null=True)),
                ('url', models.CharField(blank=True, max_length=250, null=True)),
                ('servername', models.CharField(blank=True, max_length=250, null=True)),
                ('v_date', models.CharField(blank=True, max_length=250, null=True)),
                ('domain', models.CharField(blank=True, max_length=250, null=True)),
                ('referrer', models.CharField(blank=True, max_length=250, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='Ip Address')),
                ('ip_location', models.CharField(blank=True, default=None, editable=False, max_length=250, null=True, verbose_name='Ip Location')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'In Out Log Entry',
                'verbose_name_plural': 'In Out Log Entries',
            },
        ),
    ]
