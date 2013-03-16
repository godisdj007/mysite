from django.shortcuts import render_to_response
import MySQLdb
from django.http import HttpResponse,HttpResponseRedirect
from django.core.validators import email_re
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import datetime
import os

DEFINED_STATIC=os.path.join(os.path.dirname(__file__).replace('devesh mysite',''), 'devesh mysite/static/').replace('\\','/')

def submitrating(request):
    umail=request.session['umail']
    score=float( request.GET["score"] )
    if score>0 and score<5.1:
        cid=int( request.GET["cid"] )
        db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select * from courserate where cid=%s and ratedby=%s"
        cursor.execute(sql,[cid,umail])
        result=cursor.fetchall()
        if not result:
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

            sql="insert into courserate values(%s,%s)"
            cursor.execute(sql,[cid,umail])
            db.commit()
        db.close()
    return HttpResponse(rating)

def course(request, offset):
    if "umail" not in request.session:
        return HttpResponseRedirect("/login/")
    else:
        uml=str(request.session['umail'])
        cid=int(offset)
        db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select owner,`desc`,cname from courses where cid=%s"
        cursor.execute(sql,[cid])
        result=cursor.fetchall()
        owner=result[0][0]
        desc=result[0][1]
        cname=result[0][2]

        sql="select * from enrollments where cid=%s and uid=%s"
        cursor.execute(sql,[cid,uml])
        enrld=cursor.fetchall()

        db.close()
        if uml!=owner:
            admin=True
        else:
            admin=False
        return render_to_response('coursedetails.html',{'desc':desc,'cid':cid,'admin':admin,'enrolled':enrld,'cname':cname})
        #return HttpResponseRedirect("/viewcourse/%d"%(offset))


def viewcourse(request,offset):
    cid=int(offset)
    if "umail" not in request.session:
        return HttpResponseRedirect("/login/")
    else:
        uml=str(request.session["umail"])
        db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
        cursor = db.cursor()

        sql="select owner from courses where cid=%s"
        cursor.execute(sql,[cid])
        res=cursor.fetchall()
        owner =res[0][0]
        if owner==str(request.session['umail']):
            admin=True
        else:
            admin=False

        sql="select cid from enrollments where cid=%s and uid=%s"
        cursor.execute(sql,[cid,uml])
        x = [row[0] for row in cursor.fetchall()]

        if not x:
            msg="not enrolled to this course.. go back"
        else:
            sql="select l.cid,l.lno,lname,ldesc,l.postdate,filetype,filename,submitted_by,cname \
            from lessons as l,courses as c \
            where l.cid=%s and c.cid =%s and l.submitted_by=c.owner order by lno"
            cursor.execute(sql,[cid,cid])
            results=cursor.fetchall()
            sql="select l.cid,l.lno,lname,ldesc,l.postdate,filetype,filename,submitted_by,cname,likes \
            from lessons as l,courses as c \
            where l.cid=%s and c.cid =%s and l.submitted_by<>c.owner order by lno"
            cursor.execute(sql,[cid,cid])
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
        db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select lname,ldesc,filetype,likes from lessons where lno=%s"
        cursor.execute(sql,[lno])
        results=cursor.fetchall()
        ftype=str(results[0][2])
        if ftype.find('video')!=-1:
            vid=True
        else:
            vid=False
        db.close()
        lname=results[0][0]
        #return HttpResponse(vid)
        return render_to_response('viewlesson.html',{'qry':lname,'results':results,'cname':cname,\
                                                     'fname':fname,'lno':lno,'video':vid})


def  addlike(request):
    if "umail" not in request.session or request.session["umail"]=="":
        return HttpResponse("login to like")
    else:
        umail=request.session['umail']
        lno=int(request.GET["lno"])
        db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select * from lessonlike where lno=%s and likedby=%s"
        cursor.execute(sql,[lno,umail])
        results=cursor.fetchall()
        msg="not added"
        if not results:
            sql="update lessons set likes=likes+1 where lno=%s"
            cursor.execute(sql,[lno])
            sql="insert into lessonlike values(%s,%s)"
            cursor.execute(sql,[lno,umail])
            db.commit()
            msg="added"
        db.close()
        return HttpResponse(msg)



def removelesson(request,offset,newoffset):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        cid=int(offset)
        lno=int(newoffset)
        db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select cname,owner from courses where cid=%s"
        cursor.execute(sql,[cid])
        results=cursor.fetchall()
        cname=results[0][0]
        ownner=results[0][1]
        sql="select submitted_by from lessons where lno=%s"
        cursor.execute(sql,[lno])
        results=cursor.fetchall()
        newowner=results[0][0]
        if ownner!=str(request.session['umail']) and newowner!=str(request.session['umail']):
            msg="u dont have permission"
        else:
            sql="select filename from lessons where cid=%s and lno=%s"
            cursor.execute(sql,[cid,lno])
            results=cursor.fetchall()
            fname=results[0][0]

            os.remove("c:/djangotest/devesh mysite/static/lessons/"+cname+"/"+fname)

            sql="delete from lessons where cid=%s and lno=%s"
            cursor.execute(sql,[cid,lno])
            db.commit()
            db.close()
            msg="done"
        return HttpResponse(msg)


def addlesson(request,offset):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        return render_to_response('addlesson.html',{'cid':offset})

@csrf_exempt
def uploadlesson(request):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    elif "lname" not in request.POST or "ldesc" not in request.POST\
         or "tags" not in request.POST or "uploaded" not in request.FILES:
        msg="u entered empty form"
    else:
        cid=request.POST["cid"]
        db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
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
        if checklesson(lname):
            msg="lname already exists"
        else:
            if fsize<50000000:
                with open(DEFINED_STATIC+'/lessons/'+cname+'/'+fname, 'wb+') as destination:
                    for chunk in f.chunks():
                        destination.write(chunk)

                sql="insert into lessons (cid,lname,ldesc,postdate,filetype,filename,submitted_by)\
                       values(%s,%s,%s,%s,%s,%s,%s) "
                args=[cid,lname,ldesc,postdate,ftype,fname,sub]
                cursor.execute(sql,args)
                #db.commit()

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
                        #db.commit()
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
                        #db.commit()
                    except:
                        msg="error"

                db.commit()
                db.close()
                msg="done"
                return HttpResponseRedirect("/viewcourse/"+str(cid))
                #notify(cid,cname)
            else:
                msg="file too big"
    return HttpResponse(msg)


def checklesson(lname):
    db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
    cursor = db.cursor()
    sql="select lname from lessons where lname=%s"
    cursor.execute(sql,[lname])
    results=cursor.fetchall()
    db.close()
    if results:
        return True
    else:
        return False
    return

def notify(cid,cname):
    db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
    cursor = db.cursor()
    sql="select uid from enrollments where cid=%s"
    cursor.execute(sql,[cid])
    results=cursor.fetchall()
    db.close()
    for row in results:
        uid=row[0]
        send_mail('new lesson notification', 'a new lesson has been added to '+cname, '',
            [uid], fail_silently=False)
    return


