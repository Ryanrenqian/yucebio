from django.conf.urls import url

from . import views
app_name='projectmanager'
urlpatterns=[
    url(r'^$',views.index,name='index'),
    url(r'^project/pause/(?P<project>.*)$',views.project_pause,name='project_pause'),
    url(r'^project/stop/(?P<project>.*)$',views.stop_project,name='stop_project'),
    url(r'^project/add/(?P<project>.*)$',views.add_project,name='add_project'),
    url(r'^project/index/$', views.project_index, name='project_index'),
    url(r'^project/detail/(?P<project>.*)$', views.project_detail, name='project_detail'),
    url(r'^project/pay/(?P<project>.*)$', views.project_pay, name='project_pay'),
    url(r'^project/addtask/(?P<project>.*)$', views.project_add_task, name='project_add_task'),
    url(r'^project/declarelab/(?P<project>.*)$', views.project_declare_lab, name='project_declare_lab'),
    url(r'^project/declarejiedu/(?P<project>.*)$', views.project_declare_jiedu, name='project_declare_jiedu'),
    # url(r'^addexp/$',views.add_expproject,name='add_expproject'),
    # url(r'^addana/$',views.add_anaproject,name='add_anaproject'),
    # url(r'^addjiedu/$',views.add_report,name='add_report'),
    url(r'^search$',views.search,name='search'),
    url(r'^patient/index/$', views.patient_index, name='patient_index'),
    url(r'^patient/detail/(?P<patient>.*)$', views.patient_detail, name='patient_detail'),
    url(r'^patient/addtask/(?P<patient>.*)', views.patient_order, name='patient_order'),
    url(r'^patient/add$',views.add_patient,name='add_patient'),
    url(r'^patient/batchadd$',views.add_patient_batch,name='add_patient_batch'),
    # url(r'^projectaddlab/(?P<project>.*)$',views.project_add_lab,name='project_add_lab'),
    # url(r'^projectaddana/(?P<project>.*)$',views.project_add_ana,name='project_add_ana'),
    # url(r'^projectaddrep/(?P<project>.*)$',views.project_add_rep,name='project_add_rep'),

    url(r'^task/index/$',views.task_index,name='task_index'),
    url(r'^task/detail/(?P<task>\w+)$',views.task_detail,name='task_detail'),
    url(r'^task/labpause/(?P<task>\w+)$',views.task_pause_lab,name='task_pause_lab'),
    url(r'^task/anapause/(?P<task>\w+)$',views.task_pause_ana,name='task_pause_ana'),
    url(r'^task/jiedupause/(?P<task>\w+)$',views.task_pause_jiedu,name='task_pause_jiedu'),
    url(r'^task/reset/(?P<task>\w+)$',views.task_reset,name='task_reset'),
    url(r'^task/stop/(?P<task>\w+)$',views.task_stop,name='task_stop'),
    url(r'^task/distribute$',views.task_distribute,name='task_distribute'),
    url(r'^task/declarejiedu/(?P<task>\w+)$',views.declare_jiedu,name='declare_jiedu'),
    url(r'^task/declareana/(?P<task>\w+)$',views.declare_ana,name='declare_ana'),
    url(r'^task/declarelab/(?P<task>\w+)$',views.declare_lab,name='declare_lab'),
    url(r'^product$',views.product_index,name='product_index'),
    url(r'^product/add$',views.product_add,name='product_add'),
    # url(r'^product/modify/(?P<product>.*)$',views.product_modify,name='product_modify'),
]