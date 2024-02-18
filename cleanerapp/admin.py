

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .admin_resources import UserResource
from .models import *


class UserAdmin(ImportExportModelAdmin):
    resource_class = UserResource

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Cleaner)
class CleanerAdmin(ImportExportModelAdmin):
    list_display = ['full_name', 'user', 'sex', 'profile_image']
    search_fields = ['user__first_name', 'user__last_name', 'sex']

    def full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    full_name.short_description = 'Full Name'


@admin.register(Building)
class BuildingAdmin(ImportExportModelAdmin):
    list_display = ['name', 'total_floors']
    search_fields = ['name']

@admin.register(Room)
class RoomAdmin(ImportExportModelAdmin):
    list_display = ['room_name', 'building', 'floor_num']
    list_filter = ['building']
    search_fields = ['room_name', 'building__name', 'floor_num']

@admin.register(Work)
class WorkAdmin(ImportExportModelAdmin):
    list_display = ['work_name', 'cleaner', 'room', 'day']
    list_filter = ['day', 'cleaner', 'room']
    search_fields = ['work_name', 'cleaner__user__first_name', 'room__room_name', 'day']

@admin.register(WorksData)
class WorksDataAdmin(ImportExportModelAdmin):
    list_display = ['date', 'status', 'rating', 'work', 'comment', 'staff']
    list_filter = ['date', 'status']
    search_fields = ['work__work_name', 'status', 'staff']

@admin.register(Staff)
class StaffAdmin(ImportExportModelAdmin):
    list_display = ['user']
    search_fields = ['user__first_name', 'user__last_name']

@admin.register(Checker)
class CheckerAdmin(ImportExportModelAdmin):
    list_display = ['full_name', 'first_name', 'last_name']
    search_fields = ['first_name', 'last_name']

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = 'Full Name'