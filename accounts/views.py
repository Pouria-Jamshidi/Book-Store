
from django.shortcuts import render,redirect,get_object_or_404
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from accounts.forms import Register_form, LoginForm


class RegisterView(View):
    def get(self, request):
        form = Register_form()
        return render(request, 'accounts/register.html', {'register_form': form})

    def post(self, request):
        form = Register_form(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, f'اکانت شما به نام کاربری {new_user.username} ساخته شد!')
            return redirect('home')
        return render(request, 'accounts/register.html', {'register_form': form})

class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request,'accounts/login.html', {'login_form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(username=data.get('username'), password=data.get('password'))
            if user:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request,'کاربری با این مشخصات یافت نشد')
        return render(request, 'accounts/login.html', {'login_form': form})


def logout_view(request):
    logout(request)
    messages.success(request,'شما با موفقیت خارج شدید')
    return redirect('home')