"""oshstudy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include(debug_toolbar.urls)),
    path('', include('main.urls')),
    path('accountprofile/', include('accountprofile.urls')),
    path('company/', include('company.urls')),
    path('contract/', include('contract.urls')),
    path('knowledge/', include('knowledge.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('study/', include('study.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('comments/', include('django_comments_xtd.urls')),
    path('quiz/', include('quiz.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
