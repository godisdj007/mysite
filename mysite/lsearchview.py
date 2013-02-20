from django.shortcuts import render_to_response
import MySQLdb
from django.http import HttpResponse,HttpResponseRedirect
from django.core.validators import email_re
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import datetime

def searchlesson(qry):
        db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select *\
            from lessons where lname = %s"
        cursor.execute(sql,[qry])
        results=cursor.fetchall()
        return results


def asearchlesson(request):
    qry=str(request.GET["lname"])

    words=('and','or','to','from','part1','the','a','of','with','without',\
           'for','in','how','as','not','why','what','who','which','through','&','at','behind','on',\
           'since','you','we','is','are','learn','-','be',':',',','.','lesson','your','ppp')
    arr=qry.split(' ')
    arr=set(arr)
    qqq=[]
    arr=arr.difference(words)
    arr=list(arr)

    db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
    cursor = db.cursor()
    sql="select distinct lno from lessontags"
    cursor.execute(sql)
    results=cursor.fetchall()
    for row in results:
        count=0;
        lno=row[0]
        sql="select tag from lessontags where lno=%s and class='a'"
        cursor.execute(sql,lno)
        newresults=cursor.fetchall()
        for newrow in newresults:
                for item in arr:
                    if item==newrow[0]:
                        count+=3
                    elif item.find(newrow[0])!=-1 or newrow[0].find(item)!=-1:
                        if newrow[0].__len__()>3 and item.__len__()>3:
                            count+=1
        sql="select * from lessons where lno=%s"
        cursor.execute(sql,lno)
        roo=cursor.fetchall()
        www=[]
        www.append(count)
        for term in roo:
            www.append(term)
        qqq.append(www)

    qqq.sort()
    qqq.reverse()
    db.close()
    return HttpResponse(qqq)


def bsearchlesson(request):
    qry=str(request.GET["lname"])

    words=('and','or','to','from','part1','the','a','of','with','without',\
           'for','in','how','as','not','why','what','who','which','through','&','at','behind','on',\
           'since','you','we','is','are','learn','-','be',':',',','.','lesson','your','ppp')
    arr=qry.split(' ')
    arr=set(arr)
    qqq=[]
    arr=arr.difference(words)
    arr=list(arr)

    db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
    cursor = db.cursor()
    sql="select distinct lno from lessontags"
    cursor.execute(sql)
    results=cursor.fetchall()
    for row in results:
        count=0;
        lno=row[0]
        sql="select tag from lessontags where lno=%s and class='b'"
        cursor.execute(sql,lno)
        newresults=cursor.fetchall()
        for newrow in newresults:
            for item in arr:
                if item==newrow[0]:
                    count+=3
                elif item.find(newrow[0])!=-1 or newrow[0].find(item)!=-1:
                    if newrow[0].__len__()>3 and item.__len__()>3:
                        count+=1
        sql="select * from lessons where lno=%s"
        cursor.execute(sql,lno)
        roo=cursor.fetchall()
        www=[]
        www.append(count)
        for term in roo:
            www.append(term)
        qqq.append(www)

    qqq.sort()
    qqq.reverse()
    db.close()
    return HttpResponse(qqq)



def lessonrec(request):
    qry=str(request.GET["lname"])

    qqq=[]
    db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
    cursor = db.cursor()
    sql="select tag from lessontags as x,lessons as l where x.lno=l.lno and lname=%s"
    cursor.execute(sql,[qry])
    results=cursor.fetchall()
    arr=[]
    for row in results:
        arr.append(row[0])


    sql="select distinct x.lno from lessontags as x,lessons as l where x.lno=l.lno and lname<>%s"
    cursor.execute(sql,[qry])
    results=cursor.fetchall()
    for row in results:
        count=0;
        lno=row[0]
        sql="select tag from lessontags as x where x.lno=%s"
        cursor.execute(sql,[lno])
        newresults=cursor.fetchall()
        for newrow in newresults:
            for item in arr:
                if item==newrow[0]:
                    count+=3
                elif item.find(newrow[0])!=-1 or newrow[0].find(item)!=-1:
                    if newrow[0].__len__()>3 and item.__len__()>3:
                        count+=1
        sql="select * from lessons where lno=%s"
        cursor.execute(sql,lno)
        roo=cursor.fetchall()
        www=[]
        www.append(count)
        for term in roo:
            www.append(term)
        qqq.append(www)

    qqq.sort()
    qqq.reverse()
    db.close()
    return HttpResponse(qqq)
