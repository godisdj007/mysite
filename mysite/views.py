from django.shortcuts import render_to_response
import datetime
import MySQLdb
from django.http import HttpResponse

from django.core.validators import email_re

def trial(request):
    db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
    cursor = db.cursor()
    sql="insert into users(name,email,password) values('use2','godisd','asdf')"
    sql2="select email from users where email='godisdj00@gmail.com'"
    if cursor.execute(sql2):
        msg = [row[0] for row in cursor.fetchall()]
        #msg="true"
        #db.commit()
    else:
        msg="false"
    db.close()
    return HttpResponse(msg)

def home(request):
    return render_to_response('index.html',)

def signup(request):
    return render_to_response('signup.html',)

def login(request):
    return render_to_response('login.html',)

def loggedin(request):
    return render_to_response('loggedin.html',{'msg': "logged"})

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
            return render_to_response('loggedin.html',{'msg': msg})
        else:
            return render_to_response('login.html',{'msg': "try again wrong pass"})
    else:
        msg="try again"
        return render_to_response('login.html',{'msg': msg})


def logout(request):
    return render_to_response('index.html',)
