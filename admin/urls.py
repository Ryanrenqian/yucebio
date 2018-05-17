from django.conf.urls import url
from . import views
app_name='admin'
urlpatterns=[
    url(r'^$',views.project_index,name='project_index'),
    url(r'^index/user$',views.user_index,name='user_index'),
    url(r'^index/group$',views.group_index,name='group_index'),
    url(r'^index/patient$',views.patient_index,name='patient_index'),
    url(r'^index/chip$',views.chips_index,name='chip_index'),
    url(r'^index/product$',views.product_index,name='product_index'),
    url(r'^add_user$',views.add_user,name='add_user'),
    url(r'^add_group$',views.add_group,name='add_group'),
    url(r'^add_project$',views.add_project,name='add_project'),
    url(r'^add_chip$',views.add_chip,name='add_chip'),
    url(r'^add_patient$',views.add_patient,name='add_patient'),
    url(r'^add_product$',views.add_product,name='add_product'),
    url(r'^delete_user/(?P<user>\w+)$',views.delete_user,name='delete_user'),
    url(r'^delete_project/(?P<project>\w+)$',views.delete_project,name='delete_project'),
    url(r'^delete_group/(?P<group>\w+)$',views.delete_group,name='delete_group'),
    url(r'^delete_patient/(?P<patient>\w+)$',views.delete_patient,name='delete_patient'),
    url(r'^delete_chip/(?P<chip>\w+)$',views.delete_chip,name='delete_chip'),
    url(r'^delete_product/(?P<product>\w+)$',views.delete_product,name='delete_product'),
    url(r'^modify_user/(?P<user>\w+)/$',views.modify_user,name='modify_user'),
    url(r'^modify_project/(?P<project>\w+)$',views.modify_project,name='modify_project'),
    url(r'^modify_patient/(?P<patient>\w+)$',views.modify_patient,name='modify_patient'),
    url(r'^modify_product/(?P<product>\w+)$',views.modify_product,name='modify_product'),
]