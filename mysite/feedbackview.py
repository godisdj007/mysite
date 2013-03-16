__author__ = 'ajaysingh'


from django.shortcuts import render_to_response
import MySQLdb
from django.http import HttpResponse,HttpResponseRedirect
from django.core.validators import email_re
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import datetime


def feed(request,offset):
    cid=int(offset)
    if "umail" in request.session:
        msg="PLEASE FEED IT..."
        user=request.session['umail']
    else:
        msg="YOU SHOULD LOGIN"
        return HttpResponseRedirect("/login/")

    return render_to_response('feedback.html',{'msg': msg,'cid':cid,'user':user})

def feedbacks(request):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        cid=int(request.GET["cid"])
        user=request.session["umail"]
        if request.GET['feedback']!="":
            db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
            cursor = db.cursor()
            date=datetime.date.today()
            feedback=request.GET['feedback']
            sql="insert into feedbacks(cid,user,feedback,post_date) values(%s,%s,%s,%s)"
            args=[cid,user,feedback,date]
            if cursor.execute(sql,args):
                db.commit()
                db.close()
                return HttpResponseRedirect("/viewcourse/%d"%(cid))
            else:
                msg="sql fail"
                return HttpResponse(msg)
        else:
            msg = 'PLEASE FILL IT PROPERLY'
            return render_to_response('feedback.html',{'msg': msg,'cid':cid,'user':user})


def viewfeedback(request,offset):
    cid=int(offset)
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:

        db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select cid from enrollments where cid='%d' and uid='%s'" %(cid,request.session['umail'])
        cursor.execute(sql)
        x = [row[0] for row in cursor.fetchall()]
        if not x:
            msg="not enrolled to this course.. go back"
        else:
            sql="select fno,cid,user,feedback,post_date from feedbacks where cid=%s"
            args=[cid]
            cursor.execute(sql,args)
            results=cursor.fetchall()
            db.close
            user=request.session['umail']
            return render_to_response('viewfeedback.html',{'results':results,'cid':cid,'user':user})
        db.close()
        return HttpResponseRedirect("/viewcourse/%d"%(cid))


