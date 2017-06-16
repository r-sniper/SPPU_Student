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
    # /refresh - Update Database with new codes
    url(r'^refresh/$', views.refresh, name="refresh"),
    #url /view_code
    url(r'^subject/$',views.test,name='view_code')

]
