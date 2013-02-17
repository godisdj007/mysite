from django.shortcuts import render_to_response
import MySQLdb
from django.http import HttpResponse,HttpResponseRedirect
from django.core.validators import email_re
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import datetime
import os

DEFINED_STATIC=os.path.join(os.path.dirname(__file__).replace('mysite',''), 'mysite/static/').replace('\\','/')

def submitrating(request):
    score=float( request.GET["score"] )
    cid=int( request.GET["cid"] )
    db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
    cursor = db.cursor()
    sql="select rating,raters from courses where cid='%d'"%(cid)
    cursor.execute(sql)
    result=cursor.fetchall()
    row=result[0]
    rating = row[0]
    raters = row[1]
    raters=raters+1
    rating=(rating*(raters-1)+score)/raters
    sql="update courses set rating='%f',raters='%d' where cid='%d'"%(rating,raters,cid)
    cursor.execute(sql)
    db.commit()
    db.close()
    return HttpResponse(rating)

def course(request, offset):
    if "umail" not in request.session:
        return HttpResponseRedirect("/login/")
    else:
        offset=int(offset)
        db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select owner from courses where cid='%d'"%(offset)
        cursor.execute(sql)
        result=cursor.fetchall()
        owner=result[0][0]
        db.close()
        if request.session['umail']!=owner:
            return HttpResponseRedirect("/viewcourse/%d"%(offset))
        else:
            return HttpResponseRedirect("/viewcourse/%d"%(offset)) #to be changed to owners view


def viewcourse(request,offset):
    offset=int(offset)
    if "umail" not in request.session:
        return HttpResponseRedirect("/login/")
    else:
        db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
        cursor = db.cursor()

        sql="select owner from courses where cid=%s"
        cursor.execute(sql,[offset])
        owner = [row[0] for row in cursor.fetchall()]
        if owner==request.session['umail']:
            admin=True
        else:
            admin=False

        sql="select cid from enrollments where cid='%d' and uid='%s'" %(offset,request.session['umail'])
        cursor.execute(sql)
        x = [row[0] for row in cursor.fetchall()]

        if not x:
            msg="not enrolled to this course.. go back"
        else:
            sql="select l.cid,l.lno,lname,ldesc,l.postdate,filetype,filename,submitted_by,cname \
            from lessons as l,courses as c \
            where l.cid='%d' and c.cid ='%d' and l.submitted_by=c.owner order by lno"%(offset,offset)
            cursor.execute(sql)
            results=cursor.fetchall()
            sql="select l.cid,l.lno,lname,ldesc,l.postdate,filetype,filename,submitted_by,cname,likes \
            from lessons as l,courses as c \
            where l.cid='%d' and c.cid ='%d' and l.submitted_by<>c.owner order by lno"%(offset,offset)
            cursor.execute(sql)
            newresults=cursor.fetchall()
            db.close()
            return render_to_response('viewcourse.html',{'cid':offset,'admin':admin,\
                                                        'results':results,'newresults':newresults})
        return render_to_response('all courses.html',{'msg':msg})


def  viewlesson(request):
    if "umail" not in request.session or request.session["umail"]=="":
        return HttpResponseRedirect("/login/")
    else:
        cname=str(request.GET["cname"])
        fname=str(request.GET["fname"])
        lno=int(request.GET["lno"])
        db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select lname,ldesc,filetype from lessons where lno=%s"
        cursor.execute(sql,[lno])
        results=cursor.fetchall()
        return render_to_response('viewlesson.html',{'results':results,'cname':cname,'fname':fname,'lno':lno})


def  addlike(request):
    if "umail" not in request.session or request.session["umail"]=="":
        return HttpResponse("login to like")
    else:
        lno=int(request.GET["lno"])
        db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
        cursor = db.cursor()
        sql="update lessons set likes=likes+1 where lno=%s"
        cursor.execute(sql,[lno])
        db.commit()
        db.close()
        return HttpResponse("added")


def addlesson(request,offset):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        return render_to_response('addlesson.html',{'cid':offset})

def removelesson(request,offset,newoffset):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        cid=int(offset)
        lno=int(newoffset)
        db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select cname,owner from courses where cid=%s"
        cursor.execute(sql,[cid])
        results=cursor.fetchall()
        cname=results[0][0]
        ownner=results[0][1]
        if ownner!=str(request.session['umail']):
            msg="u dont have permission"
        else:
            sql="select filename from lessons where cid=%s and lno=%s"
            cursor.execute(sql,[cid,lno])
            results=cursor.fetchall()
            fname=results[0][0]

            os.remove("c:/djangotest/mysite/static/lessons/"+cname+"/"+fname)

            sql="delete from lessons where cid=%s and lno=%s"
            cursor.execute(sql,[cid,lno])
            db.commit()
            db.close()
            msg="done"
        return HttpResponse(msg)


@csrf_exempt
def uploadlesson(request):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    elif "lname" not in request.POST or "ldesc" not in request.POST\
         or "tags" not in request.POST or "uploaded" not in request.FILES:
        msg="u entered empty form"
    else:
        cid=request.POST["cid"]
        db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select cname from courses where cid=%s"
        cursor.execute(sql,[cid])
        results=cursor.fetchall()
        cname=results[0][0]

        lname=request.POST["lname"]
        ldesc=request.POST["ldesc"]
        postdate=datetime.date.today()
        sub=request.session["umail"]
        f=request.FILES['uploaded']
        fname=str(f.name)
        ftype=f.content_type
        fsize=f.size
        if fsize<50000000:
            with open(DEFINED_STATIC+'/lessons/'+cname+'/'+fname, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)

            sql="insert into lessons (cid,lname,ldesc,postdate,filetype,filename,submitted_by)\
                   values(%s,%s,%s,%s,%s,%s,%s) "
            args=[cid,lname,ldesc,postdate,ftype,fname,sub]
            cursor.execute(sql,args)
            db.commit()

            sql="select lno from lessons where lname=%s and submitted_by=%s"
            cursor.execute(sql,[lname,sub])
            results=cursor.fetchall()
            lno=results[0][0]


            words=('and','or','to','from','part1','the','a','of','with','without',\
            'for','in','how','as','not','why','what','who','which','through','&','at','behind','on',\
            'since','you','we','is','are','learn','-','be',':',',','.','lesson','your')
            tags=lname.split(' ')
            tags=set(tags)
            tags=tags.difference(words)
            tags=list(tags)
            for item in tags:
                sql="insert into lessontags values(%s,%s,'a')"
                args=[lno,item]
                try:
                    cursor.execute(sql,args)
                    db.commit()
                except:
                    msg="error"

            tags=str(request.POST['tags'])
            tags=tags.split('+')
            tags=set(tags)
            tags=tags.difference(words)
            tags=list(tags)
            for item in tags:
                sql="insert into lessontags values(%s,%s,'b')"
                args=[lno,item]
                try:
                    cursor.execute(sql,args)
                    db.commit()
                except:
                    msg="error"

            db.commit()
            db.close()
            msg="done"
        else:
            msg="file too big"
    return HttpResponse(msg)




