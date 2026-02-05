
from django.shortcuts import render,redirect,get_object_or_404
from django.conf import settings
from django.views import View
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView, LogoutView
from accounts.forms import Register_form, Login_form
from sales.services import update_cart_cache


class RegisterView(View):
    def get(self, request):
        form = Register_form()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = Register_form(request.POST)
        if form.is_valid():
            new_user = form.save()
            messages.success(request, 'اکانت شما به نام کاربری {} ساخته شد!'.format(new_user.username))
            return redirect('login')
        return render(request, 'accounts/register.html', {'form': form})

class Login_view(LoginView):
    form_class = Login_form
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, 'شما قبلاً وارد شده‌اید')
            # check for next parameter
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)

            # fallback to default success_url
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):

        #  ===================== Remember me ======================
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)
        #  ================== End of Remember me ==================

        user = form.get_user()
        messages.success(self.request,'کاربر {} با موفقیت وارد شد'.format(user.username))

        # ======================================== To update the number of cart items in session when user logs in ===================================
        # return super().form_valid(form)
        response = super().form_valid(form) # performs the login adn save the http response in a variable
        update_cart_cache(self.request) # update the number of cart items
        return response # Return the saved http response
        # =================================================================================================================================


    def form_invalid(self, form):
        messages.error(self.request, 'کاربری با این مشخصات یافت نشد')
        return super().form_invalid(form)


class logout_view(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        messages.success(request,'شما با موفقیت خارج شدید')
        return super().dispatch(request,*args,**kwargs)