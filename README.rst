=================
Django UN Foo
=================
Description


Quick start
-----------

1. Install the lib: 

     pip install django-un-foo


1. Add "foo" to your ``INSTALLED_APPS`` setting like this::

    INSTALLED_APPS = [
        ...
        'un_foo',
        ...
    ]

2. Include the foo URLconf in your project ``urls.py`` like this::

    path('', include('un_foo.urls')),

3. Add this variable ``FOO_SETTING`` to ``settings.py``


4. You will find the foo api documentation in  `/foo/`.

