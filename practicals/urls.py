
from django.conf.urls import url
from django.contrib import admin
from . import views

app_name = 'selection'

urlpatterns = [
    #
    url(r'^$', views.home, name="home_page"),
    #/subject/
    url(r'^subject/$',views.default_subject,name="default_subject"),
    #/subject/(stream_id)
    url(r'^subject/(?P<stream_id>[0-9]+)/$', views.change_subject, name="change_subject"),
    # /subject/(stream_id)/(Subject)
    url(r'^subject/(?P<stream_id>[0-9]+)/(?P<subject_id>[0-9]+)/$', views.view_code, name="view_code"),

]