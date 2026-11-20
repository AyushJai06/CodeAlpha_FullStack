
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                'Your account has been created successfully!'
            )

            return redirect('home')

    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {
        'form': form
    })


def user_login(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = AuthenticationForm(
            request,
            data=request.POST
        )

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            next_url = request.GET.get('next')

            return redirect(next_url or 'home')

    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {
        'form': form
    })


def user_logout(request):

    if request.method == 'POST':
        logout(request)

    return redirect('home')


@login_required
def profile(request):

    return render(request, 'accounts/profile.html')
