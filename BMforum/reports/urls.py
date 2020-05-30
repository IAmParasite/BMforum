from django.urls import path
from . import views
app_name = 'reports'
urlpatterns = [
    path('report/<int:post_pk>', views.report, name='report'),
]
