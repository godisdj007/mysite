__author__ = 'ajaysingh'

from django.shortcuts import render_to_response
import MySQLdb
from django.http import HttpResponse,HttpResponseRedirect
from django.core.validators import email_re
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
import datetime

def assignment(request,offset):
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
            sql1="select asid,cid,assname,post_by,post_date,type from assignment where cid=%s and type=%s"
            arr1=[offset,'mcq']
            cursor.execute(sql1,arr1)
            result1=cursor.fetchall()

            sql2="select asid,cid,assname,post_by,post_date,type from assignment where cid=%s and type=%s"
            arr2=[offset,'descriptive']
            cursor.execute(sql2,arr2)
            result2=cursor.fetchall()
            msg=""
            sql="select cid,cname,owner,category from courses where cid=%s and owner=%s"
            arr=[offset,request.session['umail']]
            cursor.execute(sql,arr)
            x = [row[0] for row in cursor.fetchall()]
            if  x:
                flag=1
            else:
                flag=""
            db.close()
            return render_to_response('assignment.html',{'result1':result1,'result2':result2,'msg':msg,'flag':flag})
        db.close()
        return render_to_response('all courses.html',{'msg':msg})


def viewassignment(request):
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
          asid=int(request.GET["asid"])
          type=str(request.GET["type"])
          qt=int(request.GET["qt"])
          sql="select asid,cid,user from usermarks where asid=%s and cid=%s and user=%s"
          arr=[asid,cid,request.session['umail']]
          cursor.execute(sql,arr)
          x = [row[0] for row in cursor.fetchall()]
          if x:
             msg="You did this already,Can't do it again"
          else:
             sql1="select v.qno,v.cid,v.asid,v.question,v.options,v.answer from viewdescriptive as v,assignment as a\
                  WHERE v.asid =a.asid and v.cid =a.cid and v.asid=%s and v.cid=%s and  a.type = %s"
             arr1=[asid,cid,type]
             cursor.execute(sql1,arr1)
             result1=cursor.fetchall()
             num=cursor.rowcount;
             if num>qt:
               if(type=='mcq'):
                    subresult = result1[qt]
                    y=result1[qt][4]
                    arr=y.split('~!@')
                    size1=range(len(arr)-1)
                    result1=0
               else:
                   arr="descriptive"
                   size1="lenthy"
                   subresult="0"
               sql2="select assname from assignment where asid=%s and cid=%s and type=%s"
               arr2=[asid,cid,type]
               cursor.execute(sql2,arr2)
               result2=cursor.fetchall()
               x=result2[0][0]
               qt+=1
               db.close()
               return render_to_response('viewassignment.html',{'result1':result1,'x':x,'size1':size1,'qt':qt,\
                                       'subresult':subresult,'asid':asid,'cid':cid,'type':type,'arr':arr,'num':num})
             else:
                  # msg="HELLO"
                   db.close
                   return HttpResponseRedirect("/assignment/%d"%(cid))
          db.close
          return render_to_response('viewassignment.html',{'msg':msg,'cid':cid})
        db.close()
        return render_to_response('all courses.html',{'msg':msg})



def finishassignment(request):
    if "umail" not in request.session or request.session['umail']=="":
          return HttpResponseRedirect("/login/")
    else:
          cid=int(request.GET['cid1'])
          db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
          cursor = db.cursor()
          sql="select cid from enrollments where cid='%d' and uid='%s'" %(cid,request.session['umail'])
          cursor.execute(sql)
          x = [row[0] for row in cursor.fetchall()]
          if not x:
              msg="not enrolled to this course.. go back"
          else:
            asid=int(request.GET["asid1"])
            marks=int(request.GET["marks"])
            sql="select asid,cid,user from usermarks where asid=%s and cid=%s and user=%s"
            arr=[asid,cid,request.session['umail']]
            cursor.execute(sql,arr)
            x = [row[0] for row in cursor.fetchall()]
            if x:
                 msg1="Please Don't reload page..Your rank can't be increase.. :)"
            else:
                 sql="insert into usermarks (asid,cid,user,marks) values(%s,%s,%s,%s)"
                 args=[asid,cid,request.session['umail'],marks]
                 cursor.execute(sql,args)
                 db.commit()
                 msg1="ASSIGNMENT DONE"
            sql1="select marks from usermarks WHERE asid=%s and cid=%s"
            arr1=[asid,cid]
            cursor.execute(sql1,arr1)
            result1=cursor.fetchall()
            usernum=cursor.rowcount;
            n1=list()
            for row in result1:
               n1.append(row[0])
            n1.sort()
            n1.reverse()
            for x in n1:
                if(marks==x):
                    pos=n1.index(x)
            pos+=1
            db.close()

            return render_to_response('assignment.html',{'msg1':msg1,'cid':cid,'asid':asid,'n1':n1,'pos':pos,\
                                                            'usernum':usernum})
              #return HttpResponse("ASSIGNMENT DONE")
          db.close()
          return render_to_response('all courses.html',{'msg':msg})


def createassignment(request):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
        cursor = db.cursor()
        cid=int(request.GET['cid'])
        sql="select cid from enrollments where cid='%d' and uid='%s'" %(cid,request.session['umail'])
        cursor.execute(sql)
        x = [row[0] for row in cursor.fetchall()]
        if not x:
            msg="not enrolled to this course.. go back"
        else:
            msg=""
            sql="select cid,cname,owner,category from courses where cid=%s and owner=%s"
            arr=[cid,request.session['umail']]
            cursor.execute(sql,arr)
            x = [row[0] for row in cursor.fetchall()]
            db.close()
            if  not x:
                   msg="You are not owner of this course..Can't add assignment.."
                   return render_to_response('all courses.html',{'msg':msg})
            else:
                return render_to_response('createassignment.html',{'cid':cid,'msg':msg})
        db.close()
        return render_to_response('all courses.html',{'msg':msg})



def addassignment(request):
        if "umail" not in request.session or request.session['umail']=="":
            return HttpResponseRedirect("/login/")
        else:
            db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
            cursor = db.cursor()
            cid=int(request.GET['cid'])
            dt=datetime.date.today()
            type=str(request.GET["type"])
            assname=str(request.GET["assname"])
            sql="select cid from enrollments where cid='%d' and uid='%s'" %(cid,request.session['umail'])
            cursor.execute(sql)
            x = [row[0] for row in cursor.fetchall()]
            if not x:
                msg="not enrolled to this course.. go back"
            else:
                msg=""
                sql="select cid,cname,owner,category from courses where cid=%s and owner=%s"
                arr=[cid,request.session['umail']]
                cursor.execute(sql,arr)
                x = [row[0] for row in cursor.fetchall()]
                if  not x:
                    msg="You are not owner of this course..Can't add assignment.."
                    return render_to_response('all courses.html',{'msg':msg})
                else:
                    sql="select cid,assname,post_by,type from assignment where cid=%s and assname=%s and type=%s"
                    arr=[cid,assname,type]
                    cursor.execute(sql,arr)
                    x = [row[0] for row in cursor.fetchall()]
                    if x:
                        msg="'ASSIGNMENT NAME' exists For This Couse & assignment type.." \
                            "Plaese Change value of one of them"
                    else:
                       sql="insert into assignment (cid,assname,post_by,post_date,type) values(%s,%s,%s,%s,%s)"
                       args=[cid,assname,str(request.session['umail']),dt,type]
                       cursor.execute(sql,args)
                       db.commit()
                       sql="select max(asid) from assignment"
                       cursor.execute(sql)
                       result=cursor.fetchall()
                       asid=result[0][0]
                       db.close()
                       return render_to_response('addassignment_question.html',{'cid':cid,'asid':asid,\
                                                                       'assname':assname,'type':type})
                    db.close()
                    return render_to_response('createassignment.html',{'cid':cid,'msg':msg})
            db.close()
            return render_to_response('all courses.html',{'msg':msg})



def addassignment_question(request):
    if "umail" not in request.session or request.session['umail']=="":
        return HttpResponseRedirect("/login/")
    else:
        db = MySQLdb.connect(user='root', db='devesh mysite', passwd='', host='')
        cursor = db.cursor()
        cid=int(request.GET['cid'])
        type=str(request.GET["type"])
        assname=str(request.GET["assname"])
        asid=int(request.GET['asid'])
        question=str(request.GET["question"])
        sql="select cid from enrollments where cid='%d' and uid='%s'" %(cid,request.session['umail'])
        cursor.execute(sql)
        x = [row[0] for row in cursor.fetchall()]
        if not x:
            msg="not enrolled to this course.. go back"
        else:
            msg=""
            sql="select cid,cname,owner,category from courses where cid=%s and owner=%s"
            arr=[cid,request.session['umail']]
            cursor.execute(sql,arr)
            x = [row[0] for row in cursor.fetchall()]
            if  not x:
                msg="You are not owner of this course..Can't add assignment.."
                return render_to_response('all courses.html',{'msg':msg})
            else:
                if(type=='mcq'):
                    a=str(request.GET["a"])
                    b=str(request.GET["b"])
                    c=str(request.GET["c"])
                    d=str(request.GET["d"])
                    answer=str(request.GET[str(request.GET["answer"])])
                    n1=a+'~!@'+b+'~!@'+c+'~!@'+d
                    sql="insert into viewdescriptive (cid,asid,question,options,answer)values(%s,%s,%s,%s,%s)"
                    args=[cid,asid,question,n1,answer]
                    cursor.execute(sql,args)
                    db.commit()
                else:
                    sql="insert into viewdescriptive (cid,asid,question)values(%s,%s,%s)"
                    args=[cid,asid,question]
                    cursor.execute(sql,args)
                    db.commit()
                db.close()
                return render_to_response('addassignment_question.html',{'cid':cid,'asid':asid,\
                                                                         'assname':assname,'type':type})
        db.close()
        return render_to_response('all courses.html',{'msg':msg})
