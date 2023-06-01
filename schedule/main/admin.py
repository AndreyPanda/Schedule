from django.contrib import admin

from main.models import Specialization, Doctor, Client, Visit


class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('title', 'visit_duration', 'is_used')
    search_fields = ('title',)
    list_editable = ('is_used',)
    list_filter = ('is_used',)
    prepopulated_fields = {'slug': ('title',)}


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'fathers_name', 'specialization', 'is_active')
    search_fields = ('last_name',)
    list_editable = ('is_active',)
    list_filter = ('is_active', 'specialization')
    prepopulated_fields = {'slug': ('first_name', 'last_name', 'fathers_name')}


class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'fathers_name', 'birth_date', 'phone')
    search_fields = ('last_name',)


class VisitAdmin(admin.ModelAdmin):
    list_display = ('visit_datetime', 'doctor_to_visit', 'client_visiting')
    search_fields = ('visit_datetime__date', 'doctor_to_visit__last_name', 'client_visiting__last_name',)
    list_filter = ('doctor_to_visit',)


admin.site.register(Specialization, SpecializationAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(Visit, VisitAdmin)
