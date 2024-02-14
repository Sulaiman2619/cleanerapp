

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .admin_resources import UserResource
from .models import *


class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(Cleaner, ImportExportModelAdmin)
admin.site.register(Building, ImportExportModelAdmin)
admin.site.register(Room, ImportExportModelAdmin)
admin.site.register(Work, ImportExportModelAdmin)
admin.site.register(WorksData, ImportExportModelAdmin)
admin.site.register(Staff, ImportExportModelAdmin)
admin.site.register(Checker, ImportExportModelAdmin)