from django.contrib import admin

from main.models import Specialization, Doctor, Client


class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('title', 'visit_duration', 'is_used')
    search_fields = ('title',)
    list_editable = ('is_used',)
    list_filter = ('is_used',)


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'fathers_name', 'specialization', 'is_active')
    search_fields = ('last_name',)
    list_editable = ('is_active',)
    list_filter = ('is_active', 'specialization')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'fathers_name')
    search_fields = ('last_name',)


admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Client, ClientAdmin)
