# Bootstrap5 Repackaged for Django

[Bootstrap5](https://getbootstrap.com/docs/5.2/) packaged in a Django reusable app.

This package includes only the original JS and CSS files.


## Installation

    pip install django-js-lib-bootstrap5

## Usage

1. Add `"js_lib_bootstrap5"` to your `INSTALLED_APPS` setting like this::

       INSTALLED_APPS = [
           ...
           "js_lib_bootstrap5",
           ...
       ]

2. In your template use:
   
       {% load static %}
   
   ...
   
       <link rel="stylesheet" href="{% static "js-lib-bootstrap5/css/bootstrap.css" %}">

   ...
   
       <script src="{% static "js-lib-bootstrap5/js/bootstrap.js" %}"></script>
