from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from views import *
from courseview import *
from searchview import *
from lsearchview import *
from forumsview import *
from assignmentview import *
from feedbackview import *
from subscribeview import *


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
    (r'^byuser/(\S+)/(\d+)/$', byuser),
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




    (r'^forum/(\d+)/$', forum),
    ('^addforum/$',addforum),
    ('^viewforum/(\d+)/(\d+)/$',viewforum),
    ('^addpost/$',addpost),
    ('^userlikes/$',userlikes),
    (r'^assignment/(\d+)/$',assignment),
    (r'^viewassignment/$',viewassignment),
    ('^finishassignment/$',finishassignment),
    ('^createassignment/$',createassignment),
    ('^addassignment/$',addassignment),
    ('^addassignment_question/$',addassignment_question),
    ('^feed/(\d+)/$',feed),
    ('^feedbacks/$',feedbacks),
    ('^viewfeedback/(\d+)/$', viewfeedback),
    ('^subscribe/(\S+)/(\d+)/(\d+)/$',subscribe),
    ('^recentactivity/$',recentactivity),


)
