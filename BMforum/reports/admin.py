from django.contrib import admin
from .models import Report

class ReportAdmin(admin.ModelAdmin):
    list_display = ['title','name','post','created_time']
    fields = ['title','name', 'text', 'post']

admin.site.register(Report, ReportAdmin)