from django.contrib import admin
from .models import MovieReport

class MovieReportAdmin(admin.ModelAdmin):
    list_display = ['title','name','post','created_time']
    fields = ['title','name', 'text', 'post']

admin.site.register(MovieReport, MovieReportAdmin)