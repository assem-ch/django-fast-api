from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render
from django.conf import settings

def foo_view(request):
    if hasattr(settings, 'FOO_SETTING'):
        return render(request, template_name="foo.html", context={'data': {}})
    else:
        raise ImproperlyConfigured('You should define FOO_SETTING in your settings')
