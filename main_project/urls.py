from django.contrib import admin
from django.urls import path, include

import authentication
from . import view

urlpatterns = [
    path('', view.index, name='index'),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('shop/', include('shop.urls')),
]
