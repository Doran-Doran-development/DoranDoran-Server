from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from .views import TeamListCreateAPI, TeamRetrieveDestroyAPI


urlpatterns = [
    url(r"base", TeamListCreateAPI.as_view()),
    url(r"base/<int:pk>", TeamRetrieveDestroyAPI.as_view()),
]
