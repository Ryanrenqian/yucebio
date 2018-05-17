from django.conf.urls import url

from . import views
app_name='projecymanaa'
urlpatterns = [
    url(r'^$',views.index,name='index'),
    url(r'^patientindex/(?P<key>\w+)/$', views.patientindex,name='patient'),
    url(r'^patient/(?P<patient_id>[0-9]+)/$', views.patientdetail,name='patientdetail'),
    url(r'^addproject/(?P<patient_id>[0-9]+)/$', views.addproject,name='addproject'),
    url(r'^addinfo/(?P<patient_id>[0-9]+)/$', views.addinfo,name='addinfo'),
    url(r'^projectindex/$', views.projectindex,name='project'),
    url(r'^project/(?P<project_id>\w+)/$', views.projectdetail,name='projectdetail'),
    url(r'^product/$',views.product,name='product'),
    url(r'^addproduct/$',views.addproduct,name='addproduct'),
    url(r'^checkorder/(?P<project_id>\w+)/$',views.ordercheck,name='ordercheck'),
    url(r'^pause/(?P<project_id>\w+)/$',views.pause,name='pause')
]
