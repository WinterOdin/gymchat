
from __future__ import unicode_literals, absolute_import
from django.urls import path, re_path, include
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static



from typing import List




urlpatterns = [
    re_path('admin/', admin.site.urls),
    
    path('com/', include('chat.urls', namespace='chat')),
    path('chat/', TemplateView.as_view(template_name='base.html'), name='home'),
    path('locations/', include('locations.urls')),
    path('auth/', include('user_mgmt.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
