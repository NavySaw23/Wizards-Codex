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
<<<<<<< HEAD
from projects.views import loginView, registrationView, logoutView,update_flower_count,get_user_data,clean_flower_data
from levels.views import lvl_view_1, lvl_view_2,lvl_view_4
=======
from projects.views import loginView, registrationView, logoutView,update_flower_count,get_user_data
from levels.views import lvl_view_1, lvl_view_2, lvl_view_3, lvl_view_4
>>>>>>> 10c6da84312c75ba637a049988c40377ce948dca

urlpatterns = [
    path('', home_view, name='home'),

    path('register/', registrationView, name='registration'),
    path('login/', loginView, name='login'),
    path('logout/', logoutView, name='logout'),
    path('level1/', lvl_view_1, name='lvl_1'),
    path('level2/', lvl_view_2, name='lvl_2'),
<<<<<<< HEAD
    path('level2/', lvl_view_2, name='lvl_4'),
=======
    path('level3/', lvl_view_3, name='lvl_3'),
    path('level4/', lvl_view_4, name='lvl_4'),
    path('update_flower_count/', update_flower_count, name='update_flower_count'),
>>>>>>> 10c6da84312c75ba637a049988c40377ce948dca
    path('get_user_data/', get_user_data, name='get_user_data'),
    path('update_flower_count/', update_flower_count, name='update_flower_count'),
    path('clean_flower_data/', clean_flower_data, name='clean_flower_data'),


    
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)    