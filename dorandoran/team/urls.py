from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from .views import (
    TeamListCreateView,
    TeamRetrieveDestroyView,
    TeamJoinView,
    TeamOutView,
)


urlpatterns = [
    path(r"", TeamListCreateView.as_view()),
    path(r"<int:pk>", TeamRetrieveDestroyView.as_view()),
    path(r"join", TeamJoinView.as_view()),
    path(r"member/<team_id>/<email>", TeamOutView.as_view()),
]
