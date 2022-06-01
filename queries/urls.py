from django.urls import path

from . import views


def to_path(name):
    return path(name.replace('_', '-'), getattr(views, name), name=name)


urlpatterns = [
    path('', views.index),
    *list(map(to_path, views.__all__)),
]
