from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from .yasg import *

<<<<<<< HEAD
schema_url_patterns =[
    
    path("auth/", include("account.urls")),
    path("team/", include("team.urls")),
    path("room/", include("room.urls")),
]

schema_view = get_schema_view(
    openapi.Info(
        title="DoranDoran Open API",
        default_version="v1",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    patterns=schema_url_patterns,
)

urlpatterns = [
    
    path("auth/", include("account.urls")),
    path("team/", include("team.urls")),
    path("room/", include("room.urls")),
=======
schema_url_patterns = [
    path("auth/", include("account.urls")),
    path("room/", include("room.urls")),
    path("team/", include("team.urls")),
    path("reserve/", include("reserve.urls")),
]

schema_view = get_schema_view(
    openapi.Info(
        title="DoranDoran Open API",
        default_version="v1",
        terms_of_service="https://www.google.com/policies/terms/",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=schema_url_patterns,
)

urlpatterns = [
    path("auth/", include("account.urls")),
    path("room/", include("room.urls")),
    path("team/", include("team.urls")),
    path("reserve/", include("reserve.urls")),
>>>>>>> 022988459079668181a23f299d7fd1987ad08c70
    path(
        "swagger<str:format>",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("docs/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
