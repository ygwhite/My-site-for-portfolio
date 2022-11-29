from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from authentication.forms import LoginForm, RegisterForm


def login_user(requests):
    context = {'login_form': LoginForm()}
    if requests.method == "POST":
        login_form = LoginForm(requests.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(requests, user)
                return redirect('index')
            else:
                context = {
                    'login_form': login_form,
                    'attention': f'The user with username {username} and password was not found!'
                }
        else:
            context = {
                'login_form': login_form
            }
    return render(requests, 'auth/login.html', context)


class RegisterView(TemplateView):
    template_name = 'auth/register.html'

    def get(self, request):
        user_form = RegisterForm()
        context = {'user_form': user_form}
        return render(request, 'auth/register.html', context)

    def post(self, request):
        user_form = RegisterForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('index')

        context = {'user_form': user_form}
        return render(request, 'auth/register.html', context)


def logout_user(requests):
    logout(requests)
    return redirect('index')
