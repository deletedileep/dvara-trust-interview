from django.conf.urls import url, include
from . import views
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
urlpatterns = [

    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    # url(r'^login/$', login, {'template': 'login_11.html'}, name='login_11'),
    url(r'^login/$', LoginView.as_view(template_name='login_11.html'), name='login'),
    # url(r'^logout/$', logout, {'template_name': 'logout_11.html'}, name='logout_11'),
    url(r'^logout/$', LogoutView.as_view(template_name='logout_11.html'), name='logout_11'),
    # url(r'^change_password/$', views.change_password, name='change_password'),

    url(r'^cms-banners/$', views.banners_view, name='banners_view'),
    url(r'^cms-banners/add/$', views.add_banner, name='add_banner'),
    url(r'^cms-banners/(?P<pk>[0-9]+)/edit/$', views.edit_banner, name='edit_banner'),
    url(r'^cms-banners/(?P<pk>[0-9]+)/delete/$', views.delete_banner, name='delete_banner'),

    url(r'^cms-pages/$', views.pages_view, name='pages_view'),
    url(r'^cms-pages/add/$', views.add_page, name='add_page'),
    url(r'^cms-pages/(?P<pk>[0-9]+)/edit/$', views.edit_page, name='edit_page'),
    url(r'^cms-pages/(?P<pk>[0-9]+)/delete/$', views.delete_page, name='delete_page'),
    # url(r'^cms-pages/(?P<pk>[0-9]+)/details/$', views.view_page_details, name='view_page_details'),

    url(r'^cms-menubars/$', views.menubars_view, name='menubars_view'),
    url(r'^cms-menubars/add/$', views.add_menubar_link, name='add_menubar_link'),
    url(r'^cms-menubars/(?P<pk>[0-9]+)/edit/$', views.edit_menubar_link, name='edit_menubar_link'),
    url(r'^cms-menubars/(?P<pk>[0-9]+)/delete/$', views.delete_menubar_link, name='delete_menubar_link'),

    url(r'^system_settings/$', views.system_settings_view, name='system_settings_view'),
    url(r'^system_settings/(?P<pk>[0-9]+)/edit_site/$', views.edit_site_settings, name='edit_site_settings'),
    url(r'^system_settings/(?P<pk>[0-9]+)/edit_email/$', views.edit_email_settings, name='edit_email_settings'),
    url(r'^system_settings/(?P<pk>[0-9]+)/edit_payment/$', views.edit_payment_settings, name='edit_payment_settings'),
    url(r'^system_settings/(?P<pk>[0-9]+)/edit_sms/$', views.edit_sms_settings, name='edit_sms_settings'),
    url(r'^system_settings/(?P<pk>[0-9]+)/edit_android/$', views.edit_android_settings, name='edit_android_settings'),

    url(r'^users/$', views.users_list_view, name='users_list_view'),
    url(r'^staff/$', views.staff_users_list_view, name='staff_users_list_view'),
    url(r'^public/$', views.public_users_list_view, name='public_users_list_view'),

    url(r'^users/add/$', views.add_user, name='add_user'),
    url(r'^users/(?P<pk>[0-9]+)/edit/$', views.edit_user, name='edit_user'),
    url(r'^users/(?P<pk>[0-9]+)/edit_pass/$', views.edit_user_pass, name='edit_user_pass'),
    url(r'^users/(?P<pk>[0-9]+)/delete/$', views.delete_user, name='delete_user'),
    url(r'^view_user_details/(?P<user_id>[0-9]+)$', views.view_user_details, name='view_user_details'),

    url(r'^ajax_active/$', views.ajax_active, name='ajax_active'),

]