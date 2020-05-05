from django.urls import path

from . import views
 
app_name = 'post'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    #path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    #path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    #path('tag/<int:pk>/', views.TagView.as_view(), name='tag'),
    #path('search/', views.search, name='search'),
]