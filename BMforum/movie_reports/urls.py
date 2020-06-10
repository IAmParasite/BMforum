from django.urls import path
from . import views
app_name = 'movie_reports'
urlpatterns = [
    path('movie_report/<int:post_pk>', views.report, name='movie_report'),
]
