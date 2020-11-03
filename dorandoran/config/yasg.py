from django.conf.urls import url
from django.urls import path, include
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from drf_yasg import openapi

schema_url_patterns = [
]

schema_view = get_schema_view(
    openapi.Info(
        title='DoranDoran Open API',
        default_version='v1',
        description = 
        '''
        DoranDoran Open API 문서 페이지 입ㄴ다.
        본 서비스는 회의실 관리를 위해 만들어진 웹 서비스 입니다.
        ''',
        terms_of_service = "https://www.google.com/policies/terms",
        contact = openapi.Contact(email='hanbin8269@gmail.com'),
        license=openapi.License(name='DoranDoran'),
    ),
    validators=['flex'],
    public=True,
    permission_classes=(AllowAny,),
    patterns=schema_url_patterns,
)