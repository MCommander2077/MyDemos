"""
URL configuration for MTL_DJango project.

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
from django.urls import path
from index import views as index
from list import views as list
from info import views as info
from about import views as about

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index.view),
    path('list/', list.view),
    path('song/<int:song_id>', info.view),
    path('about/', about.view)

]
