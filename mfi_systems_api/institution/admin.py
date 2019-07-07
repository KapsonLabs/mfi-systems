from django.contrib import admin
from .models import Institution, InstitutionSettings, InstitutionStaff

admin.site.register(Institution)
admin.site.register(InstitutionSettings)
admin.site.register(InstitutionStaff)
