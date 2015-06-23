from django.conf.urls import patterns, url
from pytt import views

urlpatterns = patterns('',
                       url(r'^3/times$', views.list_tr),
                       url(r'^3/times/$', views.list_tr),
                       url(r'^3/departments/$', views.list_departments),
                       url(r'^3/departments$', views.list_departments),
                       url(r'^3/departments/(?P<deptag>\w+)/msg/', views.get_department_msg),
                       url(r'^3/departments/(?P<deptag>\w+)/msg', views.get_department_msg),
                       url(r'^3/departments/(?P<deptag>\w+)/groups/$', views.get_department_groups),
                       url(r'^3/departments/(?P<deptag>\w+)/groups$', views.get_department_groups),
                       url(r'^3/departments/(?P<deptag>\w+)/groups/(?P<groupname>\w+)', views.get_timetable),
                       url(r'^3/departments/(?P<deptag>\w+)/groups/(?P<groupname>\w+)/', views.get_timetable),
                       url(r'^3/teachers/(?P<teacher_id>\w+)/', views.get_teacher_timetable),
                       url(r'^3/teachers/(?P<teacher_id>\w+)', views.get_teacher_timetable),
                       url(r'^3/teachers', views.search_teacher),
                       url(r'^3/parity$', views.get_parity)
                       )
