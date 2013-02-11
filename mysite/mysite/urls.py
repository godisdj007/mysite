from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from views import *

urlpatterns = patterns('',
    ('^home/$', home),
    ('^signup/$', signup),
    ('^login/$', login),
    ('^loggedin/$', loggedin),
    ('^adduser/$', adduser),
    ('^trial/$', trial),
    ('^signuserin/$', signuserin),
    ('^logout/$', logout),
    ('^tryhtml/$', tryhtml),
    ('^allcourses/$', allcourses),
    ('^createcourse/$', createcourse),
    (r'^course/(\d+)/$', course),
    (r'^enroll/(\d+)/$', enroll),
    ('^addcourse/$', addcourse),
    (r'^unenroll/(\d+)/$', unenroll),




)
