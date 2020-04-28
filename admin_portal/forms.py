from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.conf import settings

class PageForm(ModelForm):
	class Meta:
		model = Pages
		fields = ['page_name','page_title','page_slug','page_meta_title','page_meta_keywords','page_meta_description','page_header','page_header_image','page_content','page_status']

class BannerForm(ModelForm):
	class Meta:
		model = Banners
		fields = ['name','text','image','order','link','status']

class MenubarForm(ModelForm):
	class Meta:
		model = MenuBarItems
		fields = ['parent_id','name','title','link','item_class','order','status']

class Site_SettingsForm(ModelForm):
	class Meta:
		model = System_Settings
		fields = ['system_title', 'system_description', 'system_logo', 'system_favicon', 'system_shareicon', 'system_company', 'system_emails', 'system_mobiles', 'system_address', 'system_mapcanvas', 'system_home_content', 'system_testimonials_header', 'system_video_header', 'system_contact_page_header', 'system_facebook', 'system_twitter', 'system_youtube', 'system_google', 'system_insta', 'system_linkedin', 'system_analytics']

class Email_SettingsForm(ModelForm):
	class Meta:
		model = System_Settings
		fields = ['system_email_smtp', 'system_email_use', 'system_email_host','system_email_user','system_email_pass','system_email_port']

class Payment_SettingsForm(ModelForm):
	class Meta:
		model = System_Settings
		fields = ['system_payu_key', 'system_payu_salt','system_payu_header', 'system_payu_url']

class Android_SettingsForm(ModelForm):
	class Meta:
		model = System_Settings
		fields = ['system_android_server_key', 'system_android_sender_id','system_android_app_name', 'system_android_app_url']

class Sms_SettingsForm(ModelForm):
	class Meta:
		model = System_Settings
		fields = ['system_sms_url', 'system_sms_domain', 'system_sms_username','system_sms_password','system_sms_senderid','system_sms_username_var','system_sms_password_var','system_sms_mobile_var','system_sms_message_var','system_sms_senderid_var','system_sms_type_var','system_sms_type_val','system_sms_other_var','system_sms_other_val','system_sms_other1_var','system_sms_other1_val']

class DetailsForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["parent"].queryset = UserDetails.objects.filter(user__is_staff=True)

	class Meta:
		model = UserDetails
		fields = ('parent', 'phone', 'address', 'state', 'city')

class UserProfileForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email']

class NewUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2','is_staff')

class OnlyDetailsForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["parent"].queryset = UserDetails.objects.filter(user__is_staff=True)
	# email = forms.EmailField(max_length=200, help_text='Required')
	class Meta:
		model = UserDetails
		fields = ('parent', 'phone', 'address', 'state', 'city')


