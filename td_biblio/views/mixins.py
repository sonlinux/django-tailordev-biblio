import logging

from django.contrib.auth.decorators import login_required, user_passes_test

logger = logging.getLogger("td_biblio")


def superuser_required(function=None):
    """
    Decorator for views that checks that the user is a super user redirecting
    to the log-in page if necessary.

    Inspired by Django 'login_required' decorator
    """
    actual_decorator = user_passes_test(lambda u: u.is_superuser)
    if function:
        return actual_decorator(function)
    return actual_decorator


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class SuperuserRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(SuperuserRequiredMixin, cls).as_view(**initkwargs)
        return superuser_required(view)
