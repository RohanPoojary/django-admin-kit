# Django Admin Kit

![Build Status](https://travis-ci.org/RohanPoojary/django-admin-kit.svg?branch=master)
![Docs Status](https://readthedocs.org/projects/django-admin-kit/badge/?version=latest)
![Coverage Status](https://coveralls.io/repos/github/RohanPoojary/django-admin-kit/badge.svg?branch=master)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Django admin kit is developed to provide additional functionalities to django that includes Multi Select Field, Add duplicate models and easier Ajax bindings.


# Compatibility

The project is compatible with Django 1.11+, Django 2.0+ and Python 3.5+
It is not compatible with Django-3.0 yet.

# Installation

The project can be installed by running command

    pip install django-admin-kit


# Configuration

The app name ``admin_kit`` should be put at the top of installed apps in django ``settings`` file.

    # settings.py

    INSTALLED_APPS = [
        'admin_kit',
        
        'django.contrib.admin',
        'django.contrib.auth',
        ...
    ]

This is because, Admin Kit overrides Django *change_form* template.

Then register the admin_kit app in root ``urls`` file
with name ``admin_kit``

    # urls.py

    from django.conf.urls import url
    import admin_kit
    
    urlpatterns = [
        ...
        url(r'^admin_kit/', admin_kit.site.urls, name="admin_kit"),
    ]


Start the server and hit ``/admin_kit/ping`` url response. You will get a ``PONG`` response
if configured correctly.

    
# Features

There are mainly three features Admin_Kit provides. For detailed features visit [documentation](https://django-admin-kit.readthedocs.io/)

## Duplicate Button

This is a default feature that is added right after successfull configuration of the app.

![Duplicate Button](https://raw.githubusercontent.com/RohanPoojary/django-admin-kit/master/docs/images/duplicate%20button.png)

This button is similar to ``Add Another`` button, but it initializes the fields with previously
filled data. It is also compatible with [django-nested-admin](https://github.com/theatlantic/django-nested-admin). This button is only for inlined fields.

## New Fields

Proviedes new fields like MultiSelect and SelectField with supports ajax features.

## Ajax Features

There is also features to bind your model fields from APIs via Ajax requests.

# Documentation

For documentation go to https://django-admin-kit.readthedocs.io/

# License

The project is lincensed under MIT License. Please go through ``LICENSE`` file in the root folder.
