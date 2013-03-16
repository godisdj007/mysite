__author__ = 'ajaysingh'


from django.shortcuts import render_to_response
import MySQLdb
from django.http import HttpResponse,HttpResponseRedirect
from django.core.validators import email_re
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import datetime


def subscribe(request,offset,cid,subs):
    subs=int(subs)
    cid=int(cid)
    owner=str(offset)
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:

        db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select cid from enrollments where cid='%d' and uid='%s'" %(cid,request.session['umail'])
        cursor.execute(sql)
        x = [row[0] for row in cursor.fetchall()]
        if not x:
            msg2="not enrolled to this course.. go back"
        else:
            user=request.session['umail']
            #sql="select user,sub_user,sub_cid from subscribe where user=%s and sub_user=%s and sub_cid=%s"
            #args=[user,owner,cid]
            #cursor.execute(sql,args)
            #y=[row[0] for row in cursor.fetchall()]
            #if not y:
            if subs:
                sql="insert into subscribe(user,sub_user) values(%s,%s)"
                args=[user,owner]
                if cursor.execute(sql,args):
                    db.commit()
                    db.close()
                    return HttpResponseRedirect("/viewcourse/%d"%(cid))
                else:
                    msg="sql fail"
                return HttpResponse(msg)
            else:
                sql="delete from  subscribe where user=%s and sub_user=%s"
                args=[user,owner]
                if cursor.execute(sql,args):
                    db.commit()
                    db.close()
                    return HttpResponseRedirect("/viewcourse/%d"%(cid))
                else:
                    msg="sql fail"
                return HttpResponse(msg)
        db.close()
        return render_to_response('all courses.html',{'msg2':msg2})


def recentactivity(request):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select cid from enrollments where uid='%s'" %(request.session['umail'])
        cursor.execute(sql)
        x = [row[0] for row in cursor.fetchall()]
        if not x:
            msg2="not enrolled to this course.. go back"
        else:
              user=request.session['umail']
              sql="select distinct sub_user from subscribe where user=%s"
              arr=[user]
              cursor.execute(sql,arr)
              result=cursor.fetchall()
               #owner = result[0][0]
               #return HttpResponse(owner)
              n1=list()
              n2=list()
              for row in result:
                  # n1.append(row[0])
                  #return HttpResponse(n1)
                 sql="select cid,cname,owner,start_date,no_of_followers,category,rating,raters from courses  \
                     where owner=%s order by start_date desc limit 0,2"
                 args=[row[0]]
                 cursor.execute(sql,args)
                 result1=cursor.fetchall()
                 for row1 in result1:
                    n1.append(row1)
                 sql="select cid,lno,lname,ldesc,postdate,filetype,filename,submitted_by,likes from lessons\
                     where submitted_by=%s order by postdate desc limit 0,2"
                 cursor.execute(sql,[row[0]])
                 result2=cursor.fetchall()
                 for row1 in result2:
                      n2.append(row1)
              return render_to_response('recentactivity.html',{'n1':n1,'n2':n2})
        db.close()
        return render_to_response('all courses.html',{'msg2':msg2})
