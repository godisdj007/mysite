from django.shortcuts import render_to_response
import MySQLdb
from django.http import HttpResponse,HttpResponseRedirect
from django.core.validators import email_re
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import datetime

def forum(request,offset):
    offset=int(offset)
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select cid from enrollments where cid='%d' and uid='%s'" %(offset,request.session['umail'])
        cursor.execute(sql)
        x = [row[0] for row in cursor.fetchall()]
        if not x:
            msg="not enrolled to this course.. go back"
        else:
            sql="select fno,cid,owner,fname,no_of_posts,start_date from forums where cid='%d'"%(offset)
            cursor.execute(sql)
            results=cursor.fetchall()
            db.close()
            return render_to_response('forums.html',{'results':results})
        db.close()
        return render_to_response('all courses.html',{'msg':msg})

def addforum(request):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        cid=int(request.GET['cid'])
        db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select cid from enrollments where cid='%d' and uid='%s'" %(cid,request.session['umail'])
        cursor.execute(sql)
        x = [row[0] for row in cursor.fetchall()]
        if not x:
            msg="not enrolled to this course.. go back"
        else:
            dt=datetime.date.today()
            fname=str(request.GET['fname'])
            sql="insert into forums (cid,owner,fname,start_date) \
            values('%d','%s','%s','%s')" %(cid,request.session['umail'],fname,dt)
            cursor.execute(sql)
            db.commit()
            db.close()
            return HttpResponse("forum added")
        db.close()
        return HttpResponse(x)

def addpost(request):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        cid=int(request.GET['cid'])
        db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select cid from enrollments where cid='%d' and uid='%s'" %(cid,request.session['umail'])
        cursor.execute(sql)
        x = [row[0] for row in cursor.fetchall()]
        if not x:
            msg="not enrolled to this course.. go back"
        else:
            dt=datetime.date.today()
            fno=int(request.GET["fno"])
            content=str(request.GET['content'])
            sql="insert into forumsposts (cid,fno,posted_by,posted_on,content) \
            values(%s,%s,%s,%s,%s)"
            args=[cid,fno,request.session['umail'],dt,content]
            cursor.execute(sql,args)
            db.commit()
            db.close()
            return HttpResponseRedirect("/viewforum/%d/%d"%(cid,fno))
        db.close()
        return HttpResponse(x)


def viewforum(request,cid,fno):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        cid=int(cid)
        db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select cid from enrollments where cid='%d' and uid='%s'" %(cid,request.session['umail'])
        cursor.execute(sql)
        x = [row[0] for row in cursor.fetchall()]
        if not x:
            msg="not enrolled to this course.. go back"
        else:
            fno=int(fno)
            sql="select pno,cid,fno,posted_by,posted_on,likes,content from forumsposts \
                 where fno='%d' and cid='%d'"%(fno,cid)
            cursor.execute(sql)
            results=cursor.fetchall()

            sql2="select fno,cid,owner,fname,no_of_posts,start_date from forums \
                 where fno='%d' and cid='%d'"%(fno,cid)
            cursor.execute(sql2)
            results2=cursor.fetchall()

            sql3="select pno,fno,cid,user,likes from userlikes where cid=%s and fno=%s and user=%s"
            arr=[cid,fno,request.session['umail']]
            cursor.execute(sql3,arr)
            results3=cursor.fetchall()
            db.close
            user=request.session['umail']
            return render_to_response('viewforum.html',{'results':results,'cid':cid,'fno':fno,'results2':results2, \
                                      'user':user,'result3':results3})
        db.close()
        return HttpResponseRedirect("/forum/%d"%(cid))

def userlikes(request):
    pno=int( request.GET["pno"] )
    cid=int( request.GET["cid"] )
    fno=int( request.GET["fno"] )
    db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
    cursor = db.cursor()
    sql="select likes from userlikes where pno=%s and cid=%s and fno=%s and user=%s"
    arr=[pno,cid,fno,request.session['umail']]
    cursor.execute(sql,arr)
    x = [row[0] for row in cursor.fetchall()]
    if not x:
        sql="insert into userlikes (pno,cid,fno,user,likes) values(%s,%s,%s,%s,%s)"
        args=[pno,cid,fno,request.session['umail'],1]
        cursor.execute(sql,args)
        db.commit()
        sql1="update forumsposts set likes=likes+1 where pno='%d' and cid='%d' and fno='%d'"%(pno,cid,fno)
        cursor.execute(sql1)
        db.commit()
        db.close()
        return HttpResponseRedirect("/viewforum/%d/%d"%(cid,fno))
    else:
        sql="delete from userlikes where pno=%s and cid=%s and fno=%s and user=%s"
        args=[pno,cid,fno,request.session['umail']]
        cursor.execute(sql,args)
        db.commit()
        sql1="update forumsposts set likes=likes-1 where pno='%d' and cid='%d' and fno='%d'"%(pno,cid,fno)
        cursor.execute(sql1)
        db.commit()
        db.close()
        return HttpResponseRedirect("/viewforum/%d/%d"%(cid,fno))