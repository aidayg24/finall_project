import random

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models.following import FollowRequest
from .models.profile import Profile
from ..posts.models.post import Post

User = get_user_model()


@login_required
def users_list(request):
    """
        this view will form users list to help users to fined new followers.
        this list starts with adding our follower's followers who are not our followers
        and then other peoples.
    """
    users = Profile.objects.exclude(user=request.user)
    sent_follow_requests = FollowRequest.objects.filter(from_user=request.user)
    sent_to = []
    followers = []
    for user in users:
        follower = user.followers.all()
        for f in follower:
            if f in followers:
                follower = follower.exclude(user=f.user)
        followers += follower
    the_user_followers = request.user.profile.followers.all()
    for i in the_user_followers:
        if i in followers:
            followers.remove(i)
    if request.user.profile in followers:
        followers.remove(request.user.profile)
    random_list = random.sample(list(users), min(len(list(users)), 10))
    for r in random_list:
        if r in followers:
            random_list.remove(r)
    followers += random_list
    for i in the_user_followers:
        if i in followers:
            followers.remove(i)
    for se in sent_follow_requests:
        sent_to.append(se.to_user)
    context = {
        'users': followers,
        'sent': sent_to
    }
    return render(request, "users/users_list.html", context)


def follower_list(request):
    """
        display all the followers of the user

    """
    p = request.user.profile
    followers = p.followers.all()
    context = {
        'followers': followers
    }
    return render(request, "users/follower_list.html", context)


@login_required
def send_follow_request(request, id):
    """
        create a follow request

    """
    user = get_object_or_404(User, id=id)
    frequest, created = FollowRequest.objects.get_or_create(
        from_user=request.user,
        to_user=user)
    return HttpResponseRedirect('/users/{}'.format(user.profile.slug))


@login_required
def cancel_follow_request(request, id):
    """
        cancel the request that the user sent to others
    """
    user = get_object_or_404(User, id=id)
    frequest = FollowRequest.objects.filter(
        from_user=request.user,
        to_user=user).first()
    frequest.delete()
    return HttpResponseRedirect('/users/{}'.format(user.profile.slug))


@login_required
def accept_follow_request(request, id):
    """
        accept the follow request and add the followers to the user followers

    """
    from_user = get_object_or_404(User, id=id)
    frequest = FollowRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    user1 = frequest.to_user
    user2 = from_user
    user1.profile.followers.add(user2.profile)
    user2.profile.followers.add(user1.profile)
    if (FollowRequest.objects.filter(from_user=request.user, to_user=from_user).first()):
        request_rev = FollowRequest.objects.filter(from_user=request.user, to_user=from_user).first()
        request_rev.delete()
    frequest.delete()
    return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))


@login_required
def delete_follow_request(request, id):
    """
        delete the follow request
    """
    from_user = get_object_or_404(User, id=id)
    frequest = FollowRequest.objects.filter(from_user=from_user, to_user=request.user).first()
    frequest.delete()
    return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))


def unfollow(request, id):
    """
        unfollow a follower
    """
    user_profile = request.user.profile
    follower_profile = get_object_or_404(Profile, id=id)
    user_profile.followers.remove(follower_profile)
    follower_profile.followers.remove(user_profile)
    return HttpResponseRedirect('/users/{}'.format(follower_profile.slug))


@login_required
def profile_view(request, slug):
    p = Profile.objects.filter(slug=slug).first()
    u = p.user
    sent_follow_requests = FollowRequest.objects.filter(from_user=p.user)
    rec_follow_requests = FollowRequest.objects.filter(to_user=p.user)

    user_posts = Post.objects.filter(user_name=u)

    followers = p.followers.all()

    # is this user the user follower
    button_status = 'none'
    if p not in request.user.profile.followers.all():
        button_status = 'not_follower'

        # if the user has sent this user a follow request
        if len(FollowRequest.objects.filter(
                from_user=request.user).filter(to_user=p.user)) == 1:
            button_status = 'follow_request_sent'

        # if the user has received a follow request
        if len(FollowRequest.objects.filter(
                from_user=p.user).filter(to_user=request.user)) == 1:
            button_status = 'follow_request_received'

    context = {
        'u': u,
        'button_status': button_status,
        'followers_list': followers,
        'sent_follow_requests': sent_follow_requests,
        'rec_follow_requests': rec_follow_requests,
        'post_count': user_posts.count
    }

    return render(request, "users/profile.html", context)


def register(request):
    """
        this view is for register

    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now login!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def edit_profile(request):
    """
        editing both profile and user(forms!)

    """
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('the_user_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/edit_profile.html', context)


@login_required
def the_user_profile(request):
    """
        show the user profile

    """
    p = request.user.profile
    the_user = p.user
    sent_follow_requests = FollowRequest.objects.filter(from_user=the_user)
    rec_follow_requests = FollowRequest.objects.filter(to_user=the_user)
    user_posts = Post.objects.filter(user_name=the_user)
    followers = p.followers.all()

    # # is this user the user follower
    # button_status = 'none'
    # if p not in request.user.profile.followers.all():
    #     button_status = 'not_friend'
    #
    #     # if we have sent him a friend request
    #     if len(FollowRequest.objects.filter(
    #             from_user=request.user).filter(to_user=you)) == 1:
    #         button_status = 'follow_request_sent'
    #
    #     if len(FollowRequest.objects.filter(
    #             from_user=p.user).filter(to_user=request.user)) == 1:
    #         button_status = 'follow_request_received'

    context = {
        'u': the_user,
        # 'button_status': button_status,
        'followers_list': followers,
        'sent_follow_requests': sent_follow_requests,
        'rec_follow_requests': rec_follow_requests,
        'post_count': user_posts.count
    }

    return render(request, "users/profile.html", context)


@login_required
def search_users(request):
    query = request.GET.get('q')
    object_list = User.objects.filter(username__icontains=query)
    context = {
        'users': object_list
    }
    return render(request, "users/search_users.html", context)
