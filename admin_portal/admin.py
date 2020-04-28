from django.contrib import admin
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin
from .models import *
admin.site.site_register = 'Admin Portal'

admin.site.site_header ='Institute Admin'
admin.site.site_title ='Online Exam'
admin.site.index_title ='Online Exam'


class InOutLogEntriesAdmin(ImportExportModelAdmin):
    list_display = ('action', 'username', 'device', 'os', 'browser', 'ip_address', 'ip_location', 'created_on')
    list_filter = ['action',]
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(InOutLogEntry, InOutLogEntriesAdmin)

class MenuBarItemsAdmin(ImportExportModelAdmin):
    list_display = ('name', 'parent_id', 'link', 'order', 'status', 'created_on')

admin.site.register(MenuBarItems, MenuBarItemsAdmin)

class PagesAdmin(ImportExportModelAdmin):
    list_display = ('page_name', 'page_title', 'page_slug', 'page_header', 'page_status', 'page_created_on')

admin.site.register(Pages, PagesAdmin)

class BannersAdmin(ImportExportModelAdmin):
    list_display = ('name', 'text', 'image', 'order', 'link', 'status', 'created_on')
admin.site.register(Banners, BannersAdmin)

admin.site.register(System_Settings)
class SingleInstanceAdminMixin(object):
    """Hides the "Add" button when there is already an instance."""
    def has_add_permission(self, request):
        num_objects = self.model.objects.count()
        if num_objects >= 1:
            return False
        return super(SingleInstanceAdminMixin, self).has_add_permission(request)


class ExampleAdmin(SingleInstanceAdminMixin, ImportExportModelAdmin):
    model = System_Settings