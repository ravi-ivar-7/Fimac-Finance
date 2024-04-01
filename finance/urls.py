"""
URL configuration for finance project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
#added  to change admin name,title,etc.
admin.site.site_header = "FIMAC"
admin.site.site_title = "FIMAC Admin"
admin.site.index_title = "FIMAC"
#for media and static files purpose
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns = [
    path('accessfimacfinanceadmin/', admin.site.urls),
    path('',include('code_base.urls')),
    path('home',include('code_base.urls')),
    path('backtesting',include('backtesting.urls')),
    path('livetesting',include('livetesting.urls')),
]
urlpatterns+=staticfiles_urlpatterns()

#during development only
if settings.DEBUG:
    urlpatterns=urlpatterns+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns=urlpatterns+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)