from django.conf.urls import url
from . import views

app_name = 'course'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^(?P<course_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<notes_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),
    url(r'^notes/(?P<filter_by>[a-zA_Z]+)/$', views.notes, name='notes'),
    url(r'^create_course/$', views.create_course, name='create_course'),
    url(r'^(?P<course_id>[0-9]+)/create_notes/$', views.create_notes, name='create_notes'),
    url(r'^(?P<course_id>[0-9]+)/delete_notes/(?P<notes_id>[0-9]+)/$', views.delete_notes, name='delete_notes'),
    url(r'^(?P<course_id>[0-9]+)/favorite_course/$', views.favorite_course, name='favorite_course'),
    url(r'^(?P<course_id>[0-9]+)/delete_course/$', views.delete_course, name='delete_course'),
]
