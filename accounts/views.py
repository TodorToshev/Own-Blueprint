from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.utils.decorators import method_decorator
from functools import wraps


# Create your views here.


class persist_session_vars(object):
    """
    Some views, such as login and logout, will reset all session state.
    (via a call to ``request.session.cycle_key()`` or ``session.flush()``).
    That is a security measure to mitigate session fixation vulnerabilities.

    By applying this decorator, some values are retained.
    Be very aware what kind of variables you want to persist.
    """

    def __init__(self, vars):
        self.vars = vars

    def __call__(self, view_func):

        @wraps(view_func)
        def inner(request, *args, **kwargs):
            session_backup = {}
            for var in self.vars:
                try:
                    session_backup[var] = request.session[var]
                except KeyError:
                    pass

            # Call the original view
            response = view_func(request, *args, **kwargs)

            # Restore variables in the new session
            for var, value in session_backup.items():
                request.session[var] = value

            return response

        return inner


#no need to override this view, 'cart' doesn't get deleted on login or register.
# @method_decorator(persist_session_vars(['cart']), name='dispatch')
# class LoginView(auth_views.LoginView):
#     pass

@method_decorator(persist_session_vars(['cart']), name='dispatch')
class LogoutView(auth_views.LogoutView):
    pass


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect("blog:blog")
        messages.error(request, 'Registration failed.')
    else:
        form = UserRegistrationForm()
    return render(request, template_name='registration/registration.html', context={'form': form})
