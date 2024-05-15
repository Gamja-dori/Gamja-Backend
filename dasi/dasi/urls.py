from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

schema_view = get_schema_view(
    openapi.Info(
        title="Dasi",
        default_version='0.1.1',
        description="다시: 시니어 AI 매칭 인재풀의 API 문서입니다.",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="gamjadori15@gmail.com"), # 부가정보
        license=openapi.License(name="mit"),     # 부가정보
    ),
    url='https://api.dasi-expert.com',
    public=True,
    permission_classes=[permissions.AllowAny],
)

def health_check(request): # for aws alb target group
    return HttpResponse(status=200)

urlpatterns = [
    re_path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc-v1'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('resumes/', include('resume.urls')),
    path('recommends/', include('recommend.urls')),
    path('health/', health_check),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
