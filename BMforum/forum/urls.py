from django.urls import path #导入path函数
from .import views 	#从当前的目录下导入views模块
app_name = 'forum'
urlpatterns = [			#网址和处理函数的关系写在urlpatterns列表里面
    path('index/', views.IndexView.as_view(), name='index'),
    path('book_index/', views.BooksIndexView.as_view(), name='book_index'),	#第一个参数是网址，第二个参数是处理函数#第三个name 为传递的参数，这个参数的值作为处理函数index的别名（我也不太懂）
    #path('movies_index/', views.MoviesIndexView.as_view(), name='movie_index'),
    path('groups_index/', views.GroupsIndexView.as_view(), name='groups_index'),
    path('groups/<int:pk>', views.GroupPostView.as_view(), name='group_detail'),
    path('grouppost/<int:pk>', views.GroupDetailView.as_view(), name='group_detailmore'),
    path('books/<int:pk>/', views.PostDetailView.as_view(), name='book_detail'),
    path('movies_index/', views.MoviesIndexView.as_view(), name='movie_index'),
    path('topic/', views.TopicIndexView.as_view(), name='topic_index'),
    path('books/<int:pk>/', views.PostDetailView.as_view(), name='book_detail'),
    path('movies/<int:pk>/', views.MoviePostDetailView.as_view(), name='movie_detail'),
    path('topics/<int:pk>/', views.TopicPostDetailView.as_view(), name='topic_detail'),
    path('add/<int:group_id>', views.add_post, name='add'),
    #path('archives/<int:year>/<int:month>/', views.archive, name='archive'),
    #path('categories/<int:pk>/', views.CategoryView.as_view(), name='category'),
    #path('tag/<int:pk>/', views.TagView.as_view(), name='tag'),
    path('search/', views.search, name='search'),
    path('book_search/', views.book_search, name='book_search'),
    path('movie_search/', views.movie_search, name='movie_search'),
    path('group_search/', views.group_search, name='group_search'),
    path('group_post_search/', views.group_post_search, name='group_post_search'),
    path('topic_search/', views.topic_search, name='topic_search'),
    #path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('groups_index/<int:pk>', views.add_group, name='addgroup'),
    path('groups_index/<str:name>', views.add_groupmanager, name='addgroupmanager'),
    path(r'delete/<int:pk>/<int:pkk>',views.deleteGroupPost,name = 'delete_grouppost'),
    path(r'top/<int:pk>/<int:pkk>',views.topenGroupPost,name = 'topen_grouppost')
]
