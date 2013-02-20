from django.shortcuts import render_to_response
import MySQLdb
from django.http import HttpResponse,HttpResponseRedirect
from django.core.validators import email_re
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import datetime
from lsearchview import *

def searchcourse(request):
    if "cname" in request.GET and request.GET["cname"]!="":
        qry=str(request.GET["cname"])
        db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
        cursor = db.cursor()
        sql="select cid,cname,owner,start_date,no_of_followers,category,rating \
            from courses where cname = %s"
        cursor.execute(sql,[qry])
        results=cursor.fetchall()
        newresults=searchlesson(qry)
        return render_to_response('viewsearch.html',{'newresults':newresults,'results':results,'qry':qry})


def asearchcourse(request):
    qry=str(request.GET["cname"])

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
    sql="select distinct cid from coursetags"
    cursor.execute(sql)
    results=cursor.fetchall()
    for row in results:
        count=0;
        cid=row[0]
        sql="select tag from coursetags where cid=%s and class='a'"
        cursor.execute(sql,cid)
        newresults=cursor.fetchall()
        for newrow in newresults:
                for item in arr:
                    if item==newrow[0]:
                        count+=3
                    elif item.find(newrow[0])!=-1 or newrow[0].find(item)!=-1:
                        if newrow[0].__len__()>3 and item.__len__()>3:
                            count+=1
        sql="select * from courses where cid=%s"
        cursor.execute(sql,cid)
        roo=cursor.fetchall()
        if count>1:
            www=[]
            www.append(count)
            for term in roo:
                www.append(term)
            qqq.append(www)

    qqq.sort()
    qqq.reverse()
    db.close()
    return render_to_response('coursesrec.html',{'newresults':qqq})
    #return HttpResponse(qqq)


def bsearchcourse(request):
    qry=str(request.GET["cname"])

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
    sql="select distinct cid from coursetags"
    cursor.execute(sql)
    results=cursor.fetchall()
    for row in results:
        count=0;
        cid=row[0]
        sql="select tag from coursetags where cid=%s and class='b'"
        cursor.execute(sql,cid)
        newresults=cursor.fetchall()
        for newrow in newresults:
            for item in arr:
                if item==newrow[0]:
                    count+=3
                elif item.find(newrow[0])!=-1 or newrow[0].find(item)!=-1:
                    if newrow[0].__len__()>3 and item.__len__()>3:
                        count+=1
        sql="select * from courses where cid=%s"
        cursor.execute(sql,cid)
        roo=cursor.fetchall()
        if count>1:
            www=[]
            www.append(count)
            for term in roo:
                www.append(term)
            qqq.append(www)

    qqq.sort()
    qqq.reverse()
    db.close()
    return render_to_response('coursesrec.html',{'newresults':qqq})
    #return HttpResponse(qqq)



def coursesrec(request):
    qry=str(request.GET["cname"])

    qqq=[]
    db = MySQLdb.connect(user='root', db='mysite', passwd='', host='')
    cursor = db.cursor()
    sql="select tag from coursetags as x,courses as c where x.cid=c.cid and cname=%s"
    cursor.execute(sql,[qry])
    results=cursor.fetchall()
    arr=[]
    for row in results:
        arr.append(row[0])


    sql="select distinct x.cid from coursetags as x,courses as c where x.cid=c.cid and cname<>%s"
    cursor.execute(sql,[qry])
    results=cursor.fetchall()
    for row in results:
        count=0;
        cid=row[0]
        sql="select tag from coursetags as x where x.cid=%s"
        cursor.execute(sql,[cid])
        newresults=cursor.fetchall()
        for newrow in newresults:
            for item in arr:
                if item==newrow[0]:
                    count+=3
                elif item.find(newrow[0])!=-1 or newrow[0].find(item)!=-1:
                    if newrow[0].__len__()>3 and item.__len__()>3:
                        count+=1
        sql="select cid,cname,owner,start_date,no_of_followers,category,rating from courses where cid=%s"
        cursor.execute(sql,cid)
        roo=cursor.fetchall()
        if count>1:
            www=[]
            www.append(count)
            for term in roo:
                www.append(term)
            qqq.append(www)

    qqq.sort()
    qqq.reverse()
    db.close()
    return render_to_response('coursesrec.html',{'newresults':qqq})
    #return HttpResponse(qqq)
