from django.shortcuts import render_to_response
import MySQLdb
from django.http import HttpResponse,HttpResponseRedirect
from django.core.validators import email_re
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import datetime

import time


@csrf_exempt
def trial(request):
    #os.remove("c:/djangotest/mysite/static/lessons/da/new.py")
    return HttpResponse("done")

def tryhtml(request):
    return render_to_response('try.html',{'msg':""})

def home(request):
    if "umail" in request.session:
        msg=request.session["umail"]
    else:
        msg=False
    return render_to_response('index.html',{'msg': msg})

def signup(request):
    return render_to_response('signup.html',)

def login(request):
    return render_to_response('login.html',{'msg': "please log in"})

def loggedin(request):
    if "umail" in request.session and request.session['umail']!="":
        db = MySQLdb.connect("localhost","root","","mysite" )
        cursor = db.cursor()
        sql = "SELECT c.* FROM courses as c,enrollments as e where e.uid='%s' and e.cid=c.cid" %(request.session['umail'])
        cursor.execute(sql)
        results = cursor.fetchall()

        sql = "SELECT distinct category from courses"
        cursor.execute(sql)
        newresults = cursor.fetchall()
        db.close()
        return render_to_response('loggedin.html',{'msg': "logged  "+request.session['umail'] ,'results':results,'newresults':newresults})
    else:
        return render_to_response('loggedin.html',{'msg': False})

def yourcontents(request):
    if "umail" in request.session and request.session['umail']!="":
        db = MySQLdb.connect("localhost","root","","mysite" )
        cursor = db.cursor()
        sql = "SELECT * FROM courses where owner='%s'" %(request.session['umail'])
        cursor.execute(sql)
        results = cursor.fetchall()
        db.close()
        return render_to_response('yourcontent.html',{'msg': "logged  "+request.session['umail'],'results':results})
    else:
        return render_to_response('login.html',{'msg': "please log in"})


def adduser(request):
    if  request.GET['email']!="" and request.GET['uname']!="" and request.GET['pass']!="":
        x= bool(email_re.match(request.GET['email']))
        if x:
            db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
            cursor = db.cursor()
            sql="select email from users where email='"+request.GET['email']+"'"
            cursor.execute(sql)
            x = [row[0] for row in cursor.fetchall()]
            if x:
                msg="already exists"
            else:
                sql="insert into users(name,email,password) values('"+request.GET['uname']+"','"+request.GET['email']+"','"+request.GET['pass']+"')"
                cursor.execute(sql)
                db.commit()
                request.session["umail"] = request.GET['email']
                return render_to_response('loggedin.html',{'msg': "added user"})
            db.close()
        else:
            msg="invalid email"
    else:
        msg = 'You submitted an empty form.'
    return HttpResponse(msg)


def signuserin(request):
    db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
    cursor = db.cursor()
    sql="select email,password from users where email='"+request.GET['email']+"'"
    cursor.execute(sql)
    results = cursor.fetchall()
    if results:
        for row in results:
            m = row[0]
            p = row[1]
        if p==request.GET['pass']:
            msg="welcome"
            request.session["umail"] = request.GET['email']
            return HttpResponseRedirect("/loggedin/")
        else:
            return render_to_response('login.html',{'msg': "try again wrong pass"})
    else:
        msg="try again"
        return render_to_response('login.html',{'msg': msg})


def logout(request):
    if "umail" in request.session:
        del request.session["umail"]
    return HttpResponseRedirect('/home/')

def bycategory(request):
    category=request.GET["category"]
    db = MySQLdb.connect("localhost","root","","mysite" )
    cursor = db.cursor()
    sql = "SELECT * FROM courses where category='%s'"%(category)
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print "Error: unable to fetch data"
    db.close()
    return render_to_response('all courses.html',{'results':results})

def allcourses(request):
    if "umail" in request.session and request.session['umail']!="":
        umail=request.session["umail"]
    else:
        umail=False
    db = MySQLdb.connect("localhost","root","","mysite" )
    cursor = db.cursor()
    sql = "SELECT * FROM courses"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print "Error: unable to fetch data"
    db.close()
    return render_to_response('all courses.html',{'results':results,'msg':umail})

def createcourse(request):
    if "umail" not in request.session:
        return HttpResponseRedirect("/login/")
    else:
        return render_to_response('createcourse.html',{'msg':""})


def deletecourse(request,offset):
    if "umail" in request.session:
        db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
        cursor = db.cursor()
        cid=int(offset)
        sql="select owner from courses where cid='%d'"%(cid)
        cursor.execute(sql)
        result=cursor.fetchall()
        if request.session["umail"]!=result[0][0]:
            return HttpResponse("u are not the owner")
        else:
            sql="delete from courses where cid='%d'"%(cid)
            cursor.execute(sql)
            db.commit()
            return HttpResponse("deleted")

    else:
        return render_to_response('login.html',{'msg': "please log in"})


def enroll(request, offset):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select uid from enrollments where cid='"+offset+"' and uid='"+request.session["umail"]+"'"
        cursor.execute(sql)
        result=cursor.fetchall()
        x = [row[0] for row in result]
        if x:
            msg="allready enrolled go back"
        else:
            sql="insert into enrollments(cid,uid) \
            values('"+offset+"','"+request.session["umail"]+"');"
            if cursor.execute(sql):
                db.commit()
                sql="update courses set no_of_followers=no_of_followers+1 where cid=%d "%(int(offset))
                cursor.execute(sql)
                db.commit()
                db.close()
                return HttpResponseRedirect("/course/"+offset)
    return render_to_response('all courses.html',{'msg':msg})


def unenroll(request, offset):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select uid from enrollments where cid='"+offset+"' and uid='"+request.session["umail"]+"'"
        cursor.execute(sql)
        result=cursor.fetchall()
        x = [row[0] for row in result]
        if not x:
            msg="not enrolled go back"
        else:
            sql="delete from enrollments where cid='%d' and uid='%s'"%(int(offset),request.session['umail'])
            if cursor.execute(sql):
                db.commit()
                sql="update courses set no_of_followers=no_of_followers-1 where cid=%d "%(int(offset))
                cursor.execute(sql)
                msg='unenrolled'
                db.commit()
        db.close()
    return render_to_response('all courses.html',{'msg':msg})


def byuser(request, offset):
    offset=str(offset)
    db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
    cursor = db.cursor()
    sql="select * from courses where owner='%s'"%offset
    cursor.execute(sql)
    results=cursor.fetchall()
    sql="select l.* from courses as c,lessons as l where l.cid=c.cid and submitted_by='%s' and submitted_by<>c.owner"%offset
    cursor.execute(sql)
    newresults=cursor.fetchall()
    db.close()
    return render_to_response('byuser.html',{'results':results,'newresults':newresults})


def mailtouser(usermail):
    offset=str(usermail)
    send_mail( 'Subject here', 'Here is the message.', '',[offset], fail_silently=False )


def addcourse(request):
    if "umail" not in request.session:
        return HttpResponseRedirect("/login/")
    else:
        if  request.GET['cname']!="" and request.GET['category']!="" :
            db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
            cursor = db.cursor()
            sql="select cname from courses where cname='"+request.GET['cname']+"'"
            cursor.execute(sql)
            x = [row[0] for row in cursor.fetchall()]
            if x:
                msg="course name already exists"
                db.close()
            else:
                j=0
                date=str(datetime.date.today())
                cname=str(request.GET['cname'])
                umail=str(request.session["umail"])
                category=str(request.GET['category'])
                desc=str(request.GET['desc'])
                args=[cname,umail,date,category,desc]
                sql="insert into courses(cname,owner,start_date,category,`desc`) \
                values(%s,%s,%s,%s,%s)"
                cursor.execute(sql,args)
                db.commit()

                sql="select cid from courses where cname=%s"
                cursor.execute(sql,[cname])
                results=cursor.fetchall()
                cid=results[0][0]

                words=('and','or','to','from','part1','the','a','of','with','without',\
                       'for','in','how','as','not','why','what','who','which','through','&','at','behind','on',\
                       'since','you','we','is','are','learn','-','be',':',',','.','lesson','your')
                tags=cname.split(' ')
                tags=set(tags)
                tags=tags.difference(words)
                tags=list(tags)
                for item in tags:
                        sql="insert into coursetags values(%s,%s,'a')"
                        args=[cid,item]
                        try:
                            cursor.execute(sql,args)
                            db.commit()
                        except:
                            j+=1

                tags=str(request.GET['tags'])
                arr=tags.split('+')
                for item in arr:
                    sql="insert into coursetags values(%s,%s,'b')"
                    args=[cid,item]
                    try:
                        cursor.execute(sql,args)
                        db.commit()
                    except:
                        j+=1

                sql="insert into coursetags values(%s,%s,'a')"
                args=[cid,category]
                try:
                    cursor.execute(sql,args)
                    db.commit()
                except:
                    j+=1


                db.close()
            return HttpResponseRedirect("/allcourses/")
        else:
            msg = 'You submitted an empty form go back.'
        return HttpResponse(msg)


