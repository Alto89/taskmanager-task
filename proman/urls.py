"""proman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView

from taskmanager.views import HomeView, TaskListView, ProfileDetailView, TaskCreateView, SubTaskCreateView, TaskUpdateView, SubTaskUpdateView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^tasks/$', TaskListView.as_view(), name='tasks'),
    url(r'^tasks/create-task/$', TaskCreateView.as_view(), name='create'),
    url(r'^tasks/(?P<pk>\d+)/$', TaskUpdateView.as_view(), name='detail'),
    url(r'^subtasks/(?P<pk>\d+)/$', SubTaskUpdateView.as_view(), name='subdetail'),
    url(r'^tasks/create-subtask/$', SubTaskCreateView.as_view(), name='createsub'),
    url(r'^user/$', ProfileDetailView.as_view(), name='user'),
    
]
