"""
URL configuration for WizCode project.

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

from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from home.views import home_view
# from login.views import login_view, postsign_view
from projects.views import loginView, registrationView, logoutView
from levels.views import lvl_view_1

urlpatterns = [
    path('', home_view, name='home'),

    path('register/', registrationView, name='registration'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('level1/', lvl_view_1, name='lvl_1'),
    
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    