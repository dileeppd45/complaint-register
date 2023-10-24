from django.shortcuts import render
import mimetypes
import os
from datetime import date
from urllib import request

from django.db import connection
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect
from django.template.smartif import key
from requests import session
from textblob import TextBlob
import nltk


def index(request):
    return render(request, 'HomePage.html')


def AdminHomePage(request):
    return render(request, 'Admin/AdminHomePage.html')


def DepartmentHome(request):
    return render(request, 'Department/DepartmentHome.html')


def login(request):
    return render(request, "login.html")


def login1(request):
    if request.method == "POST":
        name = request.POST['un']
        password = request.POST['pass']
        request.session['lid'] = name
        cursor = connection.cursor()
        cursor.execute("select * from login where user_id='" + name + "' and password='" + password + "'")
        print("select * from login where admin_id='" + name + "' and password='" + password + "'")
        pins = cursor.fetchone()
        flag = 'error'
        if pins == None:
            print("not admin")
            cursorF = connection.cursor()
            cursorF.execute(
                "select department_id,category_id from department where user_id='" + name + "' and password='" + password + "'")
            print("select department_id from department where user_id='" + name + "' and password='" + password + "'")
            res = cursorF.fetchone()
            if res is not None:
                n = res[0]
                c = res[1]
                request.session['cid'] = c
                request.session['sid'] = n
                return redirect("/DepartmentHome")
            return HttpResponse("<script>alert('invalid');window.location='/';</script>")
        else:
            flag = "admin"
            print("this is admin")
    print("flag is:" + flag)
    connection.close()
    if flag == "admin":
        return redirect("/AdminHomePage")
    if flag == "res":
        return redirect("/DepartmentHome")
    if flag == "error":
        return HttpResponse("<script>alert('invalid');window.location='login';</script>")

    return HttpResponse("<script>alert('invalid');window.location='login';</script>")


def logout(request):
    return render(request, 'logout.html')


def Addcategory(request):
    if request.method == "POST":
        name = request.POST['name']
        cursor = connection.cursor()
        cursor.execute("insert into category values(null,'" + name + "')")
        return HttpResponse("<script>alert('ADDED');window.location='/AdminHomePage';</script>")
    return render(request, "Admin/Addcategory.html")


def viewCategory(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    pin = cursor.fetchall()
    print(pin)
    return render(request, "Admin/viewCategory.html", {'data': pin})


def deleteCategory(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from category where category_id='" + str(id) + "'")
    return HttpResponse("<script>alert('Deleted Succesfully');window.location='/viewCategory';</script>")


def editCategory(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from category where category_id='" + str(id) + "'")
    pin = cursor.fetchall()
    print(pin)
    return render(request, "Admin/editCategory.html", {'data': pin})


def updatecategory(request, id):
    if request.method == "POST":
        name = request.POST['name']
        cursor = connection.cursor()
        cursor.execute("update category set name='" + name + "' where   category_id  ='" + str(id) + "'")
        return HttpResponse("<script>alert('Updated');window.location='/viewCategory';</script>")
    return render(request, "Admin/editCategory.html")


def AddDepartment(request, id):
    if request.method == "POST":
        categoryid = str(id)
        fax = request.POST['TxtFax']
        name = request.POST['TxtName']
        address = request.POST['TxtAddress']
        phone = request.POST['TxtPhone']
        email = request.POST['TxtEmail']
        userid = request.POST['TxtUserid']
        password = request.POST['TxtPassword']
        cursor = connection.cursor()
        cursor.execute(
            "insert into department values(null,'" + name + "','" + address + "','" + phone + "','" + email + "','" + fax + "','" + userid + "','" + password + "','" + str(
                categoryid) + "')")
        return HttpResponse("<script>alert('Registered');window.location='/AdminHomePage';</script>")
    return render(request, "Admin/AddDepartment.html")


def viewDepartment(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from department where category_id='" + str(id) + "'")
    pin = cursor.fetchall()
    if pin == None:
        return render(request, "Admin/NoDataFound.html")
    return render(request, "Admin/viewDepartment.html", {'data': pin})


def assignpincode(request, id, sid):
    if request.method == "POST":
        departid = str(id)
        pincode = request.POST['TxtPincode']
        categoryid = str(sid)
        cursor = connection.cursor()
        cursor.execute(
            "insert into department_pincode values(null,'" + str(departid) + "','" + str(pincode) + "','" + str(
                categoryid) + "')")
        return HttpResponse("<script>alert('Registered');window.location='/AdminHomePage';</script>")
    return render(request, "Admin/assignpincode.html")


def ViewPincode(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from department_pincode where department_id='" + str(id) + "'")
    pin = cursor.fetchall()
    if pin == None:
        return render(request, "Admin/NoDataFound.html")
    return render(request, "Admin/ViewPincode.html", {'data': pin})


def editpincode(request, id):
    request.session['sid'] = id
    cursor = connection.cursor()
    cursor.execute("select * from department_pincode where department_pincode_id='" + str(id) + "'")
    pin = cursor.fetchall()
    print(pin)
    return render(request, "Admin/editpincode.html", {'data': pin})


def updatepincode(request, id):
    sid = request.session['sid']
    if request.method == "POST":
        department_id = id
        pincode = request.POST['price']
        category_id = sid
        cursor = connection.cursor()
        cursor.execute(
            "update department_pincode set department_id='" + department_id + "',pincode='" + pincode + "',category_id='" + category_id + "' where   department_pincode_id  ='" + str(
                id) + "'")
        return HttpResponse("<script>alert('Updated');window.location='/ViewPincode';</script>")
    return render(request, "Admin/editpincode.html")


def deletepincode(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from department_pincode where department_pincode_id='" + str(id) + "'")
    return HttpResponse("<script>alert('Deleted Succesfully');window.location='/ViewPincode';</script>")


def editDepartment(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from department where department_id='" + str(id) + "'")
    pin = cursor.fetchall()
    print(pin)
    return render(request, "Admin/editDepartment.html", {'data': pin})


def updateDepartment(request, id):
    if request.method == "POST":
        departid = str(id)
        name = request.POST['TxtName']
        address = request.POST['TxtAddress']
        phone = request.POST['TxtPhone']
        email = request.POST['TxtEmail']
        fax = request.POST['TxtFax']
        userid = request.POST['TxtUserid']
        password = request.POST['TxtPassword']
        cursor = connection.cursor()
        cursor.execute(
            "update department set name='" + name + "',address='" + address + "',phone='" + phone + "',email='" + email + "',fax='" + fax + "',user_id='" + userid + "',password='" + password + "' where department_id='" + str(
                departid) + "'")
        return HttpResponse("<script>alert('Updated');window.location='/viewCategory';</script>")
    return render(request, "Admin/editDepartment.html")


def deletedepart(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from department where department_id='" + str(id) + "'")
    return HttpResponse("<script>alert('Deleted Succesfully');window.location='/AdminHomePage';</script>")


def viewCategory_cmp(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    pin = cursor.fetchall()
    print(pin)
    return render(request, "Admin/viewCategory_cmp.html", {'data': pin})


def DepartmentComplaints(request, id):
    cursor = connection.cursor()
    cursor.execute("select complaint_date,count(complaint_date) from complaints  where category_id='" + str(
        id) + "' group by complaint_date ")
    pin = cursor.fetchall()
    if pin == None:
        return render(request, "Admin/NoDataFound.html")
    return render(request, "Admin/Date.html", {'data': pin})


def DepaComps(request, id, sid):
    cursor = connection.cursor()
    cursor.execute(
        "select com.*,bs.name from complaints as com join branch_staff as bs on com.branch_staff_id=bs.branch_staff_id where com.category_id='" + str(
            id) + "' and com.complaint_date='" + str(sid) + "'")
    pin = cursor.fetchall()
    if pin == None:
        return render(request, "Admin/NoDataFound.html")
    return render(request, "Admin/DepartmentComplaints.html", {'data': pin})


def Viewchats(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from complaint_chat where complaint_id='" + str(id) + "'")
    pin = cursor.fetchall()
    if pin == None:
        return render(request, "Admin/NoDataFound.html")
    return render(request, "Admin/ComplaintChat.html", {'data': pin})


def Count(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    pin = cursor.fetchall()
    print(pin)
    return render(request, "Admin/Count.html", {'data': pin})


def CountCmp(request, id):
    cursor = connection.cursor()
    cursor.execute("select count(complaint_id) as comp from complaints where category_id='" + str(id) + "'")
    pin = cursor.fetchall()
    print(pin)
    return render(request, "Admin/CountCmp.html", {'data': pin})


def DepNOtify(request):
    cursor = connection.cursor()
    cursor.execute("select * from category")
    pin = cursor.fetchall()
    print(pin)
    return render(request, "Admin/DepNOtify.html", {'data': pin})


def View_Department_N(request, id):
    request.session['cid'] = id
    cursor = connection.cursor()
    cursor.execute("select * from department where category_id='" + str(id) + "'")
    pin = cursor.fetchall()
    print(pin)
    return render(request, "Admin/View_Department_N.html", {'data': pin})


def linkSendNotification(request, id):
    request.session['did'] = id
    return render(request, "Admin/SendNotification.html")


def SendNotification(request):
    cid = request.session['cid']
    if request.method == "POST":
        notific = request.POST['TxtNotification']
        categoryid = str(cid)
        departmentid = request.session['did']
        cursor = connection.cursor()
        cursor.execute(
            "insert into notification values(null,'" + notific + "',curdate(),'" + str(categoryid) + "','" + str(
                departmentid) + "')")
        return HttpResponse("<script>alert('Registered');window.location='/AdminHomePage';</script>")
    return render(request, "Admin/SendNotification.html")


def ViewNotification(request):
    cursor = connection.cursor()
    cursor.execute(
        "select n.notification_id,n.notification,n.notification_date,c.name,d.name as dname from notification as n join category as c join department as d on n.category_id=c.category_id and n.department_id=d.department_id and d.category_id=c.category_id")
    pin = cursor.fetchall()
    print(pin)
    return render(request, "Admin/ViewNotification.html", {'data': pin})


def searchusercompliant(request):
    if request.method == "POST":
        userid = request.POST['Txtuserid']
        cursor = connection.cursor()
        cursor.execute("select * from complaints where user_id='" + str(userid) + "'")
        pin = cursor.fetchall()
        return render(request, "Admin/searchusercompliant.html", {'data': pin})
    return render(request, "Admin/searchusercompliant.html")


def User(request):
    cursor = connection.cursor()
    cursor.execute("select * from user_register")
    pin = cursor.fetchall()
    return render(request, "Admin/User.html", {'data': pin})


# -------------------------------------------------Department------------------------------------------------#


def AddStaff(request):
    ddi = request.session['sid']
    if request.method == "POST":
        bsid = request.POST['TxtBranchStaffId']
        name = request.POST['TxtName']
        phone = request.POST['TxtPhone']
        email = request.POST['TxtEmail']
        department_id = str(ddi)
        print(ddi)
        cursor = connection.cursor()
        cursor.execute(
            "insert into branch_staff values('" + bsid + "','" + name + "','" + phone + "','" + email + "','" + department_id + "')")
        return HttpResponse("<script>alert('Registered');window.location='/ViewStaff';</script>")
    return render(request, "Department/AddStaff.html")


def ViewStaff(request):
    ddi = request.session['sid']
    department_id = str(ddi)
    cursor = connection.cursor()
    cursor.execute("select * from branch_staff where department_id='" + department_id + "' ")
    pin = cursor.fetchall()
    print(pin)
    return render(request, "Department/ViewStaff.html", {'data': pin})


def DeleStaff(request, sid):
    cursor = connection.cursor()
    cursor.execute("delete from branch_staff where branch_staff_id='" + sid + "'")
    return HttpResponse("<script>alert('Deleted Succesfully');window.location='/ViewStaff';</script>")


def ViewMoreChat(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from complaint_chat where complaint_id='" + str(id) + "'")
    res = cursor.fetchall()
    return render(request, "Department/MoreChat.html", {'data': res})


def Viewdepacmplaint(request):
    ddi = request.session['lid']
    userid = str(ddi)
    cursor = connection.cursor()
    c = request.session['cid']
    cursor.execute("SELECT * from complaints where category_id='" + str(c) + "'")
    pin = cursor.fetchall()
    if pin == None:
        return render(request, "Department/NoDataFound.html")
    return render(request, "Department/Viewdepacmplaint.html", {'data': pin})


def ReplyComplaint(request, id):
    request.session['rep'] = id
    return render(request, "Department/ReplyComplaint.html")


def replycomplaintaction(request):
    id = request.session['rep']
    reply = request.POST['TxtReply']
    cursor = connection.cursor()
    cursor.execute("update complaints set reply='" + reply + "',status='replied' where complaint_id='" + str(id) + "' ")
    return HttpResponse("<script>alert('updated Succesfully');window.location='/Viewdepacmplaint';</script>")


def Compliantbasedondate(request):
    ddi = request.session['cid']
    userid = str(ddi)
    cursor = connection.cursor()

    cursor.execute("SELECT distinct complaint_date from complaints where category_id='" + str(userid) + "'")
    pin = cursor.fetchall()
    if pin == None:
        return render(request, "Department/NoDataFound.html")
    return render(request, "Department/Compliantbasedondate.html", {'data': pin})


def Department_Com_Date(request, sid):
    date = str(sid)
    cursor = connection.cursor()
    ddi = request.session['cid']
    cursor.execute(
        "select complaints.*,branch_staff.name from complaints join branch_staff on complaints.branch_staff_id=branch_staff.branch_staff_id where complaint_date='" + str(
            date) + "' and category_id='" + str(ddi) + "' ")
    pin = cursor.fetchall()
    if pin == None:
        return render(request, "Department/NoDataFound.html")
    return render(request, "Department/Department_Com_Date.html", {'data': pin})


def DepartChat(request, id):
    cursor = connection.cursor()
    cursor.execute("select * from complaint_chat where complaint_id='" + str(id) + "'")
    pin = cursor.fetchall()
    connection.close()
    if pin == None:
        return render(request, "Department/NoDataFound.html")
    return render(request, "Department/DepartChat.html", {'data': pin})


def Pincodesearch(request):
    ddi = request.session['lid']
    if request.method == "POST":
        userid = str(ddi)
        pincode = request.POST['TxtPin']
        cursor = connection.cursor()
        cursor.execute(
            "SELECT com.*,bs.name from complaints as com join  department as d join branch_staff as bs on d.category_id=com.category_id and com.branch_staff_id=bs.branch_staff_id where d.user_id='" + str(
                userid) + "' and com.pincode='" + str(pincode) + "'")
        pin = cursor.fetchall()
        print(pin)
        connection.close()
        return render(request, "Department/Pincodesearch.html", {'data': pin})
    return render(request, "Department/Pincodesearch.html")


def ViewNotificationD(request):
    ddi = request.session['lid']
    userid = str(ddi)
    cursor = connection.cursor()
    cursor.execute(
        "SELECT n.* from notification as n join department as d on n.department_id=d.department_id where d.user_id='" + str(
            userid) + "'")
    pin = cursor.fetchall()
    connection.close()
    if pin == None:
        return render(request, "Department/NoDataFound.html")
    return render(request, "Department/ViewNotification.html", {'data': pin})


def viewimage(request):
    cursor = connection.cursor()
    d = str(request.session['sid'])
    print("dept id:" + d)
    cursor.execute(
        "select department_photo.* from department_photo join department on department_photo.department_id=department.category_id  where department.department_id='" + str(
            d) + "' ")
    pin = cursor.fetchall()
    return render(request, "Department/viewimage.html", {'data': pin})


def deleteimage(request, id):
    cursor = connection.cursor()
    cursor.execute("delete from department_photo where iddepartment_photo ='" + str(id) + "' ")
    return HttpResponse("<script>alert('Deleted Succesfully');window.location='/viewimage';</script>")


def admin_view_querry(request):
    cursor = connection.cursor()
    cursor.execute("select * from user_querry")
    data = cursor.fetchall()
    return render(request, "Admin/admin_view_querry.html", {'data': data})


def admin_reply_query(request, id):
    request.session['admin_reply_query'] = id
    return render(request, "Admin/admin_reply_query.html")


def admin_reply_feedback(request):
    id = request.session['admin_reply_feedback']
    if request.method == "POST":
        reply = request.POST['reply']
        cursor = connection.cursor()
        cursor.execute("update feedback set reply='" + reply + "' where idfeedback='" + str(id) + "' ")
        return HttpResponse("<script>alert('Replied Successfully');window.location='/ViewFeedbackAdmin';</script>")


def admin_reply_query_action(request):
    id = request.session['admin_reply_query']
    if request.method == "POST":
        reply = request.POST['reply']
        cursor = connection.cursor()
        cursor.execute("update user_querry set querry_reply='" + reply + "' where iduser_querry='" + str(id) + "' ")
        return HttpResponse("<script>alert('updated Succesfully');window.location='/admin_view_querry';</script>")


def ViewFeedbackAdmin(request):
    cursor = connection.cursor()
    cursor.execute("SELECT feedback.*,category.name FROM  feedback join category  on feedback.branch_id=category.category_id")
    pin = cursor.fetchall()
    return render(request, "Admin/ViewFeedbackAdmin.html", {'data': pin})


from matplotlib import pyplot as plt

def view_graph(request):
    cursor = connection.cursor()
    file = os.getcwd()
    img = file + '/media/history_img.png'

    labels = []
    sizes = []
    explode = []
    cursor.execute("select feedback_nltk.positive_count, feedback_nltk.branch_id,category.name from feedback_nltk JOIN category ON feedback_nltk.branch_id=category.category_id  ")
    data =cursor.fetchall()
    print(data)
    for i in data:
        labels.append(i[2])
        s = i[0]
        sizes.append(s)
        explode.append(0)
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('static/images/history_img.png', dpi=100)

    connection.close()
    return render(request, "Admin/view_graph.html")



def check_feedback(request, id):
    if request.method != "POST":
        request.session['admin_reply_feedback'] = id
        cursor = connection.cursor()
        cursor.execute("select * from feedback where idfeedback='" + str(id) + "' ")
        pins = cursor.fetchone()
        print(pins)
        feedback = str(pins[3])
        to_user_id = str(pins[4])
        print(to_user_id)
        print(feedback)
        obj = TextBlob(feedback)

        sentiment = obj.sentiment.polarity
        print(sentiment)
        if sentiment == 0:
            print('The text is neutral')
        elif sentiment > 0:
            print('The text is positive')
            cursor = connection.cursor()
            cursor.execute("select * from feedback_nltk where branch_id='" + to_user_id + "' ")
            pins = cursor.fetchone()
            if pins == None:
                cursor = connection.cursor()
                cursor.execute("insert into feedback_nltk values(null,1,0,'" + to_user_id + "')")
            else:
                cursor = connection.cursor()
                cursor.execute(
                    "update feedback_nltk set positive_count=positive_count+1 where branch_id='" + to_user_id + "' ")
        else:
            print('The text is negative')
            cursor = connection.cursor()
            cursor.execute("select * from feedback_nltk where branch_id='" + to_user_id + "' ")
            pins = cursor.fetchone()
            if pins == None:
                cursor = connection.cursor()
                cursor.execute("insert into feedback_nltk values(null,0,1,'" + to_user_id + "')")
            else:
                cursor = connection.cursor()
                cursor.execute(
                    "update feedback_nltk set negative_count=negative_count+1 where branch_id='" + to_user_id + "' ")
    connection.close()
    return render(request, "Admin/FeedbackReply.html")


def ViewFeedbackNltkAdmin(request):
    cursor = connection.cursor()
    cursor.execute("select * from feedback_nltk ")
    pin = cursor.fetchall()
    connection.close()
    return render(request, "Admin/ViewFeedbackNltkAdmin.html", {'data': pin})


from matplotlib import pyplot as plt


def branch_graphs(request):
    labels = []
    sizes = []
    explode = []
    cursor = connection.cursor()
    cursor.execute(
        'select count(category.name),category.name,complaints.category_id from category inner join complaints on category.category_id = complaints.category_id group by category.name;')
    data = cursor.fetchall()
    for i in data:
        sizes.append(i[0])
        labels.append(i[1])
        explode.append(0)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.savefig('media/complaints.png', dpi=100)

    connection.close()
    return render(request, 'Admin/complaints_visual.html')
