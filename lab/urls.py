from django.conf.urls import url
from . import views
app_name='lab'
urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^taskindex/$',views.task_index,name='task_index'),
    url(r'^submittedtask/(?P<task>.*)/$',views.submitted_task,name='submitted_task'),
    url(r'^pausetask/$',views.pause_task,name='pause_task'),
    url(r'^resettask/(?P<task>.*)/$',views.reset_task,name='reset_task'),
    url(r'^processtask/(?P<task>.*)/$',views.process_task,name='process_task'),
    url(r'^patientindex/$',views.patient_index,name='patient_index'),
    url(r'^patientdetail/(?P<patient>.*)/$',views.patient_detail,name='patient_detail'),
    url(r'^patient/addsample/(?P<patient>.*)/$',views.patient_addsample,name='patient_addsample'),
    url(r'^sampleindex/$',views.sample_index,name='sample_index'),
    url(r'^search',views.search,name='search'),
    ]