from django.conf.urls import url

from . import views
from django.contrib.auth import views as loginviews

urlpatterns = [
	url(r'^$', loginviews.login,name="login"),
	url(r'^logout/$', loginviews.logout, name="logout", kwargs={'next_page': '/'}),
	url(r'^home/add/$',views.ContactInfoCreate.as_view(),name="add"),
	url(r'^accounts/profile/$', views.redirecting,name="redirecting"),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^home/$',views.ContactInfoList.as_view(),name="view_home"),
	url(r'^home/(?P<pk>\d+)/edit/$',views.ContactInfoUpdate.as_view(),name="edit"),
	url(r'^home/(?P<pk>\d+)/$',views.ContactInfoDelete.as_view(),name="displaycontact"),
	#url(r'^home/(?P<pk>\d+)/delete/', views.delete, name="delete"),
	url(r'^import/$',views.simple_upload,name="simple_upload"),
	url(r'^export/$', views.export, name="export")
]