Title: Django admin template structure
Date: 2016-10-16
Category: Django
Tags: python, django-admin, django-admin templates
Summary: Today we will see how template inheritance works inside the Django admin contribution package
Description: Analytical representation of the Django admin templates inheritance. How these templates work together.
Author: Nick Mavrakis
Status: published

As you all (probably) know, [Django](https://www.djangoproject.com/) is a magnificent Web framework to build the website of your dreams. There is a plethora of tutorials, how-to's, getting-started, django-for-dummies out there in the internet-wild. I am not going to show you the `Django` basics ([`models`](https://docs.djangoproject.com/en/dev/topics/db/models/), [`views`](https://docs.djangoproject.com/en/dev/topics/http/views/), [`templates`](https://docs.djangoproject.com/en/dev/ref/templates/) or [`forms`](https://docs.djangoproject.com/en/dev/ref/forms/) to name a few). I just want to share with you the template inheritance of the incredible [Django admin contribution package](https://docs.djangoproject.com/en/dev/ref/contrib/admin/).

At this time of writing, I am dreaming of a much more appealing admin interface which is based on the super-fancy [AdminLTE](https://almsaeedstudio.com/) template (there is a free version you can download, under the MIT License -- more about licences [here](http://choosealicense.com/)). But in order to adopt the new-dreamed template in my own project I must understand the template inheritance workflow of the built-in `Django` admin app.

I know there is a package, already out there ([django-adminlte-templates](https://github.com/StephenPCG/django-adminlte-templates)), that offer you the capability of using this admin template but I wanted to deeply understand how the `Django` admin template system is assembled and working so flawlessly. Lets get to work:


# The core ones

In this section we will describe briefly, the core HTML templates where the rest inherit from. If you do not have `Django` installed (!) or you're bored enough right now to navigate to the actual path where these templates are stored in your machine, here is `Django`'s admin [github source for the templates](https://github.com/django/django/tree/master/django/contrib/admin/templates) (you're one click away!).

As you can see there are two folders `admin` and `registration`. In the rest of this article we will assume that we are working under the `admin` directory, unless stated otherwise where we will be under the `registration` directory.

## base.html

As [Ane Brun](http://anebrun.com/) says in her song [One](https://www.youtube.com/watch?v=qMCQgb1YxI8):
> It all starts somewhere, it all starts with one

The root of the `Django` admin templates is **this file** and is located inside the `Django` folder that you installed via your [preferred method](https://docs.djangoproject.com/en/dev/intro/install/#install-django).
Assuming that:

+ you **are using** `virtualenv`
+ you **are using** Linux and
+ your `.virtualenvs` folder is inside your `$HOME` directory (note the `.` dot in front - indicates a hidden file. Press `Ctrl+H` to view hidden files)

then you will find this file following this path: `$HOME/.virtualenvs/<your_virtual_env_name>/lib/python<your_version_of_python>/site-packages/django/contrib/admin/templates/admin`
Easy eh?

Inside the `admin` folder you will find all the templates `Django` admin uses, to present itself. Nothing inherits directly from this file (in other words, there is no template which has this line at the top: `{% extends "admin/base.html" %}`) except from the `base_site.html` file.


## base_site.html

This is the only file that [extends](https://docs.djangoproject.com/en/dev/ref/templates/builtins/#extends) the *one* file (the root, the `base.html` file). I believe, until now you are following along.
Every other template file extends this one (see the graph [below](#dj-admin-diagram) for a better understanding). What? An exception? Oh, yes! Let me rephrase it:
Every other template file extends this one except from the `app_index.html` file which extends `index.html` which in turn extends `base_site.html` which (finally) extends `base.html`. This would be the longest *chain of extends* you will find in the `Django` admin templates.


## index.html

This file is just used as a base template for the `app_index.html` file. No other file extends `index.html`. Only the `app_index.html` extends `index.html`.


# Rest of the templates

Every other single template (apart from the ones mentioned above) either extends the `base_site.html` or act as standalone ready to be [*included*](https://docs.djangoproject.com/en/dev/ref/templates/builtins/#std:templatetag-include) somewhere (for example `actions.html`).


# URL-Template file relationship

In this section we will see which template file is actually called under a particular admin URL. We are assuming that inside your [URLconf](https://docs.djangoproject.com/en/dev/topics/http/urls/) file (also known as `urls.py`) the string `admin` is the one that you have chosen to visit the admin website. For example, if your site is `mywebsite.com` and this line is in your `urlpatterns` variable under `urls.py`: `url(r'^admin/', include(admin.site.urls)),` then you should visit the magnificent admin website at `mywebsite.com/admin/`.

+ URL: **`yourwebsite.com/<app_label>/<model_name>/`**, Template: **`change_list.html`**
    + Inside the template `change_list.html` the following templates are *included*: `change_list_results.html`, `actions.html` and `pagination.html`

| URL (yourwebsite.com/admin/...)          | Template                  | Comments                                            |
| -----------------------------------------|---------------------------|-----------------------------------------------------|
| `''`                                     | `index.html`              | The admin home page                                 |
| `<app_label>/`                           | `app_index.html`          | You have clicked on the name of the app (not model) |
| `<app_label>/<model_name>/`              | `change_list.html`&#185;  | You have clicked on the name of a model             |
| `<app_label>/<model_name>/<pk>/change/` `<app_label>/<model_name>/add/` | `change_form.html`&#178;  | You have clicked on an object to change it |
| `<app_label>/<model_name>/<pk>/history/` | `object_history.html`  | You have clicked on the HISTORY button to see the object's history |
| `<app_label>/<model_name>/`              | `delete_confirmation.html`&#179; | You have checked **one** object, selected *Delete selected <models_name>* and pressed *Go* |
| `<app_label>/<model_name>/`              | `delete_selected_confirmation.html`&#179; | You have checked **multiple** objects, selected *Delete selected <models_name>* and pressed *Go* |
| `login/`                                 | `login.html` | You requested to login |
| `password_change/`                       | `registration/password_change_form.html` | You requested to change your password |
| `logout/`                                | `registration/logged_out.html` | You requested to logged out |

&#185; Inside the template `change_list.html` these templates are used:

+ `change_list_results.html` (to show the objects of this model - entries in the database, if you like)
+ `actions.html` (to show the *actions* `div` which contains the default action `Delete` and any other of your own)
+ `pagination.html` (for the pagination across your objects)
+ `date_hierarchy.html` (only if the [`date_hierarchy`](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.date_hierarchy) is used)
+ `filter.html` (only if the [`list_filter`](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.list_filter) is used)
+ `search_form.html` (only if the [`search_fields`](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.search_fields) is used)

&#178; Inside the template `change_form.html` these templates are used:

+ `edit_inline/stacked.html` and `edit_inline/tabular.html` (if the [`StackedInline` or `TabularInline`](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#inlinemodeladmin-objects) is used)
+ `related_widget_wrapper.html` (again, if an inline is used)
+ `includes/fieldset.html` (if the [`fieldsets`](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.fieldsets) or/and an inline is used)
+ `submit_line.html` (in order to show the bottom - or [top](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.save_on_top) - `div` of the *Delete*, *Save and add another`*, *Save and continue editing* and *Save* buttons)
+ `prepopulated_fields_js.html` (if the [`prepopulated_fields`](https://docs.djangoproject.com/en/dev/ref/contrib/admin/#django.contrib.admin.ModelAdmin.prepopulated_fields) is used)

&#179; Inside the templates `delete_confirmation.html` and `delete_selected_confirmation.html` the `includes/object_delete_summary.html`template is used.

<br>

<figure>
<img id="dj-admin-diagram" alt="Django admin template inheritance diagram" src="/images/django_admin_template_structure/admin_template_inheritance.jpg">
<figcaption>Django admin template inheritance diagram</figcaption>
</figure>
