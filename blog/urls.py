"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path

from .views import (
    PostList, PostDetail, PostCreate, PostUpdate, PostDelete
)

app_name = 'blog'
urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('post/new/', PostCreate.as_view(), name='post_new'),
    path('post/<slug:slug>/', PostDetail.as_view(), name='post_detail'),
    path('post/<slug:slug>/edit/', PostUpdate.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete', PostDelete.as_view(), name='post_delete'),
]
