from django.conf.urls import url
from . import views
app_name='lab'
urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^task/index/$',views.task_index,name='task_index'),
    url(r'^task/submitted/(?P<task>.*)/$',views.submitted_task,name='submitted_task'),
    url(r'^task/pause/$',views.pause_task,name='pause_task'),
    url(r'^task/reset/(?P<task>.*)/$',views.reset_task,name='reset_task'),
    url(r'^task/process(?P<task>.*)/$',views.process_task,name='process_task'),
    url(r'^patient/index/$',views.patient_index,name='patient_index'),
    url(r'^patient/detail/(?P<patient>.*)/$',views.patient_detail,name='patient_detail'),
    url(r'^patient/addsample/(?P<patient>.*)/$',views.patient_addsample,name='patient_addsample'),
    url(r'^sample/index/$',views.sample_index,name='sample_index'),
    url(r'^search',views.search,name='search'),
    ]