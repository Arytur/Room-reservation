"""room_reserv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from rooms.views import show_room, add_room, show_detail, modify_room, delete_room, room_reservation, room_search

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', show_room, name='index'),
    url(r'^room/new$', add_room),
    url(r'^room/(?P<id>[0-9]+)/$', show_detail),
    url(r'^room/modify/(?P<id>[0-9]+)/$', modify_room),
    url(r'^room/delete/(?P<id>[0-9]+)/$', delete_room),
    url(r'^reservation/(?P<id>[0-9]+)/$', room_reservation),
    url(r'^search', room_search, name='search'),
]
