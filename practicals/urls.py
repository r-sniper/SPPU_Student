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
    # url /view_code
    url(r'^subject/$', views.subject, name='view_code'),
    #
    url(r'^add_quotes/$',views.add_quote,name='add_quote'),
    # /test - We use this to test any template
    url(r'^test/$', views.test, name='test')

]
