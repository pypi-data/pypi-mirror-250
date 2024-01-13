Django Jinja Helpers
====================

Helpers for using django-jinja (https://github.com/niwinz/django-jinja) with

- django-crisp-forms
- django-webpack-loader

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django_jinja_helpers

Install the app

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'django_jinja_helpers',
    )

Usage
-----

Call ``render_bundle()`` in your template

.. code-block:: html

    <!DOCTYPE html>
    <html>
      <head>
        {{ render_bundle('styles', 'css') }}
      </head>

      <body>
      </body>
    </html>

Call ``crispy()`` in your template

.. code-block:: html

    <div class="container">
      {{ crispy(form) }}
    </div>
