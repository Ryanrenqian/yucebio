"""yucebio URL Configuration

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
from django.conf.urls import url, include
urlpatterns = [
#    url(r'^admin/',include('admin.urls')),
#    url(r'^analyst/',include('Analyst.urls')),
    url(r'^projectmanager/',include('ProjectManager.urls')),
    url(r'^lab/',include('lab.urls')),
#    url(r'^samplemanager/',include('SampleManager.urls')),
#    url(r'^experimentmanager/',include('ExperimentManager.urls')),
#    url(r'^login/',include('Login.urls')),
#    url(r'^projectchecker/',include('ProjectChecker.urls')),
]
