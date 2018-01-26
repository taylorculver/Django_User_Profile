from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required


from . import forms
from . import models


def home(request):
    return render(request, 'home.html')


@login_required(login_url='/accounts/sign_in/')
def profile(request, username):
    user = get_object_or_404(models.User, username=username)
    return render(request, 'accounts/profile.html', {'user': user})


@login_required
def edit_profile(request, username):
    user = get_object_or_404(models.User, username=username)
    user_form = forms.UserForm(instance=user)
    profile_form = forms.ProfileForm(instance=user.profile)

    if request.method == 'POST':
        user_form = forms.UserForm(instance=user, data=request.POST)
        profile_form = forms.ProfileForm(instance=user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return HttpResponseRedirect(user.get_absolute_url())
    return render(request, 'accounts/edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })


@login_required
def change_password(request, username):
    error_list = []
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            new = form.cleaned_data['new_password1']
            old = form.cleaned_data['old_password']
            uppers = [letter for letter in new if letter.isupper()]
            lowers = [letter for letter in new if letter.islower()]
            numbers = [letter for letter in new if letter.isdigit()]
            special_characters = "[~\!@#\$%\^&\*\(\)_\+{}\":;'\[\]]"
            specials = [letter for letter in new if letter in special_characters]
            if old == new:
                error_list.append(messages.error(request, "Password cannot be same as current password"))
            elif len(new) <= 14:
                error_list.append(messages.error(request, "Password must be a minimum length of 14 characters"))
            elif len(uppers) == 0 or len(lowers) == 0:
                error_list.append(messages.error(request, "Password must use both uppercase and lowercase letters"))
            elif len(numbers) == 0:
                error_list.append(messages.error(request, "Password must contain one or more numerical digits"))
            elif len(specials) == 0:
                error_list.append(messages.error(request, "Password must contain at least on special character"))
            else:
                user = form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return HttpResponseRedirect(reverse('accounts:profile', args=[username]))
        else:
            messages.error(request, 'Please correct error below.')
    else:
        print(error_list)
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})


def sign_in(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if form.user_cache is not None:
                user = form.user_cache
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(
                        reverse('accounts:profile', args=[user.username])  # TODO: go to profile
                    )
                else:
                    messages.error(
                        request,
                        "That user account has been disabled."
                    )
            else:
                messages.error(
                    request,
                    "Username or password is incorrect."
                )
    return render(request, 'accounts/sign_in.html', {'form': form})


def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(
                request,
                "You're now a user! You've been signed in, too."
            )
            return HttpResponseRedirect(reverse('accounts:profile', args=[user.username]))  # TODO: go to profile
    return render(request, 'accounts/sign_up.html', {'form': form})


@login_required
def sign_out(request):
    logout(request)
    messages.success(request, "You've been signed out. Come back soon!")
    return HttpResponseRedirect(reverse('home'))
