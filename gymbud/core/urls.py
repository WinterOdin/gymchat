
from __future__ import unicode_literals, absolute_import
from django.urls import path, re_path, include
from django.contrib import admin
from django.views.generic import TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.conf.urls.static import static



from typing import List




urlpatterns = [
    re_path('admin/', admin.site.urls),
    
    re_path(r'', include('chat.urls', namespace='chat')),
    path('', login_required(TemplateView.as_view(template_name='base.html')), name='home'),

    path('auth/', include('user_mgmt.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
