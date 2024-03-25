from django.urls import path
from . import views
from base.views import ChangePasswordView


urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<str:pk>', views.blog, name='blog'),
    path('create_blog', views.create_blog, name='create_blog'),
    path('update_blog/<str:pk>', views.update_blog, name='update_blog'),
    path('delete_blog/<str:pk>', views.delete_blog, name='delete_blog'),
    path('login', views.login_user, name='login'),
    path ('logout', views.Logout, name='logout'),
    path('register', views.register, name='register'),
    path('history', views.user_history, name='history'),
    path('delete_read_history/<str:pk>', views.delete_read_history, name='delete_read_history'),
    path('user-profile', views.profile, name='user-profile'),
    path('update-user', views.updateUser, name='update-user'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]