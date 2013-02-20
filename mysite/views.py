from django.shortcuts import render_to_response
import MySQLdb
from django.http import HttpResponse,HttpResponseRedirect
from django.core.validators import email_re
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import datetime
import os


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
        sql = "SELECT c.cid,c.cname,c.owner,c.start_date,c.no_of_followers,c.category,c.rating,c.desc\
                FROM courses as c,enrollments as e where e.uid=%s and e.cid=c.cid"
        umail=str(request.session['umail'])
        cursor.execute(sql,[umail])
        results = cursor.fetchall()

        sql = "SELECT distinct category from courses where category<>%s"
        cursor.execute(sql,["Random_lessons"])
        newresults = cursor.fetchall()
        db.close()
        return render_to_response('loggedin.html',{'msg': "logged  "+request.session['umail'] ,'results':results,'newresults':newresults})
    else:
        return render_to_response('loggedin.html',{'msg': False})

def yourcontents(request):
    if "umail" in request.session and request.session['umail']!="":
        db = MySQLdb.connect("localhost","root","","mysite" )
        cursor = db.cursor()
        sql = "SELECT cid,cname,owner,start_date,no_of_followers,category,rating,`desc` FROM courses where owner=%s"
        umail=str(request.session['umail'])
        cursor.execute(sql,[umail])
        results = cursor.fetchall()

        sql = "SELECT l.lno,l.lname,l.ldesc,l.postdate,l.filetype,l.likes,l.filename,c.cname \
                from courses as c,lessons as l where l.cid=c.cid and submitted_by=%s and submitted_by<>c.owner"
        cursor.execute(sql,[umail])
        newresults = cursor.fetchall()

        db.close()
        return render_to_response('yourcontent.html',{'msg': "logged  "+request.session['umail'],\
                                                      'results':results,'newresults':newresults})
    else:
        return render_to_response('login.html',{'msg': "please log in"})


def adduser(request):
    if  request.GET['email']!="" and request.GET['uname']!="" and request.GET['pass']!="":
        x= bool(email_re.match(request.GET['email']))
        if x:
            db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
            cursor = db.cursor()
            sql="select email from users where email=%s"
            ml=request.GET['email']
            cursor.execute(sql,[ml])
            x = [row[0] for row in cursor.fetchall()]
            if x:
                msg="already exists"
            else:
                unm=request.GET['uname']
                ps=request.GET['pass']
                sql="insert into users(name,email,password) values(%s,%s,%s)"
                cursor.execute(sql,[unm,ml,ps])
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
    sql="select email,password from users where email=%s"
    ml=str(request.GET['email'])
    cursor.execute(sql,[ml])
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
    sql = "SELECT cid,cname,owner,start_date,no_of_followers,category,rating,`desc` FROM courses where category=%s"
    try:
        cursor.execute(sql,[category])
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
    sql = "SELECT cid,cname,owner,start_date,no_of_followers,category,rating,`desc` FROM courses where cname<>%s"
    try:
        cursor.execute(sql,["xxx"])
        results = cursor.fetchall()
    except:
        print "Error: unable to fetch data"
    db.close()
    return render_to_response('all courses.html',{'results':results,'msg':umail})


def enroll(request, offset):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select uid from enrollments where cid=%s and uid=%s"
        offset=int(offset)
        uml=str(request.session["umail"])
        cursor.execute(sql,[offset,uml])
        result=cursor.fetchall()
        x = [row[0] for row in result]
        if x:
            msg="allready enrolled go back"
        else:
            sql="insert into enrollments(cid,uid) values(%s,%s)"
            cursor.execute(sql,[offset,uml])
            sql="update courses set no_of_followers=no_of_followers+1 where cid=%s"
            cursor.execute(sql,[offset])
            db.commit()
            db.close()
            return HttpResponseRedirect("/course/"+str(offset))
    return render_to_response('all courses.html',{'msg':msg})


def unenroll(request, offset):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select uid from enrollments where cid=%s and uid=%s"
        offset=int(offset)
        uml=str(request.session["umail"])
        cursor.execute(sql,[offset,uml])
        result=cursor.fetchall()
        x = [row[0] for row in result]
        if not x:
            msg="not enrolled go back"
        else:
            sql="delete from enrollments where cid=%s and uid=%s"

            cursor.execute(sql,[offset,uml])
            sql="update courses set no_of_followers=no_of_followers-1 where cid=%s "
            cursor.execute(sql,[offset])
            msg='unenrolled'
            db.commit()
        db.close()
    return render_to_response('all courses.html',{'msg':msg})


def byuser(request, offset):
    offset=str(offset)
    db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
    cursor = db.cursor()
    sql="select cid,cname,owner,start_date,no_of_followers,category,rating from courses where owner=%s"
    cursor.execute(sql,[offset])
    results=cursor.fetchall()
    sql="select lno,lname,ldesc,postdate,filename,submitted_by,c.cname from lessons as l,courses as c\
            where l.cid=c.cid and submitted_by=%s and submitted_by<>c.owner"
    cursor.execute(sql,[offset])
    newresults=cursor.fetchall()
    db.close()
    return render_to_response('byuser.html',{'results':results,'newresults':newresults})

def removecourse(request,offset):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        cid=int(offset)
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
            os.rmdir("c:/djangotest/mysite/static/lessons/"+cname)

            sql="delete from courses where cid=%s"
            cursor.execute(sql,[cid])
            db.commit()
            db.close()
            msg="done"
        return HttpResponse(msg)

def createcourse(request):
    if "umail" not in request.session:
        return HttpResponseRedirect("/login/")
    else:
        return render_to_response('createcourse.html',{'msg':""})

def addcourse(request):
    if "umail" not in request.session:
        return HttpResponseRedirect("/login/")
    else:
        if  request.GET['cname']!="" and request.GET['category']!="" :
            db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
            cursor = db.cursor()
            sql="select cname from courses where cname=%s"
            cnm=str(request.GET['cname'])
            cursor.execute(sql,[cnm])
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
                        except:
                            j+=1

                tags=str(request.GET['tags'])
                arr=tags.split('+')
                for item in arr:
                    sql="insert into coursetags values(%s,%s,'b')"
                    args=[cid,item]
                    try:
                        cursor.execute(sql,args)
                    except:
                        j+=1

                sql="insert into coursetags values(%s,%s,'a')"
                args=[cid,category]
                try:
                    cursor.execute(sql,args)
                except:
                    j+=1

                os.mkdir("c:/djangotest/mysite/static/lessons/"+cname)
                db.commit()
                db.close()
            return HttpResponseRedirect("/allcourses/")
        else:
            msg = 'You submitted an empty form go back.'
        return HttpResponse(msg)


