from django.db import models
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from ckeditor_uploader.fields import RichTextUploadingField
from django.dispatch import receiver
from django.urls import reverse
import os

# Create your models here.

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

class SingleInstanceMixin(object):
	"""Makes sure that no more than one instance of a given model is created."""

	def clean(self):
		model = self.__class__
		if (model.objects.count() > 0 and self.system_id != model.objects.get().system_id):
			raise ValidationError("Can only create 1 %s instance" % model.__name__)
		super(SingleInstanceMixin, self).clean()

class SingleInstanceMixin1(object):
	"""Makes sure that no more than one instance of a given model is created."""

	def clean(self):
		model = self.__class__
		if (model.objects.count() > 0 and self.sg_id != model.objects.get().sg_id):
			raise ValidationError("Can only create 1 %s instance" % model.__name__)
		super(SingleInstanceMixin1, self).clean()

class Banners(models.Model):
	name = models.CharField(max_length=255, blank=False, verbose_name="Banner Name")
	text = models.CharField(max_length=255, blank=True, default=None, verbose_name="Banner Text")
	image = models.ImageField(upload_to="images/banners/", blank=False, verbose_name="Banner Image")
	order = models.IntegerField(default=1, blank=True, verbose_name="Banner Order")
	link = models.CharField(max_length=255, blank=True, verbose_name="Banner Link")
	status = models.BooleanField(default=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = "Banners"
		verbose_name = "Banner"
		ordering = ['order']

	def __str__(self):
		return self.name

class Pages(models.Model):
	page_id = models.AutoField(primary_key=True)
	page_name = models.CharField(max_length=250, blank=False, verbose_name="Page Name")
	page_title = models.CharField(max_length=250, blank=False, verbose_name="Page Title")
	page_slug = models.SlugField(max_length=500, unique=True, blank=True, verbose_name="Page Slug URL")
	page_meta_title = models.CharField(max_length=250, blank=True, verbose_name="Meta Title")
	page_meta_keywords = models.TextField(default='', verbose_name="Meta Keywords")
	page_meta_description = models.TextField(default='', verbose_name="Meta Description")
	page_header = models.CharField(max_length=150, blank=True, verbose_name="Page Header")
	page_header_image = models.ImageField(upload_to='images/page_headers', blank=True, null=True, verbose_name="Page Header Image")
	page_content = RichTextUploadingField(null=True, blank=True, verbose_name="Page Content")
	page_status = models.BooleanField(verbose_name="Status", default=True)
	page_created_on = models.DateTimeField(auto_now_add=True)
	page_updated_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = "Pages"
		verbose_name = "Page"
		# ordering = ['page_order']

	def save(self, *args, **kwargs):
		if not self.page_slug:
			slug = slugify(self.page_name)
			while True:
				try:
					page = Pages.objects.get(page_slug=slug)
					if page == self:
						self.page_slug = slug
						break
					else:
						slug = slug + '-'
				except:
					self.page_slug = slug
					break
		super(Pages, self).save(*args, **kwargs)

	def __str__(self):
		return self.page_name

	def get_absolute_url(self):
		return reverse("dynamic_page", kwargs={"slug": self.page_slug})

EMAIL_CHOICES = (
	('SSL', 'SSL'),
	('TLS', 'TLS'),
)

class System_Settings(SingleInstanceMixin, models.Model):
	system_id = models.AutoField(primary_key=True)
	system_title = models.CharField(max_length=250, verbose_name="System Title")
	system_description = models.TextField(verbose_name="Description of your Website", default='')
	system_logo = models.ImageField(upload_to='system', blank=True, null=True, verbose_name="System Logo")

	system_favicon = models.ImageField(upload_to='system', blank=True, null=True, verbose_name="System Favicon")
	system_shareicon = models.ImageField(upload_to='system', blank=True, null=True, verbose_name="System Shareicon")

	system_company = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="Company Name")
	system_emails = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="Contact Email's")
	system_mobiles = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="Contact Mobile's")
	system_address = models.TextField(verbose_name="Contact Address", default='')
	system_mapcanvas = models.TextField(verbose_name="Google Map Frame", default='')

	system_home_content = RichTextUploadingField(null=True, blank=True, verbose_name="Home Page Content")
	system_testimonials_header = models.CharField(max_length=250, blank=True, null=True, verbose_name="Home Testimonials Header")
	system_video_header = models.CharField(max_length=250, blank=True, null=True, verbose_name="Home Video Header")
	system_contact_page_header = models.ImageField(upload_to='contact', blank=True, null=True, verbose_name="Contact Page Header")
 
	system_facebook = models.CharField(max_length=250, blank=True, null=True, verbose_name="Facebook Link")
	system_twitter = models.CharField(max_length=250, blank=True, null=True, verbose_name="Twitter Link")
	system_youtube = models.CharField(max_length=250, blank=True, null=True, verbose_name="Youtube Link")
	system_google = models.CharField(max_length=250, blank=True, null=True, verbose_name="Google Link")
	system_insta = models.CharField(max_length=250, blank=True, null=True, verbose_name="Insta Link")
	system_linkedin = models.CharField(max_length=250, blank=True, null=True, verbose_name="Linkedin Link")

	system_email_smtp = models.BooleanField(default=False, verbose_name="Email SMTP")
	system_email_use = models.CharField(max_length=250, blank=True, null=True, default='SSL', verbose_name="Email Use", choices=EMAIL_CHOICES)
	system_email_host = models.CharField(max_length=250, blank=True, null=True, verbose_name="Email Host")
	system_email_user = models.CharField(max_length=250, blank=True, null=True, verbose_name="Email User")
	system_email_pass = models.CharField(max_length=250, blank=True, null=True, verbose_name="Email Pass")
	system_email_port = models.CharField(max_length=250, blank=True, null=True, default='465', verbose_name="Email Port")

	system_payu_key = models.CharField(max_length=250, blank=True, null=True, verbose_name="PayU Key")
	system_payu_salt = models.CharField(max_length=250, blank=True, null=True, verbose_name="PayU Salt")
	system_payu_header = models.CharField(max_length=250, blank=True, null=True, verbose_name="PayU Auth Header")
	system_payu_url = models.CharField(max_length=250, blank=True, null=True, default='https://sandboxsecure.payu.in/_payment', verbose_name="PayU URL")

	system_android_server_key = models.CharField(max_length=250, blank=True, null=True, verbose_name="Server Key")
	system_android_sender_id = models.CharField(max_length=250, blank=True, null=True, verbose_name="Sender ID")
	system_android_app_name = models.CharField(max_length=250, blank=True, null=True, verbose_name="App Name")
	system_android_app_url = models.URLField(max_length=250, blank=True, null=True, verbose_name="App or Playstore URL")

	system_sms_url = models.TextField(blank=True, null=True, default='', verbose_name="SMS Gateway URL")
	system_sms_domain = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="SMS Domain URL")
	system_sms_username = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="SMS Username")
	system_sms_password = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="SMS Password")
	system_sms_senderid = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="SMS Sender ID")
	system_sms_username_var = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="SMS Username Variable")
	system_sms_password_var = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="SMS Password Variable")
	system_sms_mobile_var = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="SMS Mobile Variable")
	system_sms_message_var = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="SMS Message Variable")
	system_sms_senderid_var = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="SMS senderId Variable")
	system_sms_type_var = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="SMS Type Variable")
	system_sms_type_val = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="SMS Type Value")
	system_sms_other_var = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="SMS Other Variable")
	system_sms_other_val = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="SMS Other Value")
	system_sms_other1_var = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="SMS Other1 Variable")
	system_sms_other1_val = models.CharField(max_length=250, blank=True, null=True, default='', verbose_name="SMS Other1 Value")
 
	system_analytics = models.TextField(verbose_name="Google or Alexa analytics script", default='', blank=True, null=True)

	system_status = models.BooleanField(default=True)
	system_created_on = models.DateTimeField(auto_now_add=True)
	system_updated_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = "System Settings"
		verbose_name = "System Setting"

	def __str__(self):
		return "%s" % self.system_title

class MenuBarItems(models.Model):
	parent_id = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, verbose_name="Parent Menu")
	name = models.CharField(max_length=250, blank=False, verbose_name="Name")
	title = models.CharField(max_length=250, blank=False, default='', verbose_name="Title")
	link = models.CharField(max_length=250, blank=False, verbose_name="Link")
	item_class = models.CharField(max_length=250, blank=True, null=True, verbose_name="Class")
	order = models.IntegerField(null=True, default=1)
	status = models.BooleanField(default=True)
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = "Menu Bar Items"
		verbose_name = "Menu Bar Item"
		ordering = ['order']

	def __str__(self):
		return self.name

class UserDetails(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	parent = models.ForeignKey("self", on_delete=models.SET_NULL, null=True, blank=True)
	phone = models.CharField(max_length=15, null=True, blank=True, verbose_name="Mobile No. +91")
	address = models.TextField(verbose_name="Address", default='')
	state = models.CharField(max_length=100, verbose_name="State", default='')
	city = models.CharField(max_length=100, verbose_name="City", default='')
	pin_code = models.PositiveIntegerField(blank=True, null=True, verbose_name="Pin Code")

	def __str__(self):
		return self.user.username + ' - ' + self.user.email

class InOutLogEntry(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	action = models.CharField(max_length=64)
	username = models.CharField(max_length=256, null=True)
	session_key = models.CharField(max_length=100, blank=True, null=True)

	ip = models.CharField(max_length=250, blank=True, null=True)
	browser = models.CharField(max_length=250, blank=True, null=True)
	bVersion = models.CharField(max_length=250, blank=True, null=True)
	os = models.CharField(max_length=250, blank=True, null=True)
	device = models.CharField(max_length=250, blank=True, null=True)
	ipType = models.CharField(max_length=250, blank=True, null=True)
	hostName = models.CharField(max_length=250, blank=True, null=True)
	ua = models.CharField(max_length=250, blank=True, null=True)
	url = models.CharField(max_length=250, blank=True, null=True)
	servername = models.CharField(max_length=250, blank=True, null=True)
	v_date = models.CharField(max_length=250, blank=True, null=True)
	domain = models.CharField(max_length=250, blank=True, null=True)
	referrer = models.CharField(max_length=250, blank=True, null=True)

	ip_address = models.GenericIPAddressField(blank=True, null=True, verbose_name="Ip Address")
	ip_location = models.CharField(max_length=250, blank=True, null=True, default=None, editable=False, verbose_name="Ip Location")
	created_on = models.DateTimeField(auto_now_add=True)
	updated_on = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

	def __str__(self):
		return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

	class Meta:
		verbose_name_plural = "In Out Log Entries"
		verbose_name = "In Out Log Entry"

@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
	ip = request.META.get('REMOTE_ADDR')
	log_entry = InOutLogEntry(username=user.username, user=user, session_key=request.session.session_key, action='logged_in', ip=ip)
	ip_address = get_client_ip(request)
	location_data = get_client_location(ip_address)
	log_entry.session_key=request.session.session_key
	log_entry.ip_address = ip_address
	log_entry.ip_location = location_data
	log_entry.browser = request.user_agent.browser.family
	log_entry.bVersion = request.user_agent.browser.version_string
	log_entry.os = request.user_agent.os.family +' '+request.user_agent.os.version_string
	log_entry.device = request.user_agent.device.family
	if 'HTTP_USER_AGENT' in request.META:
		log_entry.ua = request.META['HTTP_USER_AGENT']
	if 'HTTP_HOST' in request.META:
		log_entry.hostName = request.META['HTTP_HOST']
	if 'SERVER_NAME' in request.META:
		log_entry.servername = request.META['SERVER_NAME']
	if 'HTTP_REFERER' in request.META:
		log_entry.referrer = request.META['HTTP_REFERER']
	if 'QUERY_STRING' in request.META:
		log_entry.url = request.META['QUERY_STRING']
	if 'PATH_INFO' in request.META:
		log_entry.domain = request.META['PATH_INFO']
	log_entry.save()


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
	ip = request.META.get('REMOTE_ADDR')
	log_entry = InOutLogEntry(username=user.username, user=user, session_key=request.session.session_key, action='logged_out', ip=ip)
	ip_address = get_client_ip(request)
	location_data = get_client_location(ip_address)
	log_entry.session_key=request.session.session_key
	log_entry.ip_address = ip_address
	log_entry.ip_location = location_data
	log_entry.browser = request.user_agent.browser.family
	log_entry.bVersion = request.user_agent.browser.version_string
	log_entry.os = request.user_agent.os.family +' '+request.user_agent.os.version_string
	log_entry.device = request.user_agent.device.family
	if 'HTTP_USER_AGENT' in request.META:
		log_entry.ua = request.META['HTTP_USER_AGENT']
	if 'HTTP_HOST' in request.META:
		log_entry.hostName = request.META['HTTP_HOST']
	if 'SERVER_NAME' in request.META:
		log_entry.servername = request.META['SERVER_NAME']
	if 'HTTP_REFERER' in request.META:
		log_entry.referrer = request.META['HTTP_REFERER']
	if 'QUERY_STRING' in request.META:
		log_entry.url = request.META['QUERY_STRING']
	if 'PATH_INFO' in request.META:
		log_entry.domain = request.META['PATH_INFO']
	log_entry.save()


@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):
	ip = request.META.get('REMOTE_ADDR')
	log_entry = InOutLogEntry(username=credentials.get('username', None), session_key=request.session.session_key, action='login_failed', ip=ip)
	# log_entry = InOutLogEntry(action='user_login_failed', username=credentials.get('username', None))
	ip_address = get_client_ip(request)
	location_data = get_client_location(ip_address)
	log_entry.ip_address = ip_address
	log_entry.ip_location = location_data
	log_entry.browser = request.user_agent.browser.family
	log_entry.bVersion = request.user_agent.browser.version_string
	log_entry.os = request.user_agent.os.family +' '+request.user_agent.os.version_string
	log_entry.device = request.user_agent.device.family
	if 'HTTP_USER_AGENT' in request.META:
		log_entry.ua = request.META['HTTP_USER_AGENT']
	if 'HTTP_HOST' in request.META:
		log_entry.hostName = request.META['HTTP_HOST']
	if 'SERVER_NAME' in request.META:
		log_entry.servername = request.META['SERVER_NAME']
	if 'HTTP_REFERER' in request.META:
		log_entry.referrer = request.META['HTTP_REFERER']
	if 'QUERY_STRING' in request.META:
		log_entry.url = request.META['QUERY_STRING']
	if 'PATH_INFO' in request.META:
		log_entry.domain = request.META['PATH_INFO']
	log_entry.save()

