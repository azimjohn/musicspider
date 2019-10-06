from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


urlpatterns = [
    path('api/', include(('music.urls', 'music'))),
    path('', lambda request: HttpResponse('{"alive": true}')),
]
