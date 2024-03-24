from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<str:pk>', views.blog, name='blog'),
    path('create_blog', views.create_blog, name='create_blog'),
    path('update_blog/<str:pk>', views.update_blog, name='update_blog'),
    path('delete_blog/<str:pk>', views.delete_blog, name='delete_blog'),
    path('login', views.login_user, name='login'),
    path ('logout', views.Logout, name='logout'),
    path('register', views.register, name='register'),
]