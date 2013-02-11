from django.shortcuts import render_to_response
import MySQLdb
from django.http import HttpResponse,HttpResponseRedirect
from django.core.validators import email_re
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import datetime

@csrf_exempt
def trial(request):
    file=request.FILES['docfile']
    fd = open('%s/%s' % ("c:/djangotest", file), 'wb')
    fd.write(file)
    fd.close()

def tryhtml(request):
    return render_to_response('try.html',{'msg':""})

def home(request):
    return render_to_response('index.html',)

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
        db.close()
        return render_to_response('loggedin.html',{'msg': "logged  "+request.session['umail'] ,'results':results})
    else:
        return render_to_response('loggedin.html',{'msg': "not logged in"})

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
    del request.session["umail"]
    return render_to_response('index.html',)


def allcourses(request):
    db = MySQLdb.connect("localhost","root","","mysite" )
    cursor = db.cursor()
    sql = "SELECT * FROM courses"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        print "Error: unable to fetch data"
    db.close()
    return render_to_response('all courses.html',{'results':results})

def createcourse(request):
    if "umail" not in request.session:
        return HttpResponseRedirect("/login/")
    else:
        return render_to_response('createcourse.html',{'msg':""})

def addcourse(request):
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
            date=str(datetime.date.today())
            sql="insert into courses(cname,owner,start_date,category,`desc`) \
            values('"+request.GET['cname']+"','"+request.session["umail"]+"','"+date+"','"+request.GET['category']+"','"+request.GET['desc']+"');"
            if cursor.execute(sql):
                db.commit()
                db.close()
                return HttpResponseRedirect("/allcourses/")
            else:
                msg="sql fail"
    else:
        msg = 'You submitted an empty form go back.'
    return HttpResponse(msg)

def course(request, offset):
    if "umail" not in request.session:
        return HttpResponseRedirect("/login/")
    else:
        db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select cid from enrollments where cid='"+offset+"' and uid='"+request.session["umail"]+"'"
        cursor.execute(sql)
        x = [row[0] for row in cursor.fetchall()]
        db.close()
        if not x:
            msg="not enrolled to this course.. go back"
        else:
            return render_to_response('course.html',{'msg':offset})
        return render_to_response('all courses.html',{'msg':msg})

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
