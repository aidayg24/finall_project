"""nstagram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.users import views as user_views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.posts.urls')),

    path('users/', user_views.users_list, name='users_list'),
    path('users/<slug>/', user_views.profile_view, name='profile_view'),
    path('followers/', user_views.follower_list, name='follower_list'),
    path('users/follow-request/send/<int:id>/', user_views.send_follow_request, name='send_follow_request'),
    path('users/follow-request/cancel/<int:id>/', user_views.cancel_follow_request, name='cancel_follow_request'),
    path('users/follow-request/accept/<int:id>/', user_views.accept_follow_request, name='accept_follow_request'),
    path('users/follow-request/delete/<int:id>/', user_views.delete_follow_request, name='delete_follow_request'),
    path('users/unfollow/<int:id>/', user_views.unfollow, name='unfollow'),
    path('edit-profile/', user_views.edit_profile, name='edit_profile'),
    path('the_user_profile/', user_views.the_user_profile, name='the_user_profile'),
    path('search_users/', user_views.search_users, name='search_users'),
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
