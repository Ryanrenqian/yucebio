from django.conf.urls import url
from . import views
app_name='analyst'
urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(),
    url(),
    url(),
]