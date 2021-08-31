from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from my_blog import settings

urlpatterns = [
    path('',views.home,name='home'),
    path('contact/',views.contact,name='contact'),
    path('about/',views.about,name='about'),
    path('bloghome/',views.bloghome,name='bloghome'),
    path('search/',views.search,name='search'),
    path('postComment/', views.postComment, name="postComment"),
    path('likepost/', views.likepost, name='likepost'),
    path('likeproject/', views.likeproject, name='likeproject'),
    path('blogpost/<str:slug>',views.blogpost,name='blogpost'),

    path('handlelogout/', LogoutView.as_view(next_page=settings.LOGOUT_REDIRECT_URL), name='logout'),

    path('projects/',views.projects,name='projects'),
    path('projects/<str:slug>',views.project,name='project'),
    path('codebook/',views.codebook,name="codebook"),

    path('python/',views.pythonhome,name='pythonhome'),
    path('python/<str:slug>',views.pythonpost,name='pythonhome')
]
