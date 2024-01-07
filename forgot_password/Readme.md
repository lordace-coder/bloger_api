Welcome to drf_forgot_password
====================================

Installation
--------------


-  **This project isnt currently available on pypi so clone this project from github**

```console
    git clone https://github.com/lordace-coder/forgot_password.git
```

- **Place it in the root of your project,or in the same location as your manage.py**

- **Add it to your INSTALLED_APPS in your projects settings.py**
```python
    # settings.py
    INSTALLED_APPS = [
        ...
        'forgot_password'
    ]
```
- **Now add it to your project urls using include**
```python
    # urls.py
    from django.urls import include, path

    urlpatterns = [
        ...
        path('recovery/',include('forgot_password.urls')),
    ]

```
- **Your good to go HappyCoding**