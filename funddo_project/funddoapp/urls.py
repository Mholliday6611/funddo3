from django.conf.urls import patterns, url
from funddoapp import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^userbylocationjob/', views.userbylocationjob, name = 'userlocationjob'),
	url(r'^userbylocationfund/', views.userbylocationfund, name = 'userlocationfund'),
	url(r'^make_request/', views.make_request, name ='make_request'),
	url(r'^register/', views.register, name= 'register'),
	url(r'^register_funder/', views.register_funder, name='register_funder'),
	url(r'^register_jobseeker/', views.register_jobseeker, name='register_jobseeker'),
	url(r'^login/', views.user_login, name='login'),
	url(r'^logout/', views.user_logout, name='logout'),
	url(r'^about/', views.about, name='about'),
	url(r'^requests/(?P<req_id>\d+)/$', views.requests, name='request'),
	url(r'^user/(?P<user_username>[\w\-]+)/$',views.user_profile, name='profile'),
	url(r'^user/(?P<user_username>[\w\-]+)/edit/$',views.edit_funderprofile, name='edit_funderprofile'),
	url(r'^user/(?P<user_username>[\w\-]+)/editjob/$',views.edit_jobseekerprofile, name='edit_jobseekerprofile'),
	url(r'^settings/$', views.SettingsView.as_view(), name='settings'),
    url(r'^recover-password/$', views.PasswordRecoveryView.as_view(), name='recover-password'),
    url(r'^gallery/', views.gallery, name='gallery'),
	)
