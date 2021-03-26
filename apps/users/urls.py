from django.contrib.auth import views as auth_views
from django.urls import path

from apps.users.views import users_list, profile_view, follower_list, send_follow_request, cancel_follow_request, \
    accept_follow_request, delete_follow_request, unfollow, edit_profile, the_user_profile, search_users, register

urlpatterns = [
    # path('', include('feed.urls')),
    path('users_list/', users_list, name='users_list'),
    path('<slug>/', profile_view, name='profile_view'),
    path('followers/', follower_list, name='follower_list'),
    path('follow_request/send/<int:id>/', send_follow_request, name='send_follow_request'),
    path('follow_request/cancel/<int:id>/', cancel_follow_request, name='cancel_follow_request'),
    path('follow_request/accept/<int:id>/', accept_follow_request, name='accept_follow_request'),
    path('follow_request/delete/<int:id>/', delete_follow_request, name='delete_follow_request'),
    path('unfollow/<int:id>/', unfollow, name='unfollow'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('the_user_profile/', the_user_profile, name='the_user_profile'),
    path('search_users/', search_users, name='search_users'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),

    ####
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]


