
from __future__ import unicode_literals, absolute_import
from django.urls import path, re_path, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
import debug_toolbar

from typing import List


schema_view = get_schema_view(
   openapi.Info(
      title="GymBud API",
      default_version='v1',
      description="API",
    #   terms_of_service="",
    #   contact=openapi.Contact(email=""),
    #   license=openapi.License(name=""),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)
swaggerpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


urlpatterns = [
    re_path('admin/', admin.site.urls),
    path('com/', include('chat.urls', namespace='chat')),
    path('chat/', TemplateView.as_view(template_name='base.html'), name='home'),
    path('locations/', include('locations.urls')),
    path('api/', include('user_mgmt.urls')),
    path('__debug__/', include(debug_toolbar.urls))



] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + swaggerpatterns
