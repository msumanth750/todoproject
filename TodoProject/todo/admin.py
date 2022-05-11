from django.contrib import admin
from .models import Todo

from django.contrib.auth.models import User,Group
from import_export.admin import ImportExportModelAdmin

# Register your models here.

'''class TodoAdmin(admin.ModelAdmin):
    list_display =('Title','Description','Datetime','Status','CreatedAt','ModifiedAt')
'''
@admin.register(Todo)
class TodoAdmin(ImportExportModelAdmin):
    list_display =('Title','Description','Datetime','Status','CreatedAt','ModifiedAt')
    search_fields = ('Title','Datetime')
    list_filter = ['Datetime','Status']

#admin.site.register(Todo,TodoAdmin)

admin.site.unregister(User)
admin.site.unregister(Group)
