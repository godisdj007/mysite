from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from views import *
from courseview import *
from forumsview import *
from searchview import *
from lsearchview import *

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
    ('^submitrating/$', submitrating),
    ('^bycategory/$',bycategory),
    ('^yourcontents/$',yourcontents),
    (r'^viewcourse/(\d+)/$', viewcourse),
    (r'^byuser/(\S+)/$', byuser),
    (r'^forum/(\d+)/$', forum),
    ('^addforum/$',addforum),
    ('^viewforum/$',viewforum),
    ('^addpost/$',addpost),
    (r'^viewlesson/$', viewlesson),
    ('^addlike/$',addlike),
    ('^asearchcourse/$',asearchcourse),
    ('^searchcourse/$',searchcourse),
    ('^bsearchcourse/$',bsearchcourse),
    ('^coursesrec/$',coursesrec),
    (r'^addlesson/(\d+)/$', addlesson),
    ('^uploadlesson/$',uploadlesson),
    (r'^removelesson/(\d+)/(\d+)/$', removelesson),
    ('^asearchlesson/$',bsearchlesson),
    ('^bsearchlesson/$',bsearchlesson),
    ('^lessonrec/$',lessonrec),
    (r'^removecourse/(\d+)/$', removecourse),


)
