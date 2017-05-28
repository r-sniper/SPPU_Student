from django.conf.urls import url

from . import views

app_name = 'selection'

'''
    We will following convention for writing a url
    # actual url(eg /subject) - Description
    url(...)
'''

urlpatterns = [
    # - Homepage to choose stream and year
    url(r'^$', views.home, name="home_page"),
    # /subject/ - Select Subject and view problemstatements
    url(r'^subject/$', views.default_subject, name="default_subject"),
    # /subject/(stream_id) - When subject is changed display its assignments
    url(r'^subject/(?P<stream_id>[0-9]+)/$', views.change_subject, name="change_subject"),
    # /subject/(stream_id)/(Subject) - View Code of particular assignment
    url(r'^subject/(?P<stream_id>[0-9]+)/(?P<subject_id>[0-9]+)/$', views.view_code, name="view_code"),
    # /refresh - Update Database with new codes
    url(r'^refresh/$', views.refresh, name="refresh")

]
