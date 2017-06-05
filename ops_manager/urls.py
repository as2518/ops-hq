from django.conf.urls import url
from ops_manager import views

urlpatterns = [
    url(r'^$', views.ops_list, name='ops_list'),
    url(r'^(?P<ops_id>\d+)/(?P<cond>\w+)/(?P<status>\d+)/$', views.change_status, name='status'),
    url(r'^add/$', views.ops_add, name='ops_add'),
    url(r'^add/confirm/$', views.ops_add_confirm, name='ops_add_confirm'),
    url(r'^detail/(?P<ops_id>\d+)/$', views.ops_detail, name='ops_detail'),
    url(r'^mod/(?P<ops_id>\d+)/$', views.ops_edit, name='ops_edit'),
    url(r'^del/(?P<ops_id>\d+)/$', views.ops_del, name='ops_del'),
]