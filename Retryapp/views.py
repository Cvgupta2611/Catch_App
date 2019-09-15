from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, render_to_response
import mysql.connector
from django.template.loader import render_to_string
from mysql.connector import Error
from django.core.mail import EmailMessage
from django.core.files.storage import FileSystemStorage
import re
import play_scraper
import requests
import json
import matplotlib.pyplot as plt
import simplejson
from textblob import TextBlob
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup, element
from datetime import datetime
from datetime import timedelta
import tweepy, datetime


access_token = '3191000011-FbWkMM5vseJfz3s5cFXeCduR8UJp7ateyS4FLTh'
access_token_secret = 'yTfoRomIcuNKXtm47zEOZk23q2YcdWICDAeyngV1kta7U'
consumer_key = 'nZ36Qdt3EYGFY2KYJPX1iFDZV'
consumer_secret = 'ChJQKSG99DOMVekigTrrqptXSKuYyen1Si2gXdcIU7vvRfwEb6'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                               password='12345678'
                               , auth_plugin='mysql_native_password')
cursor = conn.cursor()



# Create your views here.
# from Retry.result_portion import analysis
# from Retry.result_portion import sentimentanalysis


def show(request):
    #return render(request,'appauth.html')
    #return render(request,'editprofile_new.html')
    #return render(request,'user_request.html')
    #return render(request, '404.html')
    #return render(request, 'added.html')
    #return render(request, 'index.html')
    #return render(request,'result_software_unauth.html')

    if (request.session.get('lid') is not None):
        return dashboard(request)
    else:
        return render(request, 'index.html')



def result(request):
    if (request.session.get('lid') is not None):
        return render(request, 'new_result.html')
    else:
        return render(request, 'login.html')


def re_site(request):
    return render(request, 'website.html')


def edit(request):
    if (request.session.get('lid') is not None):
        lid = request.session.get('lid')

        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root', password='12345678')
        cursor = conn.cursor()

        query2 = "select * from login where lid='%d'" % (lid)


        cursor.execute(query2)
        a = cursor.fetchone()
        email = a[1]
        password = a[2]
        query = "select * from registration where lid='%d'" % (lid)
        cursor.execute(query)
        b = cursor.fetchone()
        #print("value of b", b)
        name = b[1]
        age = b[2]
        gender = b[3]
        education = b[4]
        state = b[5]
        income=b[6]
        profession=b[7]
        image=b[8]
        #print(image)
        #print(b[0])
        query1 = "select interest from user_interest where rid='%d'" % (b[0])
        cursor.execute(query1)
        c = cursor.fetchall()
        #print("interest",c)
        list1 = []
        for i in c:
            list1.append(i[0])
        #print('loist',list1)

        profile_details = [name, age, gender, education, state, income, profession,image,email,password]

        data = {'c':list1}
        data = simplejson.dumps(data)
        #return HttpResponse(data, content_type='application/json')

        return render(request, 'editprofile_new.html', {'profile_details': profile_details,'c':data})

        # return render(request,'editprofile.html')
    else:
        return render(request, 'login.html')


def abt(request):
    return render(request, 'originalabout.html')


def login(request):
    return render(request, 'login.html')


def forgotpwd(request):
    return render(request, 'forgotpwd.html')


def added(request):
    if (request.session.get('lid') is not None):
        #print("request", request.session.get('lid'))

        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                       password='12345678'
                                       , auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        lid=request.session.get('lid')
        q="select app_id from user_app WHERE user_id='%d'"%(lid)
        cursor.execute(q)
        a=cursor.fetchall()
        list=[]
        rate=[]
        for i in a:
            a_id=i[0]
            query="select * from app_details where app_id='%d'"%(a_id)
            cursor.execute(query)
            f=cursor.fetchall()
            ##print(f[0])
            list.append(f[0])
        #print("list",list)
        for k in list:
            rating=float(k[3])
            r=rating/20
            rate.append(r)
        d=(zip(list,rate))
        data=set(d)
        #print("data",data)
        q="select web_id from user_website WHERE user_id='%d'"%(lid)
        cursor.execute(q)
        a=cursor.fetchall()
        print("web",a)
        list=[]
        for i in a:
            a_id=i[0]
            print(a_id)
            query="select * from web where web_id='%d'"%(a_id)
            cursor.execute(query)
            f=cursor.fetchall()
            ##print(f[0])
            list.append(f[0])
        #print("list1",list)

        q="select soft_id from user_software WHERE user_id='%d'"%(lid)
        cursor.execute(q)
        a=cursor.fetchall()
        list1=[]
        for i in a:
            a_id=i[0]
            query="select * from new_software where new_software_id='%d'"%(a_id)
            cursor.execute(query)
            f=cursor.fetchall()
            ##print(f[0])
            list1.append(f[0])
        #print("list2",list1)


        return render(request,'added.html',{'list':data,'web':list,'soft':list1})
    else:
        return render(request, 'login.html')


def getpwd(request):
    try:
        email = request.GET.get('email')
        print(email)

        query = "select password from login where email='%s' " % (email)

        cursor.execute(query)
        a = cursor.fetchone()
        print("value",a)

        body = a[0]
        #print("value of a",body)
        email = EmailMessage('Forget Password', body, to=[email])
        email.send()
        msg = "Your Password has been sent to Registered Gmail"
        return render(request, 'login.html', {'msg': msg})

        conn.commit()

    except Error as e:
        print(e)

    finally:

        cursor.close()
        conn.close()


def signup(request):
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root', password='12345678')
    cursor = conn.cursor()
    query1 = "select * from age_range "

    cursor.execute(query1)
    age_range = cursor.fetchall()

    query2 = "select * from educational_background "
    cursor.execute(query2)
    educational_background = cursor.fetchall()

    query3 = "select * from state "
    cursor.execute(query3)
    state = cursor.fetchall()

    query4 = "select * from language "
    cursor.execute(query4)
    language = cursor.fetchall()

    query5 = "select * from income "
    cursor.execute(query5)
    income = cursor.fetchall()

    query6 = "select * from profession "
    cursor.execute(query6)
    profession = cursor.fetchall()

    query7 = "select * from interest "
    cursor.execute(query7)
    interest = cursor.fetchall()

    return render(request, 'register_1.html',
                  {'age_range': age_range, 'educational_background': educational_background, 'state': state,
                   'language': language, 'income': income, 'profession': profession, 'interest': interest})


def contact(request):
    return render(request, 'contact.html')


def feedback(request):
    return render(request, 'feedback.html')


def trending(request):
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root', password='12345678')
    cursor = conn.cursor()

    category = "treanding"
    query = "select * from app_details where app_category='%s' ORDER BY rating DESC" % (category)
    cursor.execute(query)
    a = cursor.fetchall()
    ##print(a)
    count = 0
    ##print(a[0])
    rate = []
    r = 0
    for i in a:
        # rating=a[0]
        # #print(rating)
        rating = float(i[3])
        ##print("rating",rating)
        r = rating / 20
        rate.append(r)
    list = (zip(a, rate))
    l = set(list)
    #print(l)
    count = 0
    newlist = []
    for k in l:
        count = count + 1
        if (count <= 8):
            #print(count)
            newlist.append(k)
    #print(newlist)

    category2 = "Trending"
    query2 = "select * from web WHERE category='%s' ORDER BY global_rank ASC " % (category2)
    cursor.execute(query2)
    c = cursor.fetchall()
    #print(c)
    count = 0
    c1 = []
    for l in c:
        count = count + 1
        if (count <= 8):
            c1.append(l)

    category1 = "trending"
    query1 = "select * from new_software where status='%s' ORDER BY rating DESC " % (category1)
    cursor.execute(query1)
    m = cursor.fetchall()
    #print(m)
    count = 0
    soft = []
    for l in m:
        ##print(l)
        count = count + 1
        if (count <= 8):
            ##print(count)
            soft.append(l)
            ##print(soft)

            #return render(request, 'softwareguest.html',{})

    return render(request, 'trending.html', {'list': newlist, 'soft': soft, 'web': c1})


    #return render(request, 'popular.html')


def popular(request):
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root', password='12345678')
    cursor = conn.cursor()

    category = "new"
    query = "select * from app_details where app_category='%s' ORDER BY rating DESC" % (category)
    cursor.execute(query)
    a = cursor.fetchall()
    ##print(a)
    count = 0
    ##print(a[0])
    rate = []
    r = 0
    for i in a:
        # rating=a[0]
        # #print(rating)
        rating = float(i[3])
        ##print("rating",rating)
        r = rating / 20
        rate.append(r)
    list = (zip(a, rate))
    l = set(list)
    #print("value",l)
    count = 0
    newlist = []
    for k in l:
        count = count + 1
        if (count <= 8):
            #print(count)
            newlist.append(k)
    #print(newlist)

    category1 = "new"
    query1 = "select * from new_software where status='%s'ORDER BY rating DESC " % (category1)
    cursor.execute(query1)
    m = cursor.fetchall()
    #print(m)
    count = 0
    soft = []
    for l in m:
        ##print(l)
        count = count + 1
        if (count <= 8):
            #print(count)
            soft.append(l)
    #print(soft)

    #return render(request, 'softwareguest.html',{})

    return render(request, 'popular1.html', {'list': newlist, 'soft': soft})


    #return render(request, 'popular.html')


def option(request):
    guest = request.GET.get('guest')
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root', password='12345678')
    cursor = conn.cursor()

    if (guest == 'Application'):
        category = "all"
        query = "select * from app_details where app_category='%s'" % (category)
        cursor.execute(query)
        a = cursor.fetchall()
        ##print(a)
        count = 0
        ##print(a[0])
        rate = []
        r = 0
        for i in a:
            # rating=a[0]
            # #print(rating)
            rating = float(i[3])
            ##print("rating",rating)
            r = rating / 20
            rate.append(r)
        list = (zip(a, rate))
        l = set(list)
        #print(l)
        return render(request, 'appguest.html', {'list': l})

        #return render(request, 'appguest.html',{'app':a,'rating':rate})

    if (guest == 'Website'):
        category1 = "trending"
        query1 = "select * from web where category='%s'" % (category1)
        cursor.execute(query1)
        b = cursor.fetchall()
        return render(request, 'webguest.html', {'web': b})

    if (guest == 'Software'):
        category1 = "trending"
        query1 = "select * from new_software where status='%s'" % (category1)
        cursor.execute(query1)
        m = cursor.fetchall()

        return render(request, 'softwareguest.html', {'soft': m})


def store_data(request):
    try:

        username = request.POST.get('username')
        email = request.POST.get('email')
        age = request.POST.get('age')
        educational_background1 = request.POST.get('educational_background1')
        #language1 = request.POST.get('lan1')
        state = request.POST.get('state')
        gender = request.POST.get('gender')
        #marital_status = request.POST.get('marital_status')
        income = request.POST.get('income')
        profession1 = request.POST.get('profession1')
        interest = request.POST.getlist('interest')
        password = request.POST.get('password')
        c_password = request.POST.get('confirm_password')
        image = '/images/default-profile-1.png'
        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root', password='12345678')
        cursor = conn.cursor()
        query = "select * from login where email='%s'" % (email)
        cursor.execute(query)
        cfrm_email = cursor.fetchall()
        if (cfrm_email == []):

            if (password == c_password):
                query = "insert into login(email,password,role) VALUES ('%s','%s','%s')" % (email, password, 'user')

                cursor.execute(query)
                conn.commit()

                lid = int(cursor.lastrowid)
                if (educational_background1 != 'other' and profession1 != 'other'):
                    #print("1st query")
                    query1 = "insert into registration(username,age,gender,education,state,income,profession,image,status,lid) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%d')" % (
                        username, age, gender, educational_background1, state, income,
                        profession1, image, 'accepted', lid)
                    #print(query1)
                    cursor.execute(query1)
                    conn.commit()
                    rid = int(cursor.lastrowid)
                    for i in interest:
                        query2 = "insert into user_interest(interest,rid) VALUES ('%s','%d')" % (i, rid)
                        cursor.execute(query2)
                        conn.commit()
                elif (educational_background1 != 'other' and profession1 == 'other'):
                    #print("2st query")
                    profession2 = request.POST.get('profession2')
                    #educational_background2 = request.POST.get('educational_background2')
                    # language2 = request.POST.get('lan2')
                    profession2 = request.POST.get('profession2')
                    query3 = "insert into registration(username,age,gender,education,state,income,profession,image,status,lid) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%d')" % (
                        username, age, gender, educational_background1, state, income,
                        profession2, image, 'pending', lid)
                    cursor.execute(query3)
                    conn.commit()
                    rid = int(cursor.lastrowid)
                    for i in interest:
                        query32 = "insert into user_interest(interest,rid) VALUES ('%s','%d')" % (i, rid)
                        cursor.execute(query32)
                        conn.commit()

                elif (educational_background1 == 'other' and profession1 != 'other'):
                    #print("3st query")
                    #print(username)
                    #profession2 = request.POST.get('profession2')
                    educational_background2 = request.POST.get('educational_background2')
                    # language2 = request.POST.get('lan2')
                    profession2 = request.POST.get('profession2')
                    query4 = "insert into registration(username,age,gender,education,state,income,profession,image,status,lid) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%d')" % (
                        username, age, gender, educational_background2, state, income,
                        profession1, image, 'pending', lid)
                    #print(query4)
                    cursor.execute(query4)
                    conn.commit()
                    rid = int(cursor.lastrowid)
                    for i in interest:
                        query42 = "insert into user_interest(interest,rid) VALUES ('%s','%d')" % (i, rid)
                        cursor.execute(query42)
                        conn.commit()

                else:
                    #print("4th query")
                    educational_background2 = request.POST.get('educational_background2')
                    #language2 = request.POST.get('lan2')
                    profession2 = request.POST.get('profession2')
                    query1 = "insert into registration(username,age,gender,education,state,income,profession,image,status,lid) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%d')" % (
                        username, age, gender, educational_background2, state, income,
                        profession2, image, 'pending', lid)
                    cursor.execute(query1)
                    conn.commit()
                    rid = int(cursor.lastrowid)
                    for i in interest:
                        query2 = "insert into user_interest(interest,rid) VALUES ('%s','%d')" % (i, rid)
                        cursor.execute(query2)
                        conn.commit()

                # msg="login!!! data added....!"
                return render(request, 'login.html')
            else:
                Re_enter_password = "Renter your password......"
                return render(request, 'register_1.html', {'Re_enter_password': Re_enter_password})

        else:
            email_existed = "This Email-Id has already Registered"
            conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                           password='12345678')
            cursor = conn.cursor()
            query1 = "select * from age_range "

            cursor.execute(query1)
            age_range = cursor.fetchall()

            query2 = "select * from educational_background "
            cursor.execute(query2)
            educational_background = cursor.fetchall()

            query3 = "select * from state "
            cursor.execute(query3)
            state = cursor.fetchall()

            query4 = "select * from language "
            cursor.execute(query4)
            language = cursor.fetchall()

            query5 = "select * from income "
            cursor.execute(query5)
            income = cursor.fetchall()

            query6 = "select * from profession "
            cursor.execute(query6)
            profession = cursor.fetchall()

            query7 = "select * from interest "
            cursor.execute(query7)
            interest = cursor.fetchall()

            return render(request, 'register_1.html',
                          {'age_range': age_range, 'educational_background': educational_background, 'state': state,
                           'language': language, 'income': income, 'profession': profession, 'interest': interest,
                           'email_existed': email_existed})







    except Error  as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

def dashboard(request):
    #print("hello")
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root', password='12345678')
    cursor = conn.cursor()

    category = "treanding"
    query = "select * from app_details where app_category='%s' ORDER BY rating DESC" % (category)
    cursor.execute(query)
    a = cursor.fetchall()
    ##print(a)
    count = 0
    ##print(a[0])
    rate = []
    r = 0
    for i in a:
        # rating=a[0]
        # #print(rating)
        rating = float(i[3])
        ##print("rating",rating)
        r = rating / 20
        rate.append(r)
    list = (zip(a, rate))
    l = set(list)
    #print(l)
    count = 0
    newlist = []
    for k in l:
        count = count + 1
        if (count <= 4):
            #print(count)
            newlist.append(k)
    #print(newlist)

    category2 = "Trending"
    query2 = "select * from web WHERE category='%s' ORDER BY global_rank ASC " % (category2)
    cursor.execute(query2)
    c = cursor.fetchall()
    #print(c)
    count = 0
    c1 = []
    for l in c:
        count = count + 1
        if (count <= 4):
            c1.append(l)

    category1 = "trending"
    query1 = "select * from new_software where status='%s' ORDER BY rating DESC " % (category1)
    cursor.execute(query1)
    m = cursor.fetchall()
    #print(m)
    count = 0
    soft = []
    for l in m:
        ##print(l)
        count = count + 1
        if (count <= 4):
            ##print(count)
            soft.append(l)
    #print(newlist,soft,c1)
    if (request.session.get('lid') is not None):
        lid=request.session.get('lid')
        q="select * from registration where lid='%d'"%(lid)
        cursor.execute(q)
        a=cursor.fetchone()
        ##print("value of a",a)

        if(a[9]=='accepted'):
            #print("hello")
            age=a[2]
            age=age.lower()
            gender =a[3]
            gender=gender.lower()
            education=a[4]
            education=education.lower()
            #print("edu",education)
            q1="select * from user_interest where rid='%d'"%(a[0])
            cursor.execute(q1)
            interest=cursor.fetchall()
            ##print(interest)
            interest_list=[]
            for i in interest:
                interest_list.append(i[1])



            ##print(interest_list)
            if(interest_list[0] is not None):

                interest1 =interest_list[0]
                interest1=interest1.lower()
            if(interest_list[1] is not None):
                interest2 =interest_list[1]
                interest2=interest2.lower()
            else:
                interest2 =''
                interest2=interest2.lower()
            # if(interest_list[2] is not None):
            #     interest3 =interest_list[2]
            #     interest3=interest3.lower()
            # else:
            #     interest3 =interest_list[2]
            #     interest3=interest3.lower()
            # print("interest_list",interest_list)
            #
            # if(interest_list[3] is not None):
            #     interest4 =interest_list[3]
            #     interest4=interest4.lower()
            # else:
            #     interest4 =''
            #     interest4=interest4.lower()
            # if(interest_list[4] is not None):
            #     interest5 =interest_list[4]
            #     interest5=interest5.lower()
            # else:
            #     interest5 =interest_list[4]
            #     interest5=interest5.lower()


            list1=[]
            list2=[]
            list3=[]
            list4=[]
            q2="select *  from recommendation_data where age='%s' "%(age)
            cursor.execute(q2)
            re_data = cursor.fetchall()
            for i in re_data:
                if(i[1]==gender):
                    list1.append(i)


            for j in list1:
                if(j[8]==education):
                    list2.append(j)
            ##print(list2)
            for k in list2:
                if(k[2]==interest1 or k[3]==interest1 or k[4]==interest1 or k[5]==interest1 or k[6]==interest1):
                    list3.append(k)
            print(list3)
            ##print(len(list3))

            # for p in list3:
            #     if(p[2]==interest2 or p[3]==interest2 or p[4]==interest2 or p[5]==interest2 or p[6]==interest2):
            #         list4.append(p)
            #print(list4)
            #print(len(list4))
            list8=[]

            for k in list3:
                if k[7] in list8:
                    pass

                else:
                    list8.append(k[7])
            print("list8",list8)
            #print(len(list8))
            print("list8",list8)
            google_app=[]
            count =0
            for name in list8:
                if(count<4):
                    ##print(name)
                    if(name == 'bank application'):
                        name ='phonepe'
                    app_name = play_scraper.search(name, page=1)
                    app_search = app_name[0]
                    title = app_search['title']
                    count =count+1


                    query = "select * from app_details where title='%s'" % (title)
                    cursor.execute(query)
                    a = cursor.fetchall()
                    # #print(a)
                    # count = 0
                    #print(a[0])
                    google_app.append(a[0])

                rate = []
                r = 0
                for i in google_app:
                    # rating=a[0]
                    # ##print(rating)
                    rating = float(i[3])
                    ###print("rating",rating)
                    r = rating / 20
                    rate.append(r)
                list = (zip(google_app , rate))
                l = set(list)
                ##print("value of l",l)


            return render(request, 'dashoard.html',{'list': newlist, 'soft': soft, 'web': c1,'list1':l})
        else:
            recommend_msg='''Dear user, As you choose other profession or educational backgrond at your registration time so we are not able to recommend you application,website and software because we have not enough data at this time but you can use other functionality of CatchApp.
            Sorry for inconvenience...'''

            return render(request, 'dashoard.html',{'list': newlist, 'soft': soft, 'web': c1,'recommend_msg':recommend_msg})


def signin(request):
    try:
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email, password)

        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                       password='12345678'
                                       , auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        query = "select lid,role from login where email='%s' and password='%s' " % (email, password)
        # query="delete from login where email='%s' and password='%s'"%(email,password)

        cursor.execute(query)
        a = cursor.fetchall()

        #print("value of a:", a)


        if a:
            role = a[0][1]
            #print("role:", role)
            lid = a[0][0]
            #print(lid)
            if (role == 'user' ):

                quer = "select status from registration where lid='%d'"  % (lid)
                cursor.execute(quer)
                x=cursor.fetchall()
                status=x[0][0]
                if(status!='pending'):

                    query1 = "select username,image from registration where lid='%d' " % (lid)

                    cursor.execute(query1)
                    b = cursor.fetchone()
                    #print("value of b", b)
                    name = b[0]
                    image = b[1]
                    #print(image)

                    request.session['lid'] = lid
                    request.session['user_name'] = name
                    request.session['user_image'] = image

                    return dashboard(request)

                    #return render(request, 'dashoard.html', {'image': image, 'name': name})
                else:
                    msg='Your Registration is not accepted by Admin'
                    return render(request,'login.html',{'msg':msg})




            elif(role=='admin'):
                request.session['lid'] = lid
                return render(request, 'admin_dashboard.html')


        else:
            msg='enter valid data'
            return render(request,'login.html',{'msg':msg})



        conn.commit()


    except Error as e:
        print(e)

    finally:

        print("A")


def smore(request):
    if (request.session.get('lid') is not None):
        auth = request.GET.get('auth')

        if (auth == "Application"):
            #print("inside")
            conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                           password='12345678'
                                           , auth_plugin='mysql_native_password')
            cursor = conn.cursor()
            status = 'trending'
            query = "select * from app_details where app_category ='%s'" % (status)
            cursor.execute(query)
            a = cursor.fetchall()
            return render(request, 'appauth.html', {'a': a})

        if (auth == "Website"):
            return render(request, 'webauth.html')

        if (auth == 'Software'):
            return render(request, 'softwareauth.html')
    else:
        return render(request, 'login.html')


def trending_application(request):
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678'
                                   , auth_plugin='mysql_native_password')
    cursor = conn.cursor()
    category = "treanding"
    query = "select * from app_details where app_category='%s' ORDER BY rating DESC " % (category)
    cursor.execute(query)
    a = cursor.fetchall()
    rate = []
    r = 0
    for i in a:
        # rating=a[0]
        # #print(rating)
        rating = float(i[3])
        ##print("rating",rating)
        r = rating / 20
        rate.append(r)
    list = (zip(a, rate))
    l = set(list)
    #print(l)

    return render(request, 'trendingapp.html', {'app': l})


def new_application(request):
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678'
                                   , auth_plugin='mysql_native_password')
    cursor = conn.cursor()
    category = "new"
    query = "select * from app_details where app_category='%s' ORDER BY rating DESC " % (category)
    cursor.execute(query)
    a = cursor.fetchall()
    rate = []
    r = 0
    for i in a:
        # rating=a[0]
        # #print(rating)
        rating = float(i[3])
        ##print("rating",rating)
        r = rating / 20
        rate.append(r)
    list = (zip(a, rate))
    l = set(list)
    #print(l)

    return render(request, 'popularapp.html', {'app': l})


def website(request):
    category = "trending"
    query = "select * from web WHERE category='%s' ORDER by global_rank ASC " % (category)
    cursor.execute(query)
    a = cursor.fetchall()
    return render(request, 'popularweb.html', {'web': a})


def new_web(request):
    category = request.GET.get('name')
    #print(category)
    query = "select * from web WHERE category='%s' ORDER BY global_rank ASC " % (category)
    cursor.execute(query)
    a = cursor.fetchall()
    #print(a)
    return render(request, 'trendingweb.html', {'web': a,'name':category})


def trending_software(request):
    category1 = "trending"
    query1 = "select * from new_software where status='%s' ORDER BY rating DESC " % (category1)
    cursor.execute(query1)
    m = cursor.fetchall()
    #print(m)
    #count=0
    # soft=[]
    # for l in m:
    #     ##print(l)
    #     count=count+1
    #     if(count<=8):
    #         #print(count)
    #         soft.append(l)
    # #print(soft)



    return render(request, 'trendingsoftware.html', {'soft': m})


def new_software(request):
    category1 = "new"
    query1 = "select * from new_software where status='%s' ORDER BY rating DESC " % (category1)
    cursor.execute(query1)
    m = cursor.fetchall()
    #print(m)
    #count=0
    # soft=[]
    # for l in m:
    #     ##print(l)
    #     count=count+1
    #     if(count<=8):
    #         #print(count)
    #         soft.append(l)
    # #print(soft)



    return render(request, 'popularsoftware.html', {'soft': m})


def profile(request):
    if (request.session.get('lid') is not None):

        lid = request.session.get('lid')
        #print("lid", lid)

        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                       password='12345678'
                                       , auth_plugin='mysql_native_password')
        cursor = conn.cursor()

        query2 = "select email from login where lid='%d'" % (lid)

        cursor = conn.cursor()
        cursor.execute(query2)
        a = cursor.fetchone()
        email = a[0]

        query = "select * from registration where lid='%d'" % (lid)
        cursor.execute(query)
        b = cursor.fetchone()
        rid = b[0]
        # #print("dharti", b)
        query = "select * from user_interest where rid='%d'" % (rid)
        cursor.execute(query)
        interest2 = cursor.fetchall()
        interest = []
        for i in interest2:
            x = i[1]
            y = ","
            z = "".join((x, y))
            interest.append(z)
        #print(interest)

        return render(request, 'profile.html', {'profile_details': b, 'email': email, 'interest': interest,})
    else:
        return render(request, 'login.html')


def upload(request):
    try:
        #print("hello")
        # name = request.GET.get('name')
        lid = request.session.get('lid')
        name = request.POST.get('username')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        profession = request.POST.get('profession1')
        state = request.POST.get('state')
        income = request.POST.get('income')
        educational_background1 = request.POST.get('educational_background1')

        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                               password='12345678'
                               , auth_plugin='mysql_native_password')
        cursor = conn.cursor()



        password = request.POST.get('password')

        interest = request.POST.getlist('interest')

        if request.FILES:
            #print("abc")
            myfile = request.FILES['select_image']

            fs = FileSystemStorage()
            filename = myfile.name
            #print("Filename=====", filename)
            extension = filename.split('.')
            #print("Extension=====", extension)
            uploaded_file_name = name + "." + extension[1]

            filename = fs.save(uploaded_file_name, myfile)
            #print("uploaded_file_name", filename)

            image1 = fs.url(filename)
            #print("uploaded_file_url", image1)
            request.session['user_image'] = image1

            query = " update registration SET username='%s',age='%s',gender='%s',education='%s',state='%s',income='%s',profession='%s',image='%s' WHERE lid='%s' " % (
                name, age, gender, educational_background1,state,income,profession, image1, lid)
            cursor.execute(query)
            conn.commit()

            query = " update login SET email='%s',password='%s' WHERE lid='%d' " % (email,password, lid)
            cursor.execute(query)
            conn.commit()





            #return HttpResponse("Uploaded..!")
            msg = "Your profile is updated...."
        else:
            q="select image from registration where lid='%d'"%(lid)
            cursor.execute(q)
            img=cursor.fetchone()
            image2=img[0]



            query = " update registration SET username='%s',age='%s',gender='%s',education='%s',state='%s',income='%s',profession='%s',image='%s' WHERE lid='%s' " % (
                name, age, gender, educational_background1,state,income,profession, image2, lid)
            cursor.execute(query)
            conn.commit()
            query = " update login SET email='%s',password='%s' WHERE lid='%d' " % (email,password, lid)
            cursor.execute(query)
            conn.commit()

            #return HttpResponse("Uploaded..!")
            msg = "Your profile is updated...."

        query = " select rid from registration where lid='%d'"%(lid)
        cursor.execute(query)
        rid=cursor.fetchone()
        #print("rid",rid)
        query = "delete from user_interest where rid='%d'"%(rid[0])
        cursor.execute(query)
        conn.commit()

        for k in interest:
            query2 = "insert into user_interest(interest,rid) VALUES ('%s','%d')" % (k, rid[0])
            cursor.execute(query2)
            conn.commit()





        return profile(request)
        # return render(request,'editprofile.html',{'msg':msg})
    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


def viewdata(request):
    try:

        query = "SELECT * FROM registration"
        cursor.execute(query)
        rows = cursor.fetchall()

        return render(request, 'view.html', {'data': rows})

    except Error as e:
        print(e)
    finally:
        cursor.close()
        conn.close()





def sentiment(tweet, pos, neg, neu, pos_cmt, neg_cmt, neu_cmt):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        #print('Positive: ' + tweet + '\n')
        pos = pos + 1
        pos_cmt.append(tweet)
        ##print(pos_cmt)
    elif analysis.sentiment.polarity < 0:
        #print('Negative: ' + tweet + '\n')
        neg = neg + 1
        neg_cmt.append(tweet)
        ##print(neg_cmt)
    elif analysis.sentiment.polarity == 0:
        #print('Neutral' + tweet + '\n')
        neu = neu + 1
        neu_cmt.append(tweet)
        ##print(neu_cmt)
    return pos, neg, neu, pos_cmt, neg_cmt, neg_cmt


def query_twitter(q, max_tweets):
    [pos, neg, neu] = [0, 0, 0]
    sent = ''
    result = 0
    pos_cmt = []
    neg_cmt = []
    neu_cmt = []
    for tweet in tweepy.Cursor(api.search, q=q).items(max_tweets):
        if (datetime.datetime.now() - tweet.created_at).days < 1:
            #sentiment(tweet.text)
            pos, neg, neu, pos_cmt, neg_cmt, neg_cmt = sentiment(tweet.text, pos, neg, neu, pos_cmt, neg_cmt, neu_cmt)

    return pos, neg, neu


def application_search(request, st):
    try:
        #print("request:", st)
        search_term = st
        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                       password='12345678'
                                       , auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        app_name = play_scraper.search(search_term, page=1)
        app_search = app_name[0]
        title = app_search['title']
        if (title is not None):

            request.session['title'] = title
            #print("title", title)
            query5 = "select * from app_details where title='%s'" % (title)
            #print(search_term)
            cursor.execute(query5)
            a = cursor.fetchall()
            #print("ac", a)

            if (a == []):
                url=app_search['url']
                developer=app_search['developer']
                rating=app_search['score']
                per_rating = float(rating) * 20
                per_rating = round(per_rating, 2)
                icon=app_search['icon']

                package=app_search['app_id']
                #print(package)
                headers = {
                    'X-Apptweak-Key': 'WQA0noCpMD7h2eXVCUEoM57Wubg',
                }

                params = (
                    ('country', 'gb'),
                    ('language', 'en'),
                    ('max-age', '86400'),
                )
                URL2="https://api.apptweak.com/android/applications/"+package+"/information.json"
                response = requests.get(URL2, headers=headers, params=params)


                json_data1  = json.loads(response.text)
                #pprint(json_data1)
                dict3_description=json_data1
                dict4=dict3_description['content']

                list2_description=dict4['genres']
                category=list2_description[0]
                #print("category",category)

                version_list=dict4['versions']
                version_list_dict={}
                version_list_dict=version_list[0]
                #print("version details")
                last_updated=version_list_dict['release_date']
                #print("last_update",last_updated)
                # release_notes=version_list_dict['release_notes']
                # #print("release_notes",release_notes)
                current_version=version_list_dict['version']
                #print("curret_versio",current_version)
                price=dict4['price']
                content_rating1='Not Available'
                no_of_download='Not Available'
                size='varies with device'


                description=dict4['description']
               # #print("description",description)
                strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
                string = description.lower().replace("<br />", " ")
                description = re.sub(strip_special_chars, "", description.lower())
                #print("description",description)
                #developer='not available'
                query = "insert into app_details(package,icon,rating,content_rating,description,current_version,developer,price,installs,title,download_link,updated,category,app_size,app_category,app_like,app_dislike,count) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d','%d')" % (
                        package, icon, per_rating, content_rating1, description, current_version, developer, price,
                        no_of_download,
                        title,
                        url, last_updated, category, size, '1', 0, 0,0)

                #print("query",query)
                cursor.execute(query)
                conn.commit()
                app_id = int(cursor.lastrowid)
                #print("app_id",app_id)

                list_description=dict4['screenshots']

                for j in list_description:
                    #print("Screenshots",j)
                    query1 = "insert into app_screenshots(screenshot,app_id) VALUES ('%s','%d')" % (j, app_id)
                    #print(query1)
                    cursor.execute(query1)
                    conn.commit()
                # #print("hello")
                # #print(search_term)
                # app_name = play_scraper.search(search_term, page=1)
                # app_search = app_name[0]
                # title=app_search['title']
                # package=app_search['app_id']
                # url=app_search['url']
                # developer=app_search['developer']
                # rating=app_search['score']
                # per_rating = float(rating) * 20
                # per_rating = round(per_rating, 2)
                # icon=app_search['icon']
                # url1="https://play.google.com/store/apps/details?id="+package+""
                # html = urlopen(url)
                # soup = BeautifulSoup(html, 'lxml')
                # type(soup)
                # a=soup.find_all('span')
                # count=0
                # for i in range(len(a)):
                #     count=count+1
                #     x=a[i].text.strip()
                #     if x==title:
                #         index=i
                #         category=a[int(index)+int(2)].text.strip()
                #         no_of_rating=a[int(index)+int(3)].text.strip()
                #
                # div=soup.find_all('span',class_='htlgb')
                # list1=[]
                # for j in div:
                #     list1.append(j.text.strip())
                # last_updated=list1[0]
                # size=list1[2]
                # no_of_download=list1[4]
                # current_version=list1[6]
                # description=soup.find_all('div',class_='DWPxHb')
                # list=[]
                # for i in description:
                #     list.append(i.text.strip())
                # description=list[0]
                # strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
                # string = description.lower().replace("<br />", " ")
                # description = re.sub(strip_special_chars, "", description.lower())
                # img=soup.find_all('img',class_='T75of TJlTvc')
                # img1=[]
                # im=[]
                # for i in img:
                #
                #     ss=i.get('data-srcset')
                #     img1.append(ss)
                # for j in img1:
                #     if(j is not None):
                #          ss1=j.split(" ",2)
                #          im.append(ss1[0])
                # count=count+1
                # img2=[]
                # for j in img:
                #     img2.append(j.get('src'))
                # im.append(img2[0])
                # im.append(img2[1])
                # content_rating1="0"
                # price="0"
                # query = "insert into app_details(package,icon,rating,content_rating,description,current_version,developer,price,installs,title,download_link,updated,category,app_size,app_category,app_like,app_dislike,count) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d','%d')" % (
                #     package, icon, per_rating, content_rating1, description, current_version, developer, price,
                #     no_of_download,
                #     title,
                #     url, last_updated, category, size, 'all', 0, 0,1)
                # #print("query",query)
                # cursor.execute(query)
                # conn.commit()
                # app_id = int(cursor.lastrowid)
                # #print("app_id",app_id)
                # request.session['app_id'] = app_id
                #
                # for i in im:
                #     #print(i)
                #     #print(app_id)
                #     screenshots1 = i
                #     query1 = "insert into app_screenshots(screenshot,app_id) VALUES ('%s','%d')" % (i, app_id)
                #     #print(query1)
                #     cursor.execute(query1)
                #     conn.commit()

                headers = {
                    'X-Apptweak-Key': 'WQA0noCpMD7h2eXVCUEoM57Wubg',
                }

                params = (
                    ('country', 'gb'),
                    ('language', 'en'),
                    ('max-age', '964000'),
                )

                URL2 = "https://api.apptweak.com/android/applications/" + package + "/reviews.json"
                response = requests.get(URL2, headers=headers, params=params)

                json_data1 = json.loads(response.text)
                req = json_data1['content']
                #print("comment", req)

                #print(req)

                [pos, neg, neu] = [0, 0, 0]
                pos_cmt = []
                neg_cmt = []
                neu_cmt = []
                sent = ''
                result = 0
                if(req !=[]):
                    #print(req)


                    for i in req:
                        comment = i['body']
                        strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
                        string = comment.lower().replace("<br />", " ")
                        st = re.sub(strip_special_chars, "", comment.lower())
                       # print("comm",st)
                        pos, neg, neu, pos_cmt, neg_cmt, neu_cmt = sentiment(st, pos, neg, neu, pos_cmt, neg_cmt, neu_cmt)
                        #print(pos, neg, neu)
                        #sent,result=sentiment_percent(pos,neg,neu)

                    #print(pos, neg, neu)
                    #print("pos_cmt_list", pos_cmt)
                    #print("neg_cmt_list", neg_cmt)
                    #print("neu_cmt_list", neu_cmt)
                    total = pos + neg + neu
                    pos_per =round ((pos / total) * 100)
                    neg_per =round ((neg / total) * 100)
                    neu_per = round((neu / total) * 100)
                    #print(pos_per, neg_per, neu_per)

                    URL1 = "https://data.42matters.com/api/v3.0/android/apps/topics.json?p=" + package + "&access_token=f179acc1234fe6a99bb429b1682595bbac44be22"
                    response = requests.get(URL1)
                    #print(response.text)
                    json_data = json.loads(response.text)
                    reviews = json_data
                    print("reviews",reviews)
                    if(reviews is not None):
                        number_topics = reviews['number_topics']
                        total_reviews = reviews['total_reviews']
                        number_ratings = reviews['number_ratings']
                        query3 = "insert into app_reviews_result(nooftopic,noofreviews,noofrating,app_id3) VALUES ('%d','%d','%d','%d')" % (
                            number_topics, total_reviews, number_ratings, app_id)
                        cursor.execute(query3)
                        conn.commit()
                        topic = reviews['topics']
                        rrid = int(cursor.lastrowid)

                        for i in topic:
                            index = i
                            topic_name = i['topic_name']
                            no_of_reviews = i['reviews']
                            positive = i['positive']
                            per_positive = float(positive) * 100
                            per_positive = round(per_positive, 2)
                            negative = i['negative']
                            per_negative = float(negative) * 100
                            per_negative = round(per_negative, 2)
                            average_rating_of_topic = i['average_rating']
                            per_average_rating_of_topic = float(average_rating_of_topic) * 20
                            per_average_rating_of_topic = round(per_average_rating_of_topic, 2)

                            query4 = "insert into reviews_topic(topic_name,noofreviews,poscomment,negcomment,avgrating,rrid1) VALUES ('%s','%s','%s','%s','%s','%s')" % (
                                topic_name, no_of_reviews, per_positive, per_negative, per_average_rating_of_topic, rrid)
                            cursor.execute(query4)
                            conn.commit()
                    else:
                        number_topics = 'Not Available'
                        total_reviews = 'Not Available'
                        number_ratings = 'Not Available'
                        query3 = "insert into app_reviews_result(nooftopic,noofreviews,noofrating,app_id3) VALUES ('%d','%d','%d','%d')" % (
                            number_topics, total_reviews, number_ratings, app_id)
                        cursor.execute(query3)
                        conn.commit()
                        rrid = int(cursor.lastrowid)
                        topic_name='Not Available'
                        no_of_reviews='Not Available'
                        per_positive='Not Available'
                        per_negative='Not Available'
                        per_average_rating_of_topic='Not Available'

                        query4 = "insert into reviews_topic(topic_name,noofreviews,poscomment,negcomment,avgrating,rrid1) VALUES ('%s','%s','%s','%s','%s','%s')" % (
                            topic_name, no_of_reviews, per_positive, per_negative, per_average_rating_of_topic, rrid)
                        cursor.execute(query4)
                        conn.commit()

                    que = "select * from app_details where title='%s'" % (title)
                    cursor.execute(que)
                    a = cursor.fetchone()
                    appid = a[0]
                    query6 = "select screenshot from  app_screenshots where app_id ='%d'" % (appid)
                    cursor.execute(query6)
                    ss = cursor.fetchall()
                    x = len(ss)
                    list = []
                    for i in range(len(ss)):
                        if i <= 4:
                            list.append(ss[i])

                    query7 = "select * from app_reviews_result where app_id3='%d'" % (appid)
                    cursor.execute(query7)
                    review_result = cursor.fetchone()
                    r_rrid = review_result[0]
                    query8 = "select * from reviews_topic where rrid1='%d'" % (r_rrid)
                    cursor.execute(query8)
                    review_topic = cursor.fetchall()
                    #print(review_topic)

                    uid = request.session.get('lid')
                    if (uid):
                        ap_id = request.session.get('app_id')
                        ap_id = int(ap_id)

                        query9 = "select * from user_app where user_id='%d' and app_id='%d'" % (uid, ap_id)
                        cursor.execute(query9)
                        w = cursor.fetchall()
                        #print('ww', w)
                        query10 = "select status from user_app_like_dislike_status where  user_id='%d' and app_id='%d'" % (
                        uid, ap_id)
                        cursor.execute(query10)
                        j1 = cursor.fetchall()
                        if (j1 == []):
                            if (w == [] and j1 == []):
                                in_profile_status = "Add to Profile"
                                user_like_dislike = "Like"
                                return render(request, 'new_result.html',
                                              {'detail': a, 'screenshot': list, 'app_review_result': review_result,
                                               'reviews_topic': review_topic, 'in_profile_status': in_profile_status,
                                               'user_like_dislike': user_like_dislike, 'pos_per': pos_per,
                                               'neg_per': neg_per, 'neu_per': neu_per})

                            if (w != [] and j1 == []):
                                in_profile_status = "Remove From Profile"
                                user_like_dislike = "Like"
                                return render(request, 'new_result.html',
                                              {'detail': a, 'screenshot': list, 'app_review_result': review_result,
                                               'reviews_topic': review_topic, 'in_profile_status': in_profile_status,
                                               'user_like_dislike': user_like_dislike, 'pos_per': pos_per,
                                               'neg_per': neg_per, 'neu_per': neu_per})
                        else:
                            j = j1[0]
                            k = j[0]
                            #print("j1", k)
                            if (w != [] and k == 'Like'):
                                in_profile_status = "Remove From Profile"
                                user_like_dislike = "dislike"
                                return render(request, 'new_result.html',
                                              {'detail': a, 'screenshot': list, 'app_review_result': review_result,
                                               'reviews_topic': review_topic, 'in_profile_status': in_profile_status,
                                               'user_like_dislike': user_like_dislike, 'pos_per': pos_per,
                                               'neg_per': neg_per, 'neu_per': neu_per})
                            if (w == [] and k == 'Like'):
                                in_profile_status = "Add to Profile"
                                user_like_dislike = "dislike"
                                return render(request, 'new_result.html',
                                              {'detail': a, 'screenshot': list, 'app_review_result': review_result,
                                               'reviews_topic': review_topic, 'in_profile_status': in_profile_status,
                                               'user_like_dislike': user_like_dislike, 'pos_per': pos_per,
                                               'neg_per': neg_per, 'neu_per': neu_per})
                    else:
                        return render(request, 'unauth_result.html', {'detail': a, 'screenshot': list,'app_review_result': review_result})



                else:

                    pos, neg, neu = query_twitter(st, 100)
                    if(pos != "" or neg != "" or neu != ""  ):
                        total = pos + neg + neu
                        pos_per = round((pos / total) * 100)
                        neg_per =round ((neg / total) * 100)
                        neu_per = round((neu / total) * 100)
                        #print("per", pos_per, neg_per, neu_per)
                    else:
                        pos_per ="Not Available"
                        neg_per ="Not Available"
                        neu_per = "Not Available"

                    URL1 = "https://data.42matters.com/api/v3.0/android/apps/topics.json?p=" + package + "&access_token=f179acc1234fe6a99bb429b1682595bbac44be22"
                    response = requests.get(URL1)
                    #print(response.text)
                    json_data = json.loads(response.text)
                    reviews = json_data
                    if(reviews is not None):
                        number_topics = reviews['number_topics']
                        total_reviews = reviews['total_reviews']
                        number_ratings = reviews['number_ratings']
                        query3 = "insert into app_reviews_result(nooftopic,noofreviews,noofrating,app_id3) VALUES ('%d','%d','%d','%d')" % (
                            number_topics, total_reviews, number_ratings, app_id)
                        cursor.execute(query3)
                        conn.commit()
                        topic = reviews['topics']
                        rrid = int(cursor.lastrowid)

                        for i in topic:
                            index = i
                            topic_name = i['topic_name']
                            no_of_reviews = i['reviews']
                            positive = i['positive']
                            per_positive = float(positive) * 100
                            per_positive = round(per_positive, 2)
                            negative = i['negative']
                            per_negative = float(negative) * 100
                            per_negative = round(per_negative, 2)
                            average_rating_of_topic = i['average_rating']
                            per_average_rating_of_topic = float(average_rating_of_topic) * 20
                            per_average_rating_of_topic = round(per_average_rating_of_topic, 2)

                            query4 = "insert into reviews_topic(topic_name,noofreviews,poscomment,negcomment,avgrating,rrid1) VALUES ('%s','%s','%s','%s','%s','%s')" % (
                                topic_name, no_of_reviews, per_positive, per_negative, per_average_rating_of_topic, rrid)
                            cursor.execute(query4)
                            conn.commit()
                    else:
                        number_topics = 'Not Available'
                        total_reviews = 'Not Available'
                        number_ratings = 'Not Available'
                        query3 = "insert into app_reviews_result(nooftopic,noofreviews,noofrating,app_id3) VALUES ('%d','%d','%d','%d')" % (
                            number_topics, total_reviews, number_ratings, app_id)
                        cursor.execute(query3)
                        conn.commit()
                        rrid = int(cursor.lastrowid)
                        topic_name='Not Available'
                        no_of_reviews='Not Available'
                        per_positive='Not Available'
                        per_negative='Not Available'
                        per_average_rating_of_topic='Not Available'

                        query4 = "insert into reviews_topic(topic_name,noofreviews,poscomment,negcomment,avgrating,rrid1) VALUES ('%s','%s','%s','%s','%s','%s')" % (
                            topic_name, no_of_reviews, per_positive, per_negative, per_average_rating_of_topic, rrid)
                        cursor.execute(query4)
                        conn.commit()

                    que = "select * from app_details where title='%s'" % (title)
                    cursor.execute(que)
                    a = cursor.fetchone()
                    appid = a[0]
                    query6 = "select screenshot from  app_screenshots where app_id ='%d'" % (appid)
                    cursor.execute(query6)
                    ss = cursor.fetchall()
                    x = len(ss)
                    list = []
                    for i in range(len(ss)):
                        if i <= 4:
                            list.append(ss[i])

                    query7 = "select * from app_reviews_result where app_id3='%d'" % (appid)
                    cursor.execute(query7)
                    review_result = cursor.fetchone()
                    r_rrid = review_result[0]
                    query8 = "select * from reviews_topic where rrid1='%d'" % (r_rrid)
                    cursor.execute(query8)
                    review_topic = cursor.fetchall()
                    #print(review_topic)

                    uid = request.session.get('lid')
                    if (uid):
                        ap_id = request.session.get('app_id')
                        ap_id = int(ap_id)

                        query9 = "select * from user_app where user_id='%d' and app_id='%d'" % (uid, ap_id)
                        cursor.execute(query9)
                        w = cursor.fetchall()
                        #print('ww', w)
                        query10 = "select status from user_app_like_dislike_status where  user_id='%d' and app_id='%d'" % (
                        uid, ap_id)
                        cursor.execute(query10)
                        j1 = cursor.fetchall()
                        if (j1 == []):
                            if (w == [] and j1 == []):
                                in_profile_status = "Add to Profile"
                                user_like_dislike = "Like"
                                return render(request, 'new_result.html',
                                              {'detail': a, 'screenshot': list, 'app_review_result': review_result,
                                               'reviews_topic': review_topic, 'in_profile_status': in_profile_status,
                                               'user_like_dislike': user_like_dislike, 'pos_per': pos_per,
                                               'neg_per': neg_per, 'neu_per': neu_per})

                            if (w != [] and j1 == []):
                                in_profile_status = "Remove From Profile"
                                user_like_dislike = "Like"
                                return render(request, 'new_result.html',
                                              {'detail': a, 'screenshot': list, 'app_review_result': review_result,
                                               'reviews_topic': review_topic, 'in_profile_status': in_profile_status,
                                               'user_like_dislike': user_like_dislike, 'pos_per': pos_per,
                                               'neg_per': neg_per, 'neu_per': neu_per})
                        else:
                            j = j1[0]
                            k = j[0]
                            #print("j1", k)
                            if (w != [] and k == 'Like'):
                                in_profile_status = "Remove From Profile"
                                user_like_dislike = "dislike"
                                return render(request, 'new_result.html',
                                              {'detail': a, 'screenshot': list, 'app_review_result': review_result,
                                               'reviews_topic': review_topic, 'in_profile_status': in_profile_status,
                                               'user_like_dislike': user_like_dislike, 'pos_per': pos_per,
                                               'neg_per': neg_per, 'neu_per': neu_per})
                            if (w == [] and k == 'Like'):
                                in_profile_status = "Add to Profile"
                                user_like_dislike = "dislike"
                                return render(request, 'new_result.html',
                                              {'detail': a, 'screenshot': list, 'app_review_result': review_result,
                                               'reviews_topic': review_topic, 'in_profile_status': in_profile_status,
                                               'user_like_dislike': user_like_dislike, 'pos_per': pos_per,
                                               'neg_per': neg_per, 'neu_per': neu_per})
                    else:
                        return render(request, 'unauth_result.html', {'detail': a, 'screenshot': list,'app_review_result': review_result})






            else:


                #print("yes")
                #print("A", a)
                b = a[0]
                #print("whatsapp", b)
                appid = b[0]
                request.session['app_id'] = appid
                print("sgvds",appid)
                package = b[1]
                app_count=int(b[18])
                app_count=app_count+1
                #print(app_count)
                q="update app_details SET count='%d' WHERE app_id='%d' " % (app_count,appid)
                cursor.execute(q)
                conn.commit()



                query6 = "select screenshot from  app_screenshots where app_id ='%d'" % (appid)
                cursor.execute(query6)
                ss = cursor.fetchall()
                x = len(ss)
                list = []
                for i in range(len(ss)):
                    if i <= 4:
                        list.append(ss[i])
                #print(ss)

                query7 = "select * from app_reviews_result where app_id3='%d'" % (appid)
                cursor.execute(query7)
                review_result = cursor.fetchone()
                print("sads",review_result)
                r_rrid = review_result[0]
                print("rrid",r_rrid)
                query8 = "select * from reviews_topic where rrid1='%d'" % (r_rrid)
                cursor.execute(query8)
                review_topic = cursor.fetchall()
                #print(review_topic)
                uid = request.session.get('lid')
                #print("uid", uid)

                if (uid):

                    # headers = {
                    #     'X-Apptweak-Key': 'WQA0noCpMD7h2eXVCUEoM57Wubg',
                    # }
                    #
                    # params = (
                    #     ('country', 'gb'),
                    #     ('language', 'en'),
                    #     ('max-age', '964000'),
                    # )
                    #
                    # URL2 = "https://api.apptweak.com/android/applications/" + package + "/reviews.json"
                    # response = requests.get(URL2, headers=headers, params=params)
                    #
                    # json_data1 = json.loads(response.text)
                    # req = json_data1['content']
                    # #print("comment", req)
                    #
                    # [pos, neg, neu] = [0, 0, 0]
                    # pos_cmt = []
                    # neg_cmt = []
                    # neu_cmt = []
                    # sent = ''
                    # result = 0
                    # pos_per=''
                    # neg_per=''
                    # neu_per=''
                    # if(req != []):
                    #
                    #     #print(req)
                    #
                    #     for i in req:
                    #         comment = i['body']
                    #         strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
                    #         string = comment.lower().replace("<br />", " ")
                    #         st = re.sub(strip_special_chars, "", comment.lower())
                    #         print(st)
                    #         pos, neg, neu, pos_cmt, neg_cmt, neu_cmt = sentiment(st, pos, neg, neu, pos_cmt, neg_cmt,
                    #                                                              neu_cmt)
                    #         #print(pos, neg, neu)
                    #         # sent,result=sentiment_percent(pos,neg,neu)
                    #
                    #     #print(pos, neg, neu)
                    #     #print("pos_cmt_list", pos_cmt)
                    #     #print("neg_cmt_list", neg_cmt)
                    #     #print("neu_cmt_list", neu_cmt)
                    #     total = pos + neg + neu
                    #     pos_per = round((pos / total) * 100)
                    #     neg_per =round ((neg / total) * 100)
                    #     neu_per =round ((neu / total) * 100)
                    #     #print(pos_per, neg_per, neu_per)
                    # else:
                    pos, neg, neu = query_twitter(st, 100)
                    if(pos != "" or neg != "" or neu != ""  ):
                        total = pos + neg + neu
                        pos_per = round((pos / total) * 100)
                        neg_per =round ((neg / total) * 100)
                        neu_per = round((neu / total) * 100)
                        #print("per", pos_per, neg_per, neu_per)
                    else:
                        pos_per ="Not Available"
                        neg_per ="Not Available"
                        neu_per ="Not Available"


                    #print(appid)

                    app_id = int(request.session.get('app_id'))
                    #print("app_id", app_id)
                    q = "select * from user_app where user_id='%d' and app_id='%d'" % (uid, app_id)
                    #print(q)
                    cursor.execute(q)
                    w = cursor.fetchall()
                    #print('ww', w)
                    query10 = "select status from user_app_like_dislike_status where  user_id='%d' and app_id='%d'" % (
                    uid, app_id)
                    cursor.execute(query10)
                    j1 = cursor.fetchall()
                    #print("j1", j1)

                    if (j1 == []):
                        if (w == [] and j1 == []):
                            in_profile_status = "Add to Profile"
                            user_like_dislike = "Like"
                            return render(request, 'new_result.html',
                                          {'detail': b, 'screenshot': list, 'app_review_result': review_result,
                                           'reviews_topic': review_topic, 'in_profile_status': in_profile_status,
                                           'user_like_dislike': user_like_dislike, 'pos_per': pos_per,
                                           'neg_per': neg_per, 'neu_per': neu_per})

                        if (w != [] and j1 == []):
                            in_profile_status = "Remove From Profile"
                            user_like_dislike = "Like"
                            return render(request, 'new_result.html',
                                          {'detail': b, 'screenshot': list, 'app_review_result': review_result,
                                           'reviews_topic': review_topic, 'in_profile_status': in_profile_status,
                                           'user_like_dislike': user_like_dislike, 'pos_per': pos_per,
                                           'neg_per': neg_per, 'neu_per': neu_per})
                    else:
                        j = j1[0]
                        k1 = j[0]
                        #print("j1 else", k1)
                        #print("w", w)
                        if (w != [] and k1 == 'Like'):
                            in_profile_status = "Remove From Profile"
                            user_like_dislike = "dislike"
                            return render(request, 'new_result.html',
                                          {'detail': b, 'screenshot': list, 'app_review_result': review_result,
                                           'reviews_topic': review_topic, 'in_profile_status': in_profile_status,
                                           'user_like_dislike': user_like_dislike, 'pos_per': pos_per,
                                           'neg_per': neg_per, 'neu_per': neu_per})
                        if (w == [] and k1 == 'Like'):
                            in_profile_status = "Add to Profile"
                            user_like_dislike = "dislike"
                            return render(request, 'new_result.html',
                                          {'detail': b, 'screenshot': list, 'app_review_result': review_result,
                                           'reviews_topic': review_topic, 'in_profile_status': in_profile_status,
                                           'user_like_dislike': user_like_dislike, 'pos_per': pos_per,
                                           'neg_per': neg_per, 'neu_per': neu_per})



                else:
                    return render(request, 'unauth_result.html', {'detail': b, 'screenshot': list,'app_review_result': review_result})

        else:
            return render(request, '404.html')
    except Error as e:
        print(e)


def website_search(request, st):
    site = st
    #site = request.GET.get('search_term')

    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678'
                                   , auth_plugin='mysql_native_password')
    cursor = conn.cursor()
    if (site == ''):
        msg = "Please Enter Your Search Term"
        return render(request, 'index.html', {'msg': msg})
    else:
        link = "https://"
        visit_site = "".join((link, site))

        query7 = "select * FROM web where title='%s'" % (site)
        cursor.execute(query7)
        a = cursor.fetchall()
        conn.commit()


        if (a == []):


            #print(site)
            request.session['site_name'] = site
            new_word = site.split('.', 2)
            new_word1 = new_word[0]
            new_word2 = "&nbsp"
            new_string = "".join((new_word2, new_word1))
            # #print(new_word[0])

            url = "https://www.alexa.com/siteinfo/" + site + "#?sites=" + site + ""
            html = urlopen(url)

            soup = BeautifulSoup(html, 'lxml')
            type(soup)

            # gloal_rank and country rank
            global_rank = 0
            country_rank = 0
            bounce_rate = 0
            daily_time_on_site = 0
            daily_pageview_per_visitor = 0
            total_site_linking_in = 0
            rank_in_country_name = 0
            loading_time = 0
            description = 0
            rank_image = 0
            country1 = 0
            country2 = 0
            country3 = 0
            country4 = 0
            country4 = 0
            country5 = 0
            percent_of_visitor1 = 0
            percent_of_visitor2 = 0
            percent_of_visitor3 = 0
            percent_of_visitor4 = 0
            percent_of_visitor5 = 0
            rank_in_country1 = 0
            rank_in_country2 = 0
            rank_in_country3 = 0
            rank_in_country4 = 0
            rank_in_country5 = 0
            rank_in_country = 0

            # gloal_rank and country rank
            all_strong = soup.find_all("strong")
            list_of_strong = []
            for h in all_strong:
                list_of_strong.append(h.text.strip())
            global_rank = list_of_strong[6]
            country_rank = list_of_strong[9]
            for i in range(len(list_of_strong)):

                if list_of_strong[i] == 'Daily Time on Site':
                    index = i

                    bounce_rate = list_of_strong[int(index) + int(1)]
                    daily_pageview_per_visitor = list_of_strong[int(index) + int(2)]
                    daily_time_on_site = list_of_strong[int(index) + int(3)]

                if list_of_strong[i] == 'Alexa Pro Basic Plan':
                    index1 = i
                    total_site_linking_in = list_of_strong[int(index1) + int(1)]

            # Country_name
            anchor_tags = soup.find_all("a")
            for j in range(len(anchor_tags)):
                a = anchor_tags[j].text.strip()

                if a == 'Certified Site Metrics FAQs':
                    index = j
                    rank_in_country_name = anchor_tags[int(index) + int(1)].text.strip()

            # loading_time And Description

            para = soup.find_all("p")
            for k in range(len(para)):
                a = para[k].text.strip()
                if a == 'The load time metric is updated monthly.':
                    index = k
                    loading_time = para[int(index) + int(1)].text.strip()
                    description1 = para[int(index) + int(4)].text.strip()

                    strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
                    string = description1.lower().replace("<br />", " ")
                    description = re.sub(strip_special_chars, "", description1.lower())
            # image of traffic rank

            img_list = []
            all_links = soup.find_all("img")
            count = 0
            for link in all_links:
                # #print(count)
                img_list.append(link.get("src"))
                count = count + 1
            rank_image = img_list[5]

            query = "insert into web(global_rank,country_rank,bounce_rate,daily_time_on_site,daily_page_view_per_visitor,rank_image,total_site_linking_in,loading_time,description,country_name,title,category,web_like,web_dislike,count) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d','%d')" % (
                global_rank, country_rank, bounce_rate, daily_time_on_site, daily_pageview_per_visitor, rank_image,
                total_site_linking_in, loading_time, description, rank_in_country_name, site, 'all', 0, 0,1)
            #print(query)
            cursor.execute(query)
            conn.commit()

            web_id = int(cursor.lastrowid)

            # Audiace Geography

            list = []
            td_tags = soup.find_all("td")
            for t in td_tags:
                list.append(t.text.strip())
                count = count + 1

            for l in range(len(list)):

                if list[
                    l] == "Loyalty Metrics\n\n\n\nSee how much a country's visitors remain engaged over time. Based on Monthly\nUnique Visitor, Visit, and Pageview estimates in each country where those metrics are available.\n\n \nBased on unique visitor estimates\n\n\nVisits per Visitor\n\nAdvanced Plan Only\n\n\nPageviews per Visit\n\nAdvanced Plan Only\n\n\nMonthly Pageviews per Visitor\n\nAdvanced Plan Only":

                    index = l
                    # #print(index)
                    try:
                        country1 = list[int(index) + int(1)]
                        percent_of_visitor1 = list[int(index) + int(2)]
                        rank_in_country1 = list[int(index) + int(3)]
                        # #print(country1,percent_of_visitor1,rank_in_country1)


                    except Error as e:
                        continue
                    try:
                        country2 = list[int(index) + int(4)]
                        percent_of_visitor2 = list[int(index) + int(5)]
                        rank_in_country2 = list[int(index) + int(6)]
                        # #print(country2,percent_of_visitor2,rank_in_country2)
                    except Error as e:
                        continue
                    try:
                        country3 = list[int(index) + int(7)]
                        percent_of_visitor3 = list[int(index) + int(8)]
                        rank_in_country3 = list[int(index) + int(9)]

                    except Error as e:
                        continue

                    try:
                        country4 = list[int(index) + int(10)]
                        percent_of_visitor4 = list[int(index) + int(11)]
                        rank_in_country4 = list[int(index) + int(12)]
                        # #print (country4)
                    except Error as e:
                        continue
                    try:
                        country5 = list[int(index) + int(13)]
                        percent_of_visitor5 = list[int(index) + int(14)]
                        rank_in_country5 = list[int(index) + int(15)]
                        # #print(country5,percent_of_visitor5,rank_in_country5)
                    except Error as e:
                        continue
            # #print (country1,country2,country3,country4,country5)

            # if country1 is null then
            if country1 == 0:
                query1 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                    list[0], list[1], list[2], web_id)
                cursor.execute(query1)
                conn.commit()

            elif country3 == "1. &nbsp" + new_word1 + "":
                xyz = country3.split('\xa0', 2)
                p = xyz[1]
                # #print (xyz)
                if p == new_string:
                    query1 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country1, percent_of_visitor1, rank_in_country1, web_id)
                    cursor.execute(query1)
                    conn.commit()
                    query2 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country2, percent_of_visitor2, rank_in_country2, web_id)
                    cursor.execute(query2)
                    conn.commit()




            # if country 4 is nbsp then
            elif country4 == "1. &nbsp" + new_word1 + "":
                xyz = country4.split('\xa0', 2)
                p = xyz[1]
                # #print (xyz)
                if p == new_string:
                    query1 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country1, percent_of_visitor1, rank_in_country1, web_id)
                    cursor.execute(query1)
                    conn.commit()
                    query2 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country2, percent_of_visitor2, rank_in_country2, web_id)
                    cursor.execute(query2)
                    conn.commit()

                    query3 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country3, percent_of_visitor3, rank_in_country3, web_id)
                    cursor.execute(query3)
                    conn.commit()

            # if country5 is nbsp then
            elif country5 == "1. &nbsp" + new_word1 + "":
                xyz = country5.split('\xa0', 2)
                p = xyz[1]
                # #print (xyz)
                if p == new_string:
                    query1 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country1, percent_of_visitor1, rank_in_country1, web_id)
                    cursor.execute(query1)
                    conn.commit()
                    query2 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country2, percent_of_visitor2, rank_in_country2, web_id)
                    cursor.execute(query2)
                    conn.commit()

                    query3 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country3, percent_of_visitor3, rank_in_country3, web_id)
                    cursor.execute(query3)
                    conn.commit()
                    query4 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country4, percent_of_visitor4, rank_in_country4, web_id)
                    cursor.execute(query4)
                    conn.commit()

            else:
                query1 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                    country1, percent_of_visitor1, rank_in_country1, web_id)
                cursor.execute(query1)
                conn.commit()
                query2 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                    country2, percent_of_visitor2, rank_in_country2, web_id)
                cursor.execute(query2)
                conn.commit()

                query3 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                    country3, percent_of_visitor3, rank_in_country3, web_id)
                cursor.execute(query3)
                conn.commit()
                query4 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                    country4, percent_of_visitor4, rank_in_country4, web_id)
                cursor.execute(query4)
                conn.commit()
                query5 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                    country5, percent_of_visitor5, rank_in_country5, web_id)
                cursor.execute(query5)
                conn.commit()

            #print(web_id)
            query6 = "select * FROM web where title='%s'" % (site)
            cursor.execute(query6)

            a = cursor.fetchall()
            #print("value of a", a)
            conn.commit()
            c = a[0]
            d = c[0]
            request.session['web_id'] = d
            query7 = "select * FROM web_table where web_id='%d'" % (d)
            cursor.execute(query7)
            b = cursor.fetchall()
            #print("value of b", b)
            conn.commit()
            # pos_per =0
            # neg_per=0
            # neu_per =0
            #


            extension = site.split('.')
            # #print(extension)
            name=extension[0]
            #print(name)
            pos, neg, neu = query_twitter(name, 100)
            if(pos != "" or neg != "" or neu != ""  ):
                total = pos + neg + neu
                pos_per = round((pos / total) * 100)
                neg_per =round ((neg / total) * 100)
                neu_per = round((neu / total) * 100)
                #print("per", pos_per, neg_per, neu_per)
            else:
                pos_per ="Not Available"
                neg_per ="Not Available"
                neu_per ="Not Available"

            uid = request.session.get('lid')
            #print("uid", uid)

            if (uid):
                web_id = int(request.session.get('web_id'))
                #print("app_id", web_id)
                q = "select * from user_website where user_id='%d' and web_id='%d'" % (uid, web_id)
                #print(q)
                cursor.execute(q)
                w = cursor.fetchall()
                #print('ww', w)
                query10 = "select status from user_website_like_dislike_status where  user_id='%d' and web_id='%d'" % (
                    uid, web_id)
                cursor.execute(query10)
                j1 = cursor.fetchall()
                #print("j1", j1)

                if (j1 == []):
                    if (w == [] and j1 == []):
                        in_profile_status = "Add to Profile"
                        user_like_dislike = "Like"
                        return render(request, 'website.html', {'msg': c, 'b': b, "visit_site": visit_site,
                                                                'in_profile_status': in_profile_status,
                                                                'user_like_dislike': user_like_dislike,
                                                                'pos_per': pos_per, 'neg_per': neg_per,
                                                                'neu_per': neu_per})

                    if (w != [] and j1 == []):
                        in_profile_status = "Remove From Profile"
                        user_like_dislike = "Like"

                        return render(request, 'website.html', {'msg': c, 'b': b, "visit_site": visit_site,
                                                                'in_profile_status': in_profile_status,
                                                                'user_like_dislike': user_like_dislike,
                                                                'pos_per': pos_per, 'neg_per': neg_per,
                                                                'neu_per': neu_per})


                else:
                    j = j1[0]
                    k1 = j[0]
                    #print("j1 else", k1)
                    #print("w", w)
                    if (w != [] and k1 == 'Like'):
                        in_profile_status = "Remove From Profile"
                        user_like_dislike = "dislike"
                        return render(request, 'website.html', {'msg': c, 'b': b, "visit_site": visit_site,
                                                                'in_profile_status': in_profile_status,
                                                                'user_like_dislike': user_like_dislike,
                                                                'pos_per': pos_per, 'neg_per': neg_per,
                                                                'neu_per': neu_per})

                    if (w == [] and k1 == 'Like'):
                        in_profile_status = "Add to Profile"
                        user_like_dislike = "dislike"
                        return render(request, 'website.html', {'msg': c, 'b': b, "visit_site": visit_site,
                                                                'in_profile_status': in_profile_status,
                                                                'user_like_dislike': user_like_dislike,
                                                                'pos_per': pos_per, 'neg_per': neg_per,
                                                                'neu_per': neu_per})
            else:
                return render(request, 'website_unauth.html', {'msg': c, 'b': b, "visit_site": visit_site})





        else:
            query6 = "select * FROM web where title='%s'" % (site)
            cursor.execute(query6)

            a1 = cursor.fetchall()
            a = a1[0]
            request.session['site_name'] = site
            #print(a)
            conn.commit()

            d = a[0]
            web_count=int(a[15])
            web_count=web_count+1
            request.session['web_id'] = d
            q="update web SET count='%d' WHERE web_id='%d' " % (web_count,d)
            cursor.execute(q)
            conn.commit()
            query7 = "select * FROM web_table where web_id='%d'" % (d)
            cursor.execute(query7)
            b1 = cursor.fetchall()
            conn.commit()
            b = b1[0]
            for i in b1:
                print(i[1])

            extension = site.split('.')
            # #print(extension)
            name=extension[0]

            pos, neg, neu = query_twitter(name, 100)
            if(pos != "" or neg != "" or neu != ""  ):
                total = pos + neg + neu
                pos_per = round((pos / total) * 100)
                neg_per =round ((neg / total) * 100)
                neu_per = round((neu / total) * 100)
                #print("per", pos_per, neg_per, neu_per)
            else:
                pos_per ="Not Available"
                neg_per ="Not Available"
                neu_per ="Not Available"
            #print(pos_per)
            uid = request.session.get('lid')
            #print("uid", uid)

            if (uid):
                web_id = int(request.session.get('web_id'))
                #print("app_id", web_id)
                q = "select * from user_website where user_id='%d' and web_id='%d'" % (uid, web_id)
                #print(q)
                cursor.execute(q)
                w = cursor.fetchall()
                #print('ww', w)
                query10 = "select status from user_website_like_dislike_status where  user_id='%d' and web_id='%d'" % (
                    uid, web_id)
                cursor.execute(query10)
                j1 = cursor.fetchall()
                #print("j1", j1)

                if (j1 == []):
                    if (w == [] and j1 == []):
                        in_profile_status = "Add to Profile"
                        user_like_dislike = "Like"
                        return render(request, 'website.html', {'msg': a, 'b': b1, 'visit_site': visit_site,
                                                                'in_profile_status': in_profile_status,
                                                                'user_like_dislike': user_like_dislike,
                                                                'pos_per': pos_per, 'neg_per': neg_per,
                                                                'neu_per': neu_per})

                    if (w != [] and j1 == []):
                        in_profile_status = "Remove From Profile"
                        user_like_dislike = "Like"

                        return render(request, 'website.html', {'msg': a, 'b': b1, 'visit_site': visit_site,
                                                                'in_profile_status': in_profile_status,
                                                                'user_like_dislike': user_like_dislike,
                                                                'pos_per': pos_per, 'neg_per': neg_per,
                                                                'neu_per': neu_per})


                else:
                    j = j1[0]
                    k1 = j[0]
                    #print("j1 else", k1)
                    #print("w", w)
                    if (w != [] and k1 == 'Like'):
                        in_profile_status = "Remove From Profile"
                        user_like_dislike = "dislike"
                        return render(request, 'website.html', {'msg': a, 'b': b1, 'visit_site': visit_site,
                                                                'in_profile_status': in_profile_status,
                                                                'user_like_dislike': user_like_dislike,
                                                                'pos_per': pos_per, 'neg_per': neg_per,
                                                                'neu_per': neu_per})

                    if (w == [] and k1 == 'Like'):
                        in_profile_status = "Add to Profile"
                        user_like_dislike = "dislike"
                        return render(request, 'website.html', {'msg': a, 'b': b1, 'visit_site': visit_site,
                                                                'in_profile_status': in_profile_status,
                                                                'user_like_dislike': user_like_dislike,
                                                                'pos_per': pos_per, 'neg_per': neg_per,
                                                                'neu_per': neu_per})
            else:
                return render(request, 'website_unauth.html', {'msg': a, 'b': b1, 'visit_site': visit_site})
def software_search_like(request, st):
    title = 0
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678'
                                   , auth_plugin='mysql_native_password')
    cursor = conn.cursor()

    software = st

    if (software == ''):
        msg = "Please Enter Your Search Tearm"
        return render(request, 'index.html', {'msg': msg})
    else:
        query7 = "select * FROM new_software where title like '%%%s%%'" % (software)
        cursor.execute(query7)
        a = cursor.fetchall()
        #print("value", a)
        if(a == []):
            soft_msg="Software not available"
            return render(request,'software_like_query.html',{'soft_msg':soft_msg})

        else:
            return render(request,'software_like_query.html',{'soft':a})

def software_search(request, st):
    title = 0
    print("st",st)
    request.session['soft_name'] = st
    #request.session[''] = st
    a = request.session.get('soft_name')
    print("a",a)
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678'
                                   , auth_plugin='mysql_native_password')
    cursor = conn.cursor()

    software = st
    print("soft name",st)


    query66 = "select * FROM new_software where title='%s'" % (st)
    #print(query66)
    cursor.execute(query66)
    v = cursor.fetchall()
    #print("its", v)
    b = v[0]
    #print("a", b)
    conn.commit()
    soft_count =int(b[21])
    soft_count = soft_count + 1
    query2 = "update new_software SET count='%d' WHERE new_software_id='%d' " % (soft_count, b[0])
    cursor.execute(query2)
    conn.commit()
    request.session['soft_id'] = b[0]
    #request.session['soft_name'] = b[13]
    #print("soft_id",b[0])

    pos, neg, neu = query_twitter(software, 100)
    #print("per", pos, neg, neu)
    if(pos != 0 or neg != 0  or neu != 0  ):
        total = pos + neg + neu
        pos_per = round((pos / total) * 100)
        neg_per = round((neg / total) * 100)
        neu_per = round((neu / total) * 100)
        #print("per", pos_per, neg_per, neu_per)

    else:
        pos_per ="Not Available"
        neg_per ="Not Available"
        neu_per ="Not Available"
    #print("per", pos_per, neg_per, neu_per)
    uid = request.session.get('lid')
    #print("uid", uid)
    soft_id = int(request.session.get('soft_id'))
    if (uid):
        soft_id = int(request.session.get('soft_id'))
        #print("soft_id", soft_id)
        q = "select * from user_software where user_id='%d' and soft_id='%d'" % (uid, soft_id)
        #print(q)
        cursor.execute(q)
        w = cursor.fetchall()
        #print('ww', w)
        query10 = "select status from user_software_like_dislike_status where  user_id='%d' and soft_id='%d'" % (
            uid, soft_id)
        cursor.execute(query10)
        j1 = cursor.fetchall()
        #print("j1", j1)

        if (j1 == []):
            if (w == [] and j1 == []):
                in_profile_status = "Add to Profile"
                user_like_dislike = "Like"
                return render(request, 'result_download.com_software.html',
                              {'software': b, 'in_profile_status': in_profile_status,
                               'user_like_dislike': user_like_dislike, 'pos_per': pos_per, 'neg_per': neg_per,
                               'neu_per': neu_per})

            if (w != [] and j1 == []):
                in_profile_status = "Remove From Profile"
                user_like_dislike = "Like"

                return render(request, 'result_download.com_software.html',
                              {'software': b, 'in_profile_status': in_profile_status,
                               'user_like_dislike': user_like_dislike, 'pos_per': pos_per, 'neg_per': neg_per,
                               'neu_per': neu_per})


        else:
            j = j1[0]
            k1 = j[0]
            #print("j1 else", k1)
            #print("w", w)
            if (w != [] and k1 == 'Like'):
                in_profile_status = "Remove From Profile"
                user_like_dislike = "dislike"
                return render(request, 'result_download.com_software.html',
                              {'software': b, 'in_profile_status': in_profile_status,
                               'user_like_dislike': user_like_dislike, 'pos_per': pos_per, 'neg_per': neg_per,
                               'neu_per': neu_per})

            if (w == [] and k1 == 'Like'):
                in_profile_status = "Add to Profile"
                user_like_dislike = "dislike"
                return render(request, 'result_download.com_software.html',
                              {'software': b, 'in_profile_status': in_profile_status,
                               'user_like_dislike': user_like_dislike, 'pos_per': pos_per, 'neg_per': neg_per,
                               'neu_per': neu_per})

    else:
        return render(request, 'result_download.com_software_unauth.html', {'software': b})

# def retry_application_search(request,st):
#         #print("request:", st)
#         search_term = st
#         conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
#                                        password='12345678'
#                                        , auth_plugin='mysql_native_password')
#         cursor = conn.cursor()
#
#
#         #print("title",search_term)
#         query7 = "select * FROM app_details where title like '%%%s%%'" % (search_term)
#
#         cursor.execute(query7)
#         a = cursor.fetchall()
#         #print("ac", a)
#         if(a != []):
#
#             return render(request,'show.html',{'msg':a})
#         else:
#             app_name = play_scraper.search(search_term, page=1)
#             app_search = app_name[0]
#             package = app_search['app_id']
#             app_details = play_scraper.details(package)
#             icon = app_details['icon']
#             rating = app_details['score']
#             per_rating = float(rating) * 20
#             per_rating = round(per_rating, 2)
#             content_rating = app_details['content_rating']
#             content_rating1 = content_rating[0]
#             str = app_details['description']
#             strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
#             string = str.lower().replace("<br />", " ")
#             description = re.sub(strip_special_chars, "", str.lower())
#             current_version = app_details['current_version']
#             developer = app_details['developer']
#             price = app_details['price']
#             installs = app_details['installs']
#             reviews = app_details['reviews']
#             screenshots = app_details['screenshots']
#             title = app_details['title']
#             download_link = app_details['url']
#             updated = app_details['updated']
#             category1 = app_details['category']
#             category = category1[0]
#             app_size = app_details['size']
#             conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
#                                            password='12345678')
#             cursor = conn.cursor()
#             query = "insert into app_details(package,icon,rating,content_rating,description,current_version,developer,price,installs,title,download_link,updated,category,app_size,app_category,app_like,app_dislike) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d')" % (
#                 package, icon, per_rating, content_rating1, description, current_version, developer, price,
#                 installs,
#                 title,
#                 download_link, updated, category, app_size, '1', 0, 0)
#             cursor.execute(query)
#             conn.commit()
#             app_id = int(cursor.lastrowid)
#             request.session['app_id'] = app_id
#             screenshots = app_details['screenshots']
#             for i in screenshots:
#                 screenshots1 = i
#                 query1 = "insert into app_screenshots(screenshot,app_id) VALUES ('%s','%d')" % (i, app_id)
#                 cursor.execute(query1)
#                 conn.commit()
#
#             headers = {
#                 'X-Apptweak-Key': 'WQA0noCpMD7h2eXVCUEoM57Wubg',
#             }
#
#             params = (
#                 ('country', 'gb'),
#                 ('language', 'en'),
#                 ('max-age', '964000'),
#             )
#
#             URL2 = "https://api.apptweak.com/android/applications/" + package + "/reviews.json"
#             response = requests.get(URL2, headers=headers, params=params)
#
#             json_data1 = json.loads(response.text)
#             req = json_data1['content']
#             #print("comment", req)
#
#             #print(req)
#
#             [pos, neg, neu] = [0, 0, 0]
#             pos_cmt = []
#             neg_cmt = []
#             neu_cmt = []
#             sent = ''
#             result = 0
#             for i in req:
#                 comment = i['body']
#                 strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
#                 string = comment.lower().replace("<br />", " ")
#                 st = re.sub(strip_special_chars, "", comment.lower())
#                 #print(st)
#                 pos, neg, neu, pos_cmt, neg_cmt, neu_cmt = sentiment(st, pos, neg, neu, pos_cmt, neg_cmt, neu_cmt)
#                 #print(pos, neg, neu)
#                 #sent,result=sentiment_percent(pos,neg,neu)
#
#             #print(pos, neg, neu)
#             #print("pos_cmt_list", pos_cmt)
#             #print("neg_cmt_list", neg_cmt)
#             #print("neu_cmt_list", neu_cmt)
#             total = pos + neg + neu
#             pos_per = (pos / total) * 100
#             neg_per = (neg / total) * 100
#             neu_per = (neu / total) * 100
#             #print(pos_per, neg_per, neu_per)
#
#             URL1 = "https://data.42matters.com/api/v3.0/android/apps/topics.json?p=" + package + "&access_token=a773624a8f39d7427cb5c81cc27e728c91d00762"
#             response = requests.get(URL1)
#             #print(response.text)
#             json_data = json.loads(response.text)
#             reviews = json_data
#             number_topics = reviews['number_topics']
#             total_reviews = reviews['total_reviews']
#             number_ratings = reviews['number_ratings']
#             query3 = "insert into app_reviews_result(nooftopic,noofreviews,noofrating,app_id3) VALUES ('%d','%d','%d','%d')" % (
#                 number_topics, total_reviews, number_ratings, app_id)
#             cursor.execute(query3)
#             conn.commit()
#             topic = reviews['topics']
#             rrid = int(cursor.lastrowid)
#
#             for i in topic:
#                 index = i
#                 topic_name = i['topic_name']
#                 no_of_reviews = i['reviews']
#                 positive = i['positive']
#                 per_positive = float(positive) * 100
#                 per_positive = round(per_positive, 2)
#                 negative = i['negative']
#                 per_negative = float(negative) * 100
#                 per_negative = round(per_negative, 2)
#                 average_rating_of_topic = i['average_rating']
#                 per_average_rating_of_topic = float(average_rating_of_topic) * 20
#                 per_average_rating_of_topic = round(per_average_rating_of_topic, 2)
#
#                 query4 = "insert into reviews_topic(topic_name,noofreviews,poscomment,negcomment,avgrating,rrid1) VALUES ('%s','%s','%s','%s','%s','%s')" % (
#                     topic_name, no_of_reviews, per_positive, per_negative, per_average_rating_of_topic, rrid)
#                 cursor.execute(query4)
#                 conn.commit()
#
#             que = "select * from app_details where title='%s'" % (title)
#             cursor.execute(que)
#             a = cursor.fetchone()
#             appid = a[0]
#             query6 = "select screenshot from  app_screenshots where app_id ='%d'" % (appid)
#             cursor.execute(query6)
#             ss = cursor.fetchall()
#             x = len(ss)
#             list = []
#             for i in range(len(ss)):
#                 if i <= 4:
#                     list.append(ss[i])
#
#             query7 = "select * from app_reviews_result where app_id3='%d'" % (appid)
#             cursor.execute(query7)
#             review_result = cursor.fetchone()
#             r_rrid = review_result[0]
#             query8 = "select * from reviews_topic where rrid1='%d'" % (r_rrid)
#             cursor.execute(query8)
#             review_topic = cursor.fetchall()
#             #print(review_topic)
#
#             uid = request.session.get('lid')
#             if (uid):
#                 ap_id = request.session.get('app_id')
#                 ap_id = int(ap_id)
#
#                 query9 = "select * from user_app where user_id='%d' and app_id='%d'" % (uid, ap_id)
#                 cursor.execute(query9)
#                 w = cursor.fetchall()
#                 #print('ww', w)
#                 query10 = "select status from user_app_like_dislike_status where  user_id='%d' and app_id='%d'" % (
#                 uid, ap_id)
#                 cursor.execute(query10)
#                 j1 = cursor.fetchall()
#                 if (j1 == []):
#                     if (w == [] and j1 == []):
#                         in_profile_status = "Add to Profile"
#                         user_like_dislike = "Like"
#                         return render(request, 'new_result.html',
#                                       {'detail': a, 'screenshot': list, 'app_review_result': review_result,
#                                        'reviews_topic': review_topic, 'in_profile_status': in_profile_status,
#                                        'user_like_dislike': user_like_dislike, 'pos_per': pos_per,
#                                        'neg_per': neg_per, 'neu_per': neu_per})
#
#                     if (w != [] and j1 == []):
#                         in_profile_status = "Remove From Profile"
#                         user_like_dislike = "Like"
#                         return render(request, 'new_result.html',
#                                       {'detail': a, 'screenshot': list, 'app_review_result': review_result,
#                                        'reviews_topic': review_topic, 'in_profile_status': in_profile_status,
#                                        'user_like_dislike': user_like_dislike, 'pos_per': pos_per,
#                                        'neg_per': neg_per, 'neu_per': neu_per})
#                 else:
#                     j = j1[0]
#                     k = j[0]
#                     #print("j1", k)
#                     if (w != [] and k == 'Like'):
#                         in_profile_status = "Remove From Profile"
#                         user_like_dislike = "dislike"
#                         return render(request, 'new_result.html',
#                                       {'detail': a, 'screenshot': list, 'app_review_result': review_result,
#                                        'reviews_topic': review_topic, 'in_profile_status': in_profile_status,
#                                        'user_like_dislike': user_like_dislike, 'pos_per': pos_per,
#                                        'neg_per': neg_per, 'neu_per': neu_per})
#                     if (w == [] and k == 'Like'):
#                         in_profile_status = "Add to Profile"
#                         user_like_dislike = "dislike"
#                         return render(request, 'new_result.html',
#                                       {'detail': a, 'screenshot': list, 'app_review_result': review_result,
#                                        'reviews_topic': review_topic, 'in_profile_status': in_profile_status,
#                                        'user_like_dislike': user_like_dislike, 'pos_per': pos_per,
#                                        'neg_per': neg_per, 'neu_per': neu_per})
#
#             else:
#                 return render(request, 'unauth_result.html', {'detail': a, 'screenshot': list})


def s_term(request):
    try:

        search_term = request.GET.get('search_term')
        #print("search_term", search_term)
        select_type = request.GET.get('select_type')
        if (search_term == '' and select_type == ''):
            msg = "Please Enter Your Search Term Or Select Your Search Type..."

            return render(request, 'index.html', {'msg': msg})
        else:
            if (select_type == 'application'):
                #print(search_term)
                #request.session['search_term'] = search_term
                return application_search(request, search_term)

            if (select_type == 'website'):
                return website_search(request, search_term)

            if (select_type == 'software'):
                return software_search_like(request, search_term)



    except Error as e:
        print(e)

        # return render(request, 'new_result.html')


def user_app(request):
    if (request.session.get('lid') is not None):
        try:
            #app_name_from_page=request.GET.get('app_name')
            ##print("app_name_from_page",app_name_from_page)
            submit_value = request.GET.get('submit_value')
            if (submit_value == 'Add to Profile'):

                app_id = int(request.GET.get('app_id'))
                uid = int(request.session.get('lid'))

                title = request.session.get('title')
                conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                               password='12345678'
                                               , auth_plugin='mysql_native_password')
                cursor = conn.cursor()

                query1 = "insert into user_app(user_id,app_id) VALUES ('%d','%d')" % (uid, app_id)
                cursor.execute(query1)
                conn.commit()
                return application_search(request, title)

            else:
                app_id = int(request.GET.get('app_id'))
                uid = int(request.session.get('lid'))

                title = request.session.get('title')
                conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                               password='12345678'
                                               , auth_plugin='mysql_native_password')
                cursor = conn.cursor()

                query1 = "delete from user_app where user_id='%d' and app_id='%d'" % (uid, app_id)
                cursor.execute(query1)
                conn.commit()
                return application_search(request, title)








        except Error as e:
            print(e)

    else:
        return render(request, 'login.html')


def user_web(request):
    if (request.session.get('lid') is not None):
        try:
            #app_name_from_page=request.GET.get('app_name')
            ##print("app_name_from_page",app_name_from_page)
            submit_value = request.GET.get('submit_value')
            if (submit_value == 'Add to Profile'):

                web_id = request.session.get('web_id')
                uid = int(request.session.get('lid'))
                #print("uid", uid)
                #print("we", web_id)

                site_name = request.session.get('site_name')
                conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                               password='12345678'
                                               , auth_plugin='mysql_native_password')
                cursor = conn.cursor()

                query1 = "insert into user_website(user_id,web_id) VALUES ('%d','%d')" % (uid, web_id)
                cursor.execute(query1)
                conn.commit()
                return website_search(request, site_name)

            else:
                web_id = request.session.get('web_id')

                uid = int(request.session.get('lid'))

                site_name = request.session.get('site_name')
                conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                               password='12345678'
                                               , auth_plugin='mysql_native_password')
                cursor = conn.cursor()

                query1 = "delete from user_website where user_id='%d' and web_id='%d'" % (uid, web_id)
                cursor.execute(query1)
                conn.commit()
                return website_search(request, site_name)

        except Error as e:
            print(e)
    else:
        return render(request, 'login.html')


def user_soft(request):
    if (request.session.get('lid') is not None):
        try:
            #app_name_from_page=request.GET.get('app_name')
            ##print("app_name_from_page",app_name_from_page)
            submit_value = request.GET.get('submit_value')
            if (submit_value == 'Add to Profile'):

                soft_id = request.session.get('soft_id')
                uid = int(request.session.get('lid'))
                #print("uid", uid)
                #print("we", soft_id)

                soft_name = request.session.get('soft_name')
                print("software name",soft_name)
                conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                               password='12345678'
                                               , auth_plugin='mysql_native_password')
                cursor = conn.cursor()

                query1 = "insert into user_software(user_id,soft_id) VALUES ('%d','%d')" % (uid, soft_id)
                cursor.execute(query1)
                conn.commit()
                return software_search(request, soft_name)

            else:
                soft_id = request.session.get('soft_id')
                #soft_id = int(request.GET.get('soft_id'))
                #print("soft_id",soft_id)
                uid = int(request.session.get('lid'))

                soft_name = request.session.get('soft_name')
                print("soft_ame",soft_name)
                conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                               password='12345678'
                                               , auth_plugin='mysql_native_password')
                cursor = conn.cursor()

                query1 = "delete from user_software where user_id='%d' and soft_id='%d'" % (uid, soft_id)
                cursor.execute(query1)
                conn.commit()
                return software_search(request, soft_name)

        except Error as e:
            print(e)

    else:
        return render(request, 'login.html')


def user_comment(request):
    ap_id = request.session.get('app_id')
    uid = int(request.session.get('lid'))
    title = request.session.get('title')
    cmt_date = datetime.datetime.now()
    comment = request.POST.get('comment')
    #print("comment", comment)
    if (comment is not None):
        #print(comment)
        comment = request.POST.get('comment')
        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                       password='12345678'
                                       , auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        query = "insert into user_comment (cmt,u_id,app_id,cmt_date) VALUE ('%s','%d','%d','%s')" % (
            comment, uid, ap_id, cmt_date)
        cursor.execute(query)
        conn.commit()
        return application_search(request, title)



    else:

        return application_search(request, title)


def user_web_comment(request):
    web_id = request.session.get('web_id')
    uid = int(request.session.get('lid'))
    site_name = request.session.get('site_name')

    comment = request.POST.get('comment')
    #print("comment", comment)
    cmt_date = datetime.datetime.now()
    #print("date and time of comment", cmt_date)
    comment = request.POST.get('comment')
    #print("comment", comment)
    if (comment is not None):
        #print(comment)
        comment = request.POST.get('comment')
        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                       password='12345678'
                                       , auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        query = "insert into user_web_comment (cmt,user_id,web_id,cmt_date) VALUE ('%s','%d','%d','%s')" % (
            comment, uid, web_id, cmt_date)
        cursor.execute(query)
        conn.commit()
        return website_search(request, site_name)



    else:

        return website_search(request, site_name)


def user_soft_comment(request):
    soft_id = request.session.get('soft_id')
    uid = int(request.session.get('lid'))
    soft_name = request.session.get('soft_name')
    cmt_date = datetime.datetime.now()
    comment = request.POST.get('comment')
    #print("comment", comment)
    if (comment is not None):
        #print(comment)
        comment = request.POST.get('comment')
        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                       password='12345678'
                                       , auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        query = "insert into user_soft_comment (cmt,user_id,soft_id,cmt_date) VALUE ('%s','%d','%d','%s')" % (
            comment, uid, soft_id, cmt_date)
        cursor.execute(query)
        conn.commit()
        return software_search(request, soft_name)



    else:

        return software_search(request, soft_name)


def user_like(request):
    submit_value = request.GET.get('user_like')
    #print("submit", submit_value)
    if (submit_value == 'Like'):
        ap_id = request.session.get('app_id')
        #app_id = int(request.GET.get('app_id'))
        uid = int(request.session.get('lid'))

        title = request.session.get('title')
        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                       password='12345678'
                                       , auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        status = "Like"

        query = "insert into user_app_like_dislike_status(user_id,app_id,status) VALUES ('%d','%d','%s')" % (
        uid, ap_id, status)
        cursor.execute(query)
        conn.commit()

        query1 = "select app_like from app_details where app_id='%d'" % (ap_id)

        #query1 = "insert into user_app(user_id,app_id) VALUES ('%d','%d')" % (uid, app_id)
        cursor.execute(query1)
        like_count = cursor.fetchone()
        #print("like_count", like_count)
        like_count = like_count[0]
        #print("like_count", like_count)
        like_count = like_count + 1
        query2 = "update app_details SET app_like='%d' WHERE app_id='%d' " % (like_count, ap_id)
        # query2="insert into app_like(like_count) VALUES ('%d')" % (like_count)
        cursor.execute(query2)
        conn.commit()
        return application_search(request, title)


    else:
        app_id = int(request.session.get('app_id'))
        uid = int(request.session.get('lid'))

        title = request.session.get('title')
        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                       password='12345678'
                                       , auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        status = "dislike"
        query = "delete from user_app_like_dislike_status where user_id='%d' and app_id='%d'" % (uid, app_id)
        #query="update user_app_like_dislike_status set status='%s' where user_id='%d' and app_id='%d'" %(status,uid,app_id)
        #print(query)

        #query = "insert into user_app_like_dislike_status(user_id,app_id,status) VALUES ('%d','%d','%s')" % (
        #uid, app_id, status)
        cursor.execute(query)
        conn.commit()
        query1 = "select app_dislike from app_details where app_id='%d'" % (app_id)
        cursor.execute(query1)
        dislike_count = cursor.fetchone()
        dislike_count = dislike_count[0]

        dislike_count = dislike_count + 1
        #
        query2 = "update app_details SET app_dislike='%d' WHERE app_id='%d' " % (dislike_count, app_id)
        #print(query2)
        cursor.execute(query2)
        conn.commit()
        return application_search(request, title)


def user_web_like(request):
    submit_value = request.GET.get('user_like')
    #print("submit", submit_value)
    if (submit_value == 'Like'):
        web_id = request.session.get('web_id')
        #app_id = int(request.GET.get('app_id'))
        uid = int(request.session.get('lid'))

        site_name = request.session.get('site_name')
        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                       password='12345678'
                                       , auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        status = "Like"

        query = "insert into user_website_like_dislike_status(user_id,web_id,status) VALUES ('%d','%d','%s')" % (
        uid, web_id, status)
        cursor.execute(query)
        conn.commit()

        query1 = "select web_like from web where web_id='%d'" % (web_id)

        #query1 = "insert into user_app(user_id,app_id) VALUES ('%d','%d')" % (uid, app_id)
        cursor.execute(query1)
        like_count = cursor.fetchone()
        #print("like_count", like_count)
        like_count = like_count[0]
        #print("like_count", like_count)
        like_count = like_count + 1
        query2 = "update web SET web_like='%d' WHERE web_id='%d' " % (like_count, web_id)
        # query2="insert into app_like(like_count) VALUES ('%d')" % (like_count)
        cursor.execute(query2)
        conn.commit()
        return website_search(request, site_name)


    else:
        web_id = int(request.session.get('web_id'))
        uid = int(request.session.get('lid'))

        site_name = request.session.get('site_name')
        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                       password='12345678'
                                       , auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        status = "dislike"
        query = "delete from user_website_like_dislike_status where user_id='%d' and web_id='%d'" % (uid, web_id)
        #query="update user_app_like_dislike_status set status='%s' where user_id='%d' and app_id='%d'" %(status,uid,app_id)
        #print(query)

        #query = "insert into user_app_like_dislike_status(user_id,app_id,status) VALUES ('%d','%d','%s')" % (
        #uid, app_id, status)
        cursor.execute(query)
        conn.commit()
        query1 = "select web_dislike from web where web_id='%d'" % (web_id)
        cursor.execute(query1)
        dislike_count = cursor.fetchone()
        dislike_count = dislike_count[0]

        dislike_count = dislike_count + 1
        #
        query2 = "update web SET web_dislike='%d' WHERE web_id='%d' " % (dislike_count, web_id)
        #print(query2)
        cursor.execute(query2)
        conn.commit()
        return website_search(request, site_name)


def user_soft_like(request):
    submit_value = request.GET.get('user_like')
    #print("submit", submit_value)
    if (submit_value == 'Like'):
        soft_id = request.session.get('soft_id')
        #app_id = int(request.GET.get('app_id'))
        uid = int(request.session.get('lid'))

        soft_name = request.session.get('soft_name')
        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                       password='12345678'
                                       , auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        status = "Like"

        query = "insert into user_software_like_dislike_status(user_id,soft_id,status) VALUES ('%d','%d','%s')" % (
        uid, soft_id, status)
        cursor.execute(query)
        conn.commit()
        #print("soft_id",soft_id)

        query1 = "select title,software_like from new_software where new_software_id='%d'" % (soft_id)

        #query1 = "insert into user_app(user_id,app_id) VALUES ('%d','%d')" % (uid, app_id)
        cursor.execute(query1)
        like = cursor.fetchone()
        #print("like_count", like)
        like_count = like[1]
        #print("like_count", like_count)
        like_count = like_count + 1
        soft_name=like[0]
        #print("soft",soft_name)
        query2 = "update new_software SET software_like='%d' WHERE new_software_id='%d' " % (like_count, soft_id)
        # query2="insert into app_like(like_count) VALUES ('%d')" % (like_count)
        cursor.execute(query2)
        conn.commit()
        return software_search(request, soft_name)


    else:
        soft_id = int(request.session.get('soft_id'))
        uid = int(request.session.get('lid'))

        soft_name = request.session.get('soft_name')
        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                       password='12345678'
                                       , auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        status = "dislike"
        query = "delete from user_software_like_dislike_status where user_id='%d' and soft_id='%d'" % (uid, soft_id)
        #query="update user_app_like_dislike_status set status='%s' where user_id='%d' and app_id='%d'" %(status,uid,app_id)
        #print(query)

        #query = "insert into user_app_like_dislike_status(user_id,app_id,status) VALUES ('%d','%d','%s')" % (
        #uid, app_id, status)
        cursor.execute(query)
        conn.commit()
        query1 = "select software_dislike from new_software where new_software_id='%d'" % (soft_id)
        cursor.execute(query1)
        dislike_count = cursor.fetchone()
        dislike_count = dislike_count[0]

        dislike_count = dislike_count + 1
        #
        query2 = "update new_software SET software_dislike='%d' WHERE new_software_id='%d' " % (dislike_count, soft_id)
        #print(query2)
        cursor.execute(query2)
        conn.commit()
        return software_search(request, soft_name)


def logout(request):


    if(request.session.get('lid') is not None):
        del request.session['lid']
        return render(request, 'login.html')
    else:
        msg="You Have Not Registered Yet!!!"
        return render(request,'register_1.html',{'msg':msg})


def user_request(request):
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678'
                                   , auth_plugin='mysql_native_password')
    cursor = conn.cursor()

    status = "pending"
    query = "select * from registration where status='%s'" % (status)
    cursor.execute(query)
    a = cursor.fetchall()
    ##print(a)
    email = []
    all = []
    for i in a:
        ##print("i",i)
        user_detail = []
        lid = i[10]
        query1 = "select email from login where lid='%d'" % (lid)
        cursor.execute(query1)
        c = cursor.fetchall()
        ##print(c)
        user_detail.append(c[0][0])
        for j in i:
            user_detail.append(j)

        all.append(user_detail)

    ##print("user_detail",all)
    return render(request, 'user_request.html', {'user_detail': all})


def user_request_accept(request):
    rid = int(request.GET.get('rid'))

    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678'
                                   , auth_plugin='mysql_native_password')
    cursor = conn.cursor()
    query2 = "update registration SET status='%s' WHERE rid='%d' " % ('other', rid)
    cursor.execute(query2)
    conn.commit()
    q = "select lid from registration where rid='%d'" % (rid)
    cursor.execute(q)
    q1 = cursor.fetchall()
    w = "select email from login where lid='%d' " % (q1[0])
    cursor.execute(w)
    w1 = cursor.fetchall()
    body = '''Dear user, As you choose other profession or educational backgrond at your registration time so we are not able to recommend you application,website and software because we have not enough data at this time but you can use other functionality of CatchApp.
            Sorry for inconvenience...
    '''
    #print('emailid---', w1[0][0])
    email = EmailMessage('CatchApp', body, to=[w1[0][0]])
    email.send()

    status = "pending"
    query = "select * from registration where status='%s'" % (status)
    cursor.execute(query)
    a = cursor.fetchall()
    # #print(a)
    email = []
    all = []
    for i in a:
        # #print("i",i)
        user_detail = []
        lid = i[10]
        query1 = "select email from login where lid='%d'" % (lid)
        cursor.execute(query1)
        c = cursor.fetchall()
        # #print(c)
        user_detail.append(c[0][0])
        for j in i:
            user_detail.append(j)

        all.append(user_detail)

    return render(request, 'user_request.html', {'user_detail': all})


def user_request_reject(request):
    rid = int(request.GET.get('rid'))
    #print(rid)

    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678'
                                   , auth_plugin='mysql_native_password')
    cursor = conn.cursor()

    query = "select lid from registration where rid='%d'" % (rid)
    cursor.execute(query)
    a = cursor.fetchall()
    x = a[0]
    x1 = x[0]
    #print(x1)
    query4 = "delete from user_interest where rid='%d'" % (rid)
    cursor.execute(query4)
    conn.commit()

    query2 = "delete from registration where rid='%d'" % (rid)
    cursor.execute(query2)
    conn.commit()
    query3 = "delete from login where lid='%d'" % (x1)
    cursor.execute(query3)
    conn.commit()

    status = "pending"
    query = "select * from registration where status='%s'" % (status)
    cursor.execute(query)
    a = cursor.fetchall()
    # #print(a)
    email = []
    all = []
    for i in a:
        # #print("i",i)
        user_detail = []
        lid = i[10]
        query1 = "select email from login where lid='%d'" % (lid)
        cursor.execute(query1)
        c = cursor.fetchall()
        # #print(c)
        user_detail.append(c[0][0])
        for j in i:
            user_detail.append(j)

        all.append(user_detail)

    return render(request, 'user_request.html', {'user_detail': all})


def application_admin(request):
    return render(request, 'application_admin.html')


def website_admin(request):
    return render(request, 'website_admin.html')


def software_admin(request):
    return render(request, 'software_admin_new.html')


def application_search_treanding(st):
    try:
        #print("request:", st)
        search_term = st
        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                       password='12345678'
                                       , auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        app_name = play_scraper.search(search_term, page=1)
        app_search = app_name[0]
        title = app_search['title']
        # request.session['title'] = title
        query5 = "select * from app_details where title='%s'" % (title)
        #print(search_term)
        cursor.execute(query5)
        a = cursor.fetchall()
        #print("ac", a)

        if (a == []):
            #print("hello")
            #print(search_term)
            app_name = play_scraper.search(search_term, page=1)
            app_search = app_name[0]
            package = app_search['app_id']
            app_details = play_scraper.details(package)
            icon = app_details['icon']
            rating = app_details['score']
            per_rating = float(rating) * 20
            per_rating = round(per_rating, 2)
            content_rating = app_details['content_rating']
            content_rating1 = content_rating[0]
            str = app_details['description']
            strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
            string = str.lower().replace("<br />", " ")
            description = re.sub(strip_special_chars, "", str.lower())
            current_version = app_details['current_version']
            developer = app_details['developer']
            price = app_details['price']
            installs = app_details['installs']
            reviews = app_details['reviews']
            screenshots = app_details['screenshots']
            title = app_details['title']
            download_link = app_details['url']
            updated = app_details['updated']
            category1 = app_details['category']
            category = category1[0]
            app_size = app_details['size']
            conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                           password='12345678')
            cursor = conn.cursor()
            query = "insert into app_details(package,icon,rating,content_rating,description,current_version,developer,price,installs,title,download_link,updated,category,app_size,app_category,app_like,app_dislike) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d')" % (
                package, icon, per_rating, content_rating1, description, current_version, developer, price, installs,
                title,
                download_link, updated, category, app_size, 'Trending', 0, 0)
            cursor.execute(query)
            conn.commit()
            app_id = int(cursor.lastrowid)
            # request.session['app_id'] = app_id
            screenshots = app_details['screenshots']
            for i in screenshots:
                screenshots1 = i
                query1 = "insert into app_screenshots(screenshot,app_id) VALUES ('%s','%d')" % (i, app_id)
                cursor.execute(query1)
                conn.commit()

            URL1 = "https://data.42matters.com/api/v3.0/android/apps/topics.json?p=" + package + "&access_token=f179acc1234fe6a99bb429b1682595bbac44be22"
            response = requests.get(URL1)
            #print(response.text)
            json_data = json.loads(response.text)
            reviews = json_data
            #print(reviews)
            number_topics = reviews['number_topics']
            total_reviews = reviews['total_reviews']
            number_ratings = reviews['number_ratings']
            query3 = "insert into app_reviews_result(nooftopic,noofreviews,noofrating,app_id3) VALUES ('%d','%d','%d','%d')" % (
                number_topics, total_reviews, number_ratings, app_id)
            cursor.execute(query3)
            conn.commit()
            topic = reviews['topics']
            rrid = int(cursor.lastrowid)

            for i in topic:
                index = i
                topic_name = i['topic_name']
                no_of_reviews = i['reviews']
                positive = i['positive']
                per_positive = float(positive) * 100
                per_positive = round(per_positive, 2)
                negative = i['negative']
                per_negative = float(negative) * 100
                per_negative = round(per_negative, 2)
                average_rating_of_topic = i['average_rating']
                per_average_rating_of_topic = float(average_rating_of_topic) * 20
                per_average_rating_of_topic = round(per_average_rating_of_topic, 2)

                query4 = "insert into reviews_topic(topic_name,noofreviews,poscomment,negcomment,avgrating,rrid1) VALUES ('%s','%s','%s','%s','%s','%s')" % (
                    topic_name, no_of_reviews, per_positive, per_negative, per_average_rating_of_topic, rrid)
                cursor.execute(query4)
                conn.commit()

            #print("successful!!!!")




        else:

            b = a[0]
            #print(b[15])
            if (b[15] == 'new'):

                query2 = "update app_details SET app_category='%s' WHERE title='%s' " % ('both', title)
                cursor.execute(query2)
                #print(query2)
                conn.commit()


            else:

                query2 = "update app_details SET app_category='%s' WHERE title='%s' " % ('treanding', title)
                cursor.execute(query2)
                #print(query2)
                conn.commit()

                #print("Already existed")

                # if()
                #
                # query2 = "update app_details SET app_category='%s' WHERE title='%s' " % ('trending',title)
                # cursor.execute(query2)
                # #print(query2)
                # conn.commit()
                #
                # #print("Already existed")



    except Error as e:
        print(e)


def treanding_app(request):
    submit_value = request.GET.get('submit_trending')
    #print(submit_value)
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678')
    cursor = conn.cursor()
    if (submit_value == 'Update'):
        # query2 = "update app_details SET app_category='%s' where app_category='%s'" % ('all', 'treanding')
        # cursor.execute(query2)
        # #print(query2)
        # conn.commit()
        # query3 = "update app_details SET app_category='%s' where app_category='%s'" % ('new', 'both')
        # cursor.execute(query3)
        # #print(query3)
        # conn.commit()
        # list = play_scraper.collection(collection='TRENDING', results=120, gl='in', page=1)
        # count = 0
        # for i in list:
        #     #print(count)
        #     a = i['title']
        #     pprint(a)
        #     application_search_treanding(a)
        #     count = count + 1
        updated1 = "Updated"
        return render(request, 'application_admin.html', {'Treanding_App_updated': updated1})

    if (submit_value == 'Show'):
        #print("aaa")
        query = "select * from app_details where app_category='%s' or app_category='%s' " % ('treanding', 'both')
        cursor.execute(query)
        treandinng_app = cursor.fetchall()
        #print(treandinng_app)

        return render(request, 'treanding_app_admin.html', {'treandinng_app': treandinng_app})


def treanding_app_remove(request):
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678')
    cursor = conn.cursor()
    app_id = int(request.GET.get('app_id'))
    query = "select app_category from app_details where app_id='%d' " % (app_id)
    cursor.execute(query)
    a = cursor.fetchall()
    category = a[0][0]
    #print("category", category)
    if (category == 'treanding'):
        query2 = "update app_details SET app_category='%s' where app_id='%d'" % ('all', app_id)
        cursor.execute(query2)
        #print(query2)
        conn.commit()
    if (category == 'both'):
        query2 = "update app_details SET app_category='%s' where app_id='%d'" % ('new', app_id)
        cursor.execute(query2)
        #print(query2)
        conn.commit()

    query = "select * from app_details where app_category='%s' or app_category='%s'" % ('treanding', 'both')
    cursor.execute(query)
    treandinng_app = cursor.fetchall()
    #print(treandinng_app)

    return render(request, 'treanding_app_admin.html', {'treandinng_app': treandinng_app})


def application_search_new(st):
    try:
        #print("request:", st)
        search_term = st
        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                       password='12345678'
                                       , auth_plugin='mysql_native_password')
        cursor = conn.cursor()
        app_name = play_scraper.search(search_term, page=1)
        app_search = app_name[0]
        title = app_search['title']
        # request.session['title'] = title
        query5 = "select * from app_details where title='%s'" % (title)
        #print(search_term)
        cursor.execute(query5)
        a = cursor.fetchall()
        #print("ac", a)

        if (a == []):
            #print("hello")
            #print(search_term)
            app_name = play_scraper.search(search_term, page=1)
            app_search = app_name[0]
            package = app_search['app_id']
            app_details = play_scraper.details(package)
            icon = app_details['icon']
            rating = app_details['score']
            per_rating = float(rating) * 20
            per_rating = round(per_rating, 2)
            content_rating = app_details['content_rating']
            content_rating1 = content_rating[0]
            str = app_details['description']
            strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
            string = str.lower().replace("<br />", " ")
            description = re.sub(strip_special_chars, "", str.lower())
            current_version = app_details['current_version']
            developer = app_details['developer']
            price = app_details['price']
            installs = app_details['installs']
            reviews = app_details['reviews']
            screenshots = app_details['screenshots']
            title = app_details['title']
            download_link = app_details['url']
            updated = app_details['updated']
            category1 = app_details['category']
            category = category1[0]
            app_size = app_details['size']
            conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                           password='12345678')
            cursor = conn.cursor()
            query = "insert into app_details(package,icon,rating,content_rating,description,current_version,developer,price,installs,title,download_link,updated,category,app_size,app_category,app_like,app_dislike) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d')" % (
                package, icon, per_rating, content_rating1, description, current_version, developer, price, installs,
                title,
                download_link, updated, category, app_size, 'new', 0, 0)
            cursor.execute(query)
            conn.commit()
            app_id = int(cursor.lastrowid)
            # request.session['app_id'] = app_id
            screenshots = app_details['screenshots']
            for i in screenshots:
                screenshots1 = i
                query1 = "insert into app_screenshots(screenshot,app_id) VALUES ('%s','%d')" % (i, app_id)
                cursor.execute(query1)
                conn.commit()

            URL1 = "https://data.42matters.com/api/v3.0/android/apps/topics.json?p=" + package + "&access_token=f179acc1234fe6a99bb429b1682595bbac44be22"
            response = requests.get(URL1)
            #print(response.text)
            json_data = json.loads(response.text)
            reviews = json_data
            #print(reviews)
            number_topics = reviews['number_topics']
            total_reviews = reviews['total_reviews']
            number_ratings = reviews['number_ratings']
            query3 = "insert into app_reviews_result(nooftopic,noofreviews,noofrating,app_id3) VALUES ('%d','%d','%d','%d')" % (
                number_topics, total_reviews, number_ratings, app_id)
            cursor.execute(query3)
            conn.commit()
            topic = reviews['topics']
            rrid = int(cursor.lastrowid)

            for i in topic:
                index = i
                topic_name = i['topic_name']
                no_of_reviews = i['reviews']
                positive = i['positive']
                per_positive = float(positive) * 100
                per_positive = round(per_positive, 2)
                negative = i['negative']
                per_negative = float(negative) * 100
                per_negative = round(per_negative, 2)
                average_rating_of_topic = i['average_rating']
                per_average_rating_of_topic = float(average_rating_of_topic) * 20
                per_average_rating_of_topic = round(per_average_rating_of_topic, 2)

                query4 = "insert into reviews_topic(topic_name,noofreviews,poscomment,negcomment,avgrating,rrid1) VALUES ('%s','%s','%s','%s','%s','%s')" % (
                    topic_name, no_of_reviews, per_positive, per_negative, per_average_rating_of_topic, rrid)
                cursor.execute(query4)
                conn.commit()

            #print("successful!!!!")




        else:
            b = a[0]
            #print(b[15])
            if (b[15] == 'treanding'):

                query2 = "update app_details SET app_category='%s' WHERE title='%s' " % ('both', title)
                cursor.execute(query2)
                #print(query2)
                conn.commit()


            else:

                query2 = "update app_details SET app_category='%s' WHERE title='%s' " % ('new', title)
                cursor.execute(query2)
                #print(query2)
                conn.commit()

                #print("Already existed")



    except Error as e:
        print(e)


def new_app(request):
    submit_value = request.GET.get('new_submit')
    #print(submit_value)
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678')
    cursor = conn.cursor()
    if (submit_value == 'Update'):
        #print("update loop")
        # query2 = "update app_details SET app_category='%s' where app_category='%s'" % ('all', 'new')
        # cursor.execute(query2)
        # #print(query2)
        # conn.commit()
        # query3 = "update app_details SET app_category='%s' where app_category='%s'" % ('treanding', 'both')
        # cursor.execute(query3)
        # #print(query3)
        # conn.commit()
        #
        # list = play_scraper.collection(collection='NEW_FREE', results=100, gl='in', page=1)
        # count = 0
        # for i in list:
        #     #print(count)
        #     a = i['title']
        #     pprint(a)
        #     application_search_new(a)
        #     count = count + 1
        #     #print("application_search_new", a)
        updated1 = "Updated"
        return render(request, 'application_admin.html', {'New_App_updated': updated1})

    if (submit_value == 'Show'):
        #print("aaa")
        query = "select * from app_details where app_category='%s' or app_category='%s'" % ('new', 'both')
        cursor.execute(query)
        treandinng_app = cursor.fetchall()
        #print(treandinng_app)

        return render(request, 'new_app_admin.html', {'new_app': treandinng_app})


def new_app_remove(request):
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678')
    cursor = conn.cursor()
    app_id = int(request.GET.get('app_id'))
    query = "select app_category from app_details where app_id='%d' " % (app_id)
    cursor.execute(query)
    a = cursor.fetchall()
    category = a[0][0]
    #print("category", category)
    if (category == 'new'):
        query2 = "update app_details SET app_category='%s' where app_id='%d'" % ('all', app_id)
        cursor.execute(query2)
        #print(query2)
        conn.commit()
    if (category == 'both'):
        query2 = "update app_details SET app_category='%s' where app_id='%d'" % ('treanding', app_id)
        cursor.execute(query2)
        #print(query2)
        conn.commit()

    query = "select * from app_details where app_category='%s' or app_category='%s'" % ('new', 'both')
    cursor.execute(query)
    treandinng_app = cursor.fetchall()
    #print(treandinng_app)

    return render(request, 'new_app_admin.html', {'new_app': treandinng_app})


def website_search_trending(request):
    status = request.GET.get('select_type')
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678')
    cursor = conn.cursor()
    #print(status)
    query = "select site_name from website where status='%s'" % (status)
    cursor.execute(query)
    a = cursor.fetchall()
    site = ''

    for i in a:
        query8 = "select title from web where title='%s'" % (i[0])
        cursor.execute(query8)
        b = cursor.fetchall()

        if (b == ''):
            site = i[0]
            new_word = i[0].split('.', 2)
            new_word1 = new_word[0]
            new_word2 = "&nbsp"
            new_string = "".join((new_word2, new_word1))

            url = "https://www.alexa.com/siteinfo/" + i[0] + ""
            html = urlopen(url)

            soup = BeautifulSoup(html, 'lxml')
            type(soup)

            global_rank = 0
            country_rank = 0
            bounce_rate = 0
            daily_time_on_site = 0
            daily_pageview_per_visitor = 0
            total_site_linking_in = 0
            rank_in_country_name = 0
            loading_time = 0
            description = 0
            rank_image = 0
            country1 = 0
            country2 = 0
            country3 = 0
            country4 = 0
            country4 = 0
            country5 = 0
            percent_of_visitor1 = 0
            percent_of_visitor2 = 0
            percent_of_visitor3 = 0
            percent_of_visitor4 = 0
            percent_of_visitor5 = 0
            rank_in_country1 = 0
            rank_in_country2 = 0
            rank_in_country3 = 0
            rank_in_country4 = 0
            rank_in_country5 = 0
            rank_in_country = 0

            # gloal_rank and country rank
            all_strong = soup.find_all("strong")
            list_of_strong = []
            for h in all_strong:
                list_of_strong.append(h.text.strip())
            global_rank = list_of_strong[6]
            #print("gloal", global_rank)
            country_rank = list_of_strong[9]
            #print("coutry", country_rank)
            for i in range(len(list_of_strong)):

                if list_of_strong[i] == 'Daily Time on Site':
                    index = i

                    bounce_rate = list_of_strong[int(index) + int(1)]
                    #print("ouce", bounce_rate)
                    daily_pageview_per_visitor = list_of_strong[int(index) + int(2)]
                    #print("daily pageview", daily_pageview_per_visitor)
                    daily_time_on_site = list_of_strong[int(index) + int(3)]
                    #print("daily time o ", daily_time_on_site)
                if list_of_strong[i] == 'Alexa Pro Basic Plan':
                    index1 = i
                    total_site_linking_in1 = list_of_strong[int(index1) + int(1)]
                    total_site_linking_in = str(total_site_linking_in1)
            #print("total", total_site_linking_in)

            # Country_name
            anchor_tags = soup.find_all("a")
            for j in range(len(anchor_tags)):
                a = anchor_tags[j].text.strip()

                if a == 'Certified Site Metrics FAQs':
                    index = j
                    rank_in_country_name = anchor_tags[int(index) + int(1)].text.strip()
                    #print("rak", rank_in_country_name)

            # loading_time And Description

            para = soup.find_all("p")
            for k in range(len(para)):
                a = para[k].text.strip()
                if a == 'The load time metric is updated monthly.':
                    index = k
                    loading_time = para[int(index) + int(1)].text.strip()
                    #print("loadig", loading_time)
                    description1 = para[int(index) + int(4)].text.strip()

                    strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
                    string = description1.lower().replace("<br />", " ")
                    description = re.sub(strip_special_chars, "", description1.lower())
                    #print("descriptio", description)
            # image of traffic rank

            img_list = []
            all_links = soup.find_all("img")
            count = 0
            for link in all_links:
                # #print(count)
                img_list.append(link.get("src"))
                count = count + 1
            rank_image = img_list[5]
            #print("rak", rank_image)

            query = "insert into web(global_rank,country_rank,bounce_rate,daily_time_on_site,daily_page_view_per_visitor,rank_image,total_site_linking_in,loading_time,description,country_name,title,category,web_like,web_dislike) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d')" % (
                global_rank, country_rank, bounce_rate, daily_time_on_site, daily_pageview_per_visitor, rank_image,
                total_site_linking_in, loading_time, description, rank_in_country_name, site, status, 0, 0)
            #print(query)
            cursor.execute(query)
            conn.commit()

            web_id = int(cursor.lastrowid)

            # Audiace Geography

            list = []
            td_tags = soup.find_all("td")
            for t in td_tags:
                list.append(t.text.strip())
                count = count + 1

            for l in range(len(list)):

                if list[
                    l] == "Loyalty Metrics\n\n\n\nSee how much a country's visitors remain engaged over time. Based on Monthly\nUnique Visitor, Visit, and Pageview estimates in each country where those metrics are available.\n\n \nBased on unique visitor estimates\n\n\nVisits per Visitor\n\nAdvanced Plan Only\n\n\nPageviews per Visit\n\nAdvanced Plan Only\n\n\nMonthly Pageviews per Visitor\n\nAdvanced Plan Only":

                    index = l
                    # #print(index)
                    try:
                        country1 = list[int(index) + int(1)]
                        percent_of_visitor1 = list[int(index) + int(2)]
                        rank_in_country1 = list[int(index) + int(3)]
                        # #print(country1,percent_of_visitor1,rank_in_country1)


                    except Error as e:
                        continue
                    try:
                        country2 = list[int(index) + int(4)]
                        percent_of_visitor2 = list[int(index) + int(5)]
                        rank_in_country2 = list[int(index) + int(6)]
                        # #print(country2,percent_of_visitor2,rank_in_country2)
                    except Error as e:
                        continue
                    try:
                        country3 = list[int(index) + int(7)]
                        percent_of_visitor3 = list[int(index) + int(8)]
                        rank_in_country3 = list[int(index) + int(9)]

                    except Error as e:
                        continue

                    try:
                        country4 = list[int(index) + int(10)]
                        percent_of_visitor4 = list[int(index) + int(11)]
                        rank_in_country4 = list[int(index) + int(12)]
                        # #print (country4)
                    except Error as e:
                        continue
                    try:
                        country5 = list[int(index) + int(13)]
                        percent_of_visitor5 = list[int(index) + int(14)]
                        rank_in_country5 = list[int(index) + int(15)]
                        # #print(country5,percent_of_visitor5,rank_in_country5)
                    except Error as e:
                        continue
            # #print (country1,country2,country3,country4,country5)

            # if country1 is null then
            if country1 == 0:
                query1 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                    list[0], list[1], list[2], web_id)
                cursor.execute(query1)
                conn.commit()

            elif country3 == "1. &nbsp" + new_word1 + "":
                xyz = country3.split('\xa0', 2)
                p = xyz[1]
                # #print (xyz)
                if p == new_string:
                    query1 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country1, percent_of_visitor1, rank_in_country1, web_id)
                    cursor.execute(query1)
                    conn.commit()
                    query2 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country2, percent_of_visitor2, rank_in_country2, web_id)
                    cursor.execute(query2)
                    conn.commit()




            # if country 4 is nbsp then
            elif country4 == "1. &nbsp" + new_word1 + "":
                xyz = country4.split('\xa0', 2)
                p = xyz[1]
                # #print (xyz)
                if p == new_string:
                    query1 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country1, percent_of_visitor1, rank_in_country1, web_id)
                    cursor.execute(query1)
                    conn.commit()
                    query2 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country2, percent_of_visitor2, rank_in_country2, web_id)
                    cursor.execute(query2)
                    conn.commit()

                    query3 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country3, percent_of_visitor3, rank_in_country3, web_id)
                    cursor.execute(query3)
                    conn.commit()

            # if country5 is nbsp then
            elif country5 == "1. &nbsp" + new_word1 + "":
                xyz = country5.split('\xa0', 2)
                p = xyz[1]
                # #print (xyz)
                if p == new_string:
                    query1 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country1, percent_of_visitor1, rank_in_country1, web_id)
                    cursor.execute(query1)
                    conn.commit()
                    query2 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country2, percent_of_visitor2, rank_in_country2, web_id)
                    cursor.execute(query2)
                    conn.commit()

                    query3 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country3, percent_of_visitor3, rank_in_country3, web_id)
                    cursor.execute(query3)
                    conn.commit()
                    query4 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                        country4, percent_of_visitor4, rank_in_country4, web_id)
                    cursor.execute(query4)
                    conn.commit()

            else:
                query1 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                    country1, percent_of_visitor1, rank_in_country1, web_id)
                cursor.execute(query1)
                conn.commit()
                query2 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                    country2, percent_of_visitor2, rank_in_country2, web_id)
                cursor.execute(query2)
                conn.commit()

                query3 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                    country3, percent_of_visitor3, rank_in_country3, web_id)
                cursor.execute(query3)
                conn.commit()
                query4 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                    country4, percent_of_visitor4, rank_in_country4, web_id)
                cursor.execute(query4)
                conn.commit()
                query5 = "insert into web_table(country_name,percent_of_visitor,rank_in_country,web_id) VALUES ('%s','%s','%s','%d')" % (
                    country5, percent_of_visitor5, rank_in_country5, web_id)
                cursor.execute(query5)
                conn.commit()

                msg = "Added..."
                return render(request, 'website_admin.html', {'msg': msg})

        else:
            msg = "Updated..."
            return render(request, 'website_admin.html', {'msg': msg})


def website_treading_display(request):
    select_type = request.GET.get('select_type')
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678')
    cursor = conn.cursor()

    query = "select web_id,title from web where category='%s'" % (select_type)
    cursor.execute(query)
    treanding_web = cursor.fetchall()
    #print(treanding_web)
    return render(request, 'treanding_web_show.html', {'treanding_web': treanding_web, 'category': select_type})


def treanding_web_remove(request):
    web_id = int(request.GET.get('web_id'))

    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678')
    cursor = conn.cursor()

    query = "select category from web where web_id='%d'" % (web_id)
    cursor.execute(query)
    category = cursor.fetchall()
    ab = category[0][0]
    #print("value", ab)

    query2 = "update web SET category='%s' where web_id='%d'" % ('all', web_id)
    cursor.execute(query2)
    #print(query2)
    conn.commit()
    #print("comp")

    query = "select web_id,title from web where category='%s'" % (ab)
    cursor.execute(query)
    treandinng_web = cursor.fetchall()
    #print(treandinng_web)

    return render(request, 'treanding_web_show.html', {'treanding_web': treandinng_web, 'category': ab})


def app_display(request):
    app_name = request.GET.get('app_name')
    #print(app_name)
    return application_search(request, app_name)


def web_display(request):
    web_name = request.GET.get('web_name')
    #print(web_name)
    return website_search(request, web_name)


def new_software_search(request, soft_name):
    st = soft_name
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678')
    cursor = conn.cursor()
    query = "select * from new_software where title='%s'" % (st)
    cursor.execute(query)
    a = cursor.fetchall()
    #print(a)

    if (request.session.get('lid') is not None):
        pos, neg, neu = query_twitter(st, 100)
        total = pos + neg + neu
        pos_per = (pos / total) * 100
        neg_per = (neg / total) * 100
        neu_per = (neu / total) * 100
        #print("perce", pos_per, neg_per, neu_per)
        return render(request, 'result_download.com_software.html', {'software': a})



    else:
        return render(request, 'result_download.com_software_unauth.html', {'software': a})


def soft_display(request):
    soft_name = request.GET.get('soft_name')
    print("1",soft_name)
    return software_search(request, soft_name)


def treanding_soft(request):
    submit_value = request.GET.get('submit_trending')
    #print(submit_value)
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678')
    cursor = conn.cursor()
    if (submit_value == 'Update'):
        #print("hello")
        msg = "updated.."
        return render(request, 'software_admin_new.html', {'msg': msg})

    if (submit_value == 'Show'):
        #print("aaa")
        category = "trending"
        query = "select * from new_software where status='%s'" % (category)
        cursor.execute(query)
        treandinng_app = cursor.fetchall()
        #print(treandinng_app)

        return render(request, 'treanding_soft_admin.html', {'treandinng_soft': treandinng_app})


def treanding_soft_remove(request):
    soft_id = int(request.GET.get('soft_id1'))
    #print(soft_id)
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678')
    cursor = conn.cursor()
    query = "delete from new_software where new_software_id='%d' " % (soft_id)
    cursor.execute(query)
    conn.commit()
    query = "select * from new_software where status='%s'" % ('trending')
    cursor.execute(query)
    treandinng_app = cursor.fetchall()
    #print(treandinng_app)

    return render(request, 'treanding_soft_admin.html', {'treandinng_soft': treandinng_app})


def new_soft(request):
    submit_value = request.GET.get('new_submit')
    #print(submit_value)
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678')
    cursor = conn.cursor()
    if (submit_value == 'Update'):
        #print("update loop")
        # category = "new"
        # query = "delete FROM software_trending WHERE status='%s'" % (category)
        # cursor.execute(query)
        # conn.commit()
        # query1 = "delete FROM new_software WHERE status='%s'" % (category)
        # cursor.execute(query1)
        # conn.commit()
        #
        # n = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        # list1 = []
        # list2 = []
        # for i in n:
        #     j = str(i)
        #     url = "https://download.cnet.com/s/software/windows/?sort=latest&page=" + j + ""
        #     html = urlopen(url)
        #
        #     soup = BeautifulSoup(html, 'lxml')
        #     type(soup)
        #
        #     a = soup.find_all('div', class_='title OneLinkNoTx')
        #     for h in a:
        #         list1.append(h.text.strip())
        #
        #     link = soup.find_all('a')
        #     # #print (link)
        #     ##print(link)
        #     count = 0
        #     for k in range(len(link)):
        #         count = count + 1
        #         ##print(count)
        #         if count >= 51 and count <= 60:
        #             list2.append(link[k].get('href'))
        #
        #
        #
        #             # #print("name", list_of_h3)
        #             # #print("link", href)
        # #print(list1)
        # #print(len(list1))
        # #print(list2)
        #
        # for i in range(len(list1)):
        #     ##print("name",i)
        #     for j in range(len(list2)):
        #         ##print("link",j)
        #         if i == j:
        #             link1 = "https://download.cnet.com"
        #             link2 = list2[j]
        #             link = "".join((link1, link2))
        #
        #             title = list1[i]
        #             strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
        #             string = title.lower().replace("<br />", " ")
        #             title1 = re.sub(strip_special_chars, "", title.lower())
        #             #print(title1)
        #             #print("name", title1, "link", link)
        #
        #             query = "insert into software_trending(name,link,status) VALUES ('%s','%s','%s')" % (
        #             title1, link, 'new')
        #
        #             cursor.execute(query)
        #             conn.commit()
        # status = "new"
        # query = "select link from software_trending where status='%s'" % (status)
        # cursor.execute(query)
        # a = cursor.fetchall()
        # ##print(a)
        # count1 = 0
        # for i in a:
        #     #print(count1)
        #     if count1 >= 1:
        #         url = i[0]
        #         html = urlopen(url)
        #
        #         soup = BeautifulSoup(html, 'lxml')
        #         type(soup)
        #
        #         a = soup.find_all('span')
        #         count = 0
        #         for i in a:
        #             count = count + 1
        #             ##print(count)
        #             if count == 17:
        #                 title = i.text.strip()
        #                 #print(title)
        #
        #         img_list = []
        #         all_links = soup.find_all("img")
        #         count = 0
        #         for link in all_links:
        #             ##print(count)
        #             img_list.append(link.get("src"))
        #
        #         #img=img_list[2]
        #         for k in img_list:
        #             count = count + 1
        #             ##print(count)
        #             ##print(k)
        #             icon = img_list[6]
        #         #print("img")
        #
        #         p = soup.find_all('p')
        #         count = 0
        #         for x in p:
        #             count = count + 1
        #             ##print(count)
        #             if count == 3:
        #                 description1 = x.text.strip()
        #                 #str = app_details['description']
        #                 strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
        #                 string = description1.lower().replace("<br />", " ")
        #                 description = re.sub(strip_special_chars, "", description1.lower())
        #                 #print(description)
        #
        #         rating = soup.find_all('span', class_='stars')
        #         count = 0
        #         for b in rating:
        #             count = count + 1
        #             if count == 1:
        #                 rating = b.text.strip()
        #                 #print(rating)
        #
        #         td = soup.find_all("td")
        #         count = 0
        #         for z in range(len(td)):
        #             count = count + 1
        #             ##print(count)
        #             q = td[z].text.strip()
        #             if q == "Publisher":
        #                 index = z
        #                 publisher = td[int(index) + int(1)].text.strip()
        #             if q == "Publisher web site":
        #                 index = z
        #                 publisher_website = td[int(index) + int(1)].text.strip()
        #             if q == "Release Date":
        #                 index = z
        #                 Release_Date = td[int(index) + int(1)].text.strip()
        #             if q == "Date Added":
        #                 index = z
        #                 date_added = td[int(index) + int(1)].text.strip()
        #             if q == "Version":
        #                 index = z
        #                 version = td[int(index) + int(1)].text.strip()
        #             if q == "Category":
        #                 index = z
        #                 category = td[int(index) + int(1)].text.strip()
        #             if q == "Subcategory":
        #                 index = z
        #                 subcategory = td[int(index) + int(1)].text.strip()
        #             if q == "Operating Systems":
        #                 index = z
        #                 os = td[int(index) + int(1)].text.strip()
        #             if q == "Additional Requirements":
        #                 index = z
        #                 requirment = td[int(index) + int(1)].text.strip()
        #             if q == "File Size":
        #                 index = z
        #                 size = td[int(index) + int(1)].text.strip()
        #             if q == "File Name":
        #                 index = z
        #                 file_name = td[int(index) + int(1)].text.strip()
        #             if q == "Total Downloads":
        #                 index = z
        #                 total_downloads = td[int(index) + int(1)].text.strip()
        #             if q == "Downloads Last Week":
        #                 index = z
        #                 downloads_last_week = td[int(index) + int(1)].text.strip()
        #             if q == "License Model":
        #                 index = z
        #                 licence_version = td[int(index) + int(1)].text.strip()
        #             if q == "Limitations":
        #                 index = z
        #                 limitations = td[int(index) + int(1)].text.strip()
        #             if q == "Price":
        #                 index = z
        #                 price = td[int(index) + int(1)].text.strip()
        #
        #         #print("publisher", publisher)
        #         #print("publisher_website", publisher_website)
        #         #print("release date", Release_Date)
        #         #print("dtae added", date_added)
        #         #print("version", version)
        #         #print("category", category)
        #         #print("subcategory", subcategory)
        #         #print("os", os)
        #         #print("additional requirmet", requirment)
        #         #print("size", size)
        #         #print("total downloads", total_downloads)
        #         #print("download last week", downloads_last_week)
        #         #print("license", licence_version)
        #         #print("limitiation", limitations)
        #         #print("price", price)
        #
        #         #CNET's Site Terms of Use
        #         query1 = "insert into new_software(title,icon,description,rating,publisher,publisher_website,release_date,date_added,version,category,subcategory,os,additional_requirment,size,total_download,download_last_week,license,limitation,price,software_category,count,software_like,software_dislike,status) values ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d','%d','%d','%s')" % \
        #                  (title, icon, description, rating, publisher, publisher_website, Release_Date, date_added,
        #                   version, category, subcategory, os, requirment, size, total_downloads, downloads_last_week,
        #                   licence_version, limitations, price, 0, 0, 0, 0, status)
        #         cursor.execute(query1)
        #         conn.commit()
        #     count1 = count1 + 1

        msg = "updated..."
        return render(request, 'software_admin_new.html', {'msg': msg})
        #return render(request, 'application_admin.html', {'New_App_updated': updated1})

    if (submit_value == 'Show'):
        #print("aaa")
        query = "select * from app_details where app_category='%s' or app_category='%s'" % ('new', 'both')
        cursor.execute(query)
        treandinng_app = cursor.fetchall()
        #print(treandinng_app)

        return render(request, 'new_app_admin.html', {'new_app': treandinng_app})


def added_app(request):
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678')
    cursor = conn.cursor()
    lid=request.session.get('lid')
    q="select app_id from user_app WHERE user_id='%d'"%(lid)
    cursor.execute(q)
    a=cursor.fetchall()
    list=[]
    rate=[]
    for i in a:
        a_id=i[0]
        query="select * from app_details where app_id='%d'"%(a_id)
        cursor.execute(query)
        f=cursor.fetchall()
        ##print(f[0])
        list.append(f[0])
    ##print(list)
    for k in list:
        rating=float(k[3])
        r=rating/20
        rate.append(r)
    d=(zip(list,rate))
    data=set(d)

    ##print("data",data)



    if(a==[]):

        msg="you have not added any application at your profile yet...!!"
        return render(request,'added_app.html',{'msg':msg})

    else:
        return render(request,'added_app.html',{'list':data})

def added_web(request):
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678')
    cursor = conn.cursor()
    lid=request.session.get('lid')
    q="select web_id from user_website WHERE user_id='%d'"%(lid)
    cursor.execute(q)
    a=cursor.fetchall()
    list=[]
    for i in a:
        a_id=i[0]
        query="select * from web where web_id='%d'"%(a_id)
        cursor.execute(query)
        f=cursor.fetchall()
        ##print(f[0])
        list.append(f[0])

    if(a==[]):

        msg="you have not added any website at your profile yet...!!"
        return render(request,'addedweb.html',{'msg':msg})

    else:
        return render(request,'addedweb.html',{'web':list})

def added_soft(request):
    conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                                   password='12345678')
    cursor = conn.cursor()
    lid=request.session.get('lid')
    q="select soft_id from user_software WHERE user_id='%d'"%(lid)
    cursor.execute(q)
    a=cursor.fetchall()
    list=[]
    for i in a:
        a_id=i[0]
        query="select * from new_software where new_software_id='%d'"%(a_id)
        cursor.execute(query)
        f=cursor.fetchall()
        ##print(f[0])
        list.append(f[0])


    if(a==[]):

        msg="you have not added any software at your profile yet...!!"
        return render(request,'addedsoftware.html',{'msg':msg})

    else:
        return render(request,'addedsoftware.html',{'soft':list})





def new(request):
    option=request.GET.get('guest')
    if(option=='New Application'):
        return new_application(request)
    if(option=='New Website'):
        return render(request,'new_website_categories.html')
    if(option=='New Software'):
        return new_software(request)


def highlights(request):

    q="Select * from app_details order by count desc"
    cursor.execute(q)
    a=cursor.fetchall()
    #print(a)
    count = 0
    ##print(a[0])
    rate = []
    r = 0
    for i in a:
        # rating=a[0]
        # #print(rating)
        rating = float(i[3])
        ##print("rating",rating)
        r = rating / 20
        rate.append(r)
    list = (zip(a, rate))
    l = set(list)
    #print(l)
    count = 0
    newlist = []
    for k in l:
        count = count + 1
        if (count <= 8):
            #print(count)
            newlist.append(k)
    #print(newlist)
    q2="Select * from web order by count desc"
    cursor.execute(q2)
    c = cursor.fetchall()
    #print(c)
    count = 0
    c1 = []
    for l in c:
        count = count + 1
        if (count <= 8):
            c1.append(l)

    q="Select * from new_software order by count desc"
    cursor.execute(q)
    m=cursor.fetchall()
    #print(m)
    count = 0
    soft = []
    for l in m:
        ##print(l)
        count = count + 1
        if (count <= 8):
            ##print(count)
            soft.append(l)
            ##print(soft)


    return render(request,'highlights.html',{'list':newlist,'web':c1,'soft':soft})



def app_highlights(request):
    q="Select * from app_details order by count desc"
    cursor.execute(q)
    a=cursor.fetchall()
    #print(a)
    count = 0
    ##print(a[0])
    rate = []
    r = 0
    for i in a:
        # rating=a[0]
        # #print(rating)
        rating = float(i[3])
        ##print("rating",rating)
        r = rating / 20
        rate.append(r)
    list = (zip(a, rate))
    l = set(list)
    #print(l)
    return render(request,'highlightsapp.html',{'list':l})


def web_highlights(request):
    q2="Select * from web order by count desc"
    cursor.execute(q2)
    c = cursor.fetchall()
    #print(c)

    return render(request,'highlightweb.html',{'web':c})

def soft_highlights(request):
    q="Select * from new_software order by count desc"
    cursor.execute(q)
    m=cursor.fetchall()
    #print(m)
    return render(request,'highlightsoftware.html',{'soft':m})

def highlights_nevigation(request):


    option=request.GET.get('guest')
    if(option=='Highlight App'):
        return app_highlights(request)
    if(option=='Highlight Web'):
       return web_highlights(request)
    if(option=='Highlight Soft'):
        return soft_highlights(request)


def added_nevigation(request):

    option=request.GET.get('guest')
    if(option=='Added App'):
        return added_app(request)
    if(option=='Added Web'):
       return added_web(request)
    if(option=='Added Soft'):
        return added_soft(request)
def recommend_app(app):
    search_term=app
    app_name = play_scraper.search(search_term, page=1)
    app_search = app_name[0]
    title = app_search['title']
    if (title is not None):
        #print("title", title)
        query5 = "select * from app_details where title='%s'" % (title)
        #print(search_term)
        cursor.execute(query5)
        a = cursor.fetchall()
        #print("ac", a)

        if (a == []):
            #print("hello")
            #print(search_term)
            app_name = play_scraper.search(search_term, page=1)
            app_search = app_name[0]
            title=app_search['title']
            package=app_search['app_id']
            url=app_search['url']
            developer=app_search['developer']
            rating=app_search['score']
            per_rating = float(rating) * 20
            per_rating = round(per_rating, 2)
            icon=app_search['icon']
            url1="https://play.google.com/store/apps/details?id="+package+""
            html = urlopen(url)
            soup = BeautifulSoup(html, 'lxml')
            type(soup)
            a=soup.find_all('span')
            count=0
            for i in range(len(a)):
                count=count+1
                x=a[i].text.strip()
                if x==title:
                    index=i
                    category=a[int(index)+int(2)].text.strip()
                    no_of_rating=a[int(index)+int(3)].text.strip()

            div=soup.find_all('span',class_='htlgb')
            list1=[]
            for j in div:
                list1.append(j.text.strip())
            last_updated=list1[0]
            size=list1[2]
            no_of_download=list1[4]
            current_version=list1[6]
            description=soup.find_all('div',class_='DWPxHb')
            list=[]
            for i in description:
                list.append(i.text.strip())
            description=list[0]
            strip_special_chars = re.compile("[^A-Za-z0-9 ]+")
            string = description.lower().replace("<br />", " ")
            description = re.sub(strip_special_chars, "", description.lower())
            img=soup.find_all('img',class_='T75of TJlTvc')
            img1=[]
            im=[]
            for i in img:

                ss=i.get('data-srcset')
                img1.append(ss)
            for j in img1:
                if(j is not None):
                     ss1=j.split(" ",2)
                     im.append(ss1[0])
            count=count+1
            img2=[]
            for j in img:
                img2.append(j.get('src'))
            im.append(img2[0])
            im.append(img2[1])
            content_rating1="0"
            price="0"
            query = "insert into app_details(package,icon,rating,content_rating,description,current_version,developer,price,installs,title,download_link,updated,category,app_size,app_category,app_like,app_dislike,count) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%d','%d','%d')" % (
                package, icon, per_rating, content_rating1, description, current_version, developer, price,
                no_of_download,
                title,
                url, last_updated, category, size, 'all', 0, 0,1)
            #print("query",query)
            cursor.execute(query)
            conn.commit()
            app_id = int(cursor.lastrowid)
            #print("app_id",app_id)


            for i in im:
                #print(i)
                #print(app_id)
                screenshots1 = i
                query1 = "insert into app_screenshots(screenshot,app_id) VALUES ('%s','%d')" % (i, app_id)
                #print(query1)
                cursor.execute(query1)
                conn.commit()

            URL1 = "https://data.42matters.com/api/v3.0/android/apps/topics.json?p=" + package + "&access_token=f179acc1234fe6a99bb429b1682595bbac44be22"
            response = requests.get(URL1)
            #print(response.text)
            json_data = json.loads(response.text)
            reviews = json_data
            #print("reviews",reviews)
            if(reviews is not None):
                number_topics = reviews['number_topics']
                total_reviews = reviews['total_reviews']
                number_ratings = reviews['number_ratings']
                query3 = "insert into app_reviews_result(nooftopic,noofreviews,noofrating,app_id3) VALUES ('%d','%d','%d','%d')" % (
                    number_topics, total_reviews, number_ratings, app_id)
                cursor.execute(query3)
                conn.commit()
                topic = reviews['topics']
                rrid = int(cursor.lastrowid)

                for i in topic:
                    index = i
                    topic_name = i['topic_name']
                    no_of_reviews = i['reviews']
                    positive = i['positive']
                    per_positive = float(positive) * 100
                    per_positive = round(per_positive, 2)
                    negative = i['negative']
                    per_negative = float(negative) * 100
                    per_negative = round(per_negative, 2)
                    average_rating_of_topic = i['average_rating']
                    per_average_rating_of_topic = float(average_rating_of_topic) * 20
                    per_average_rating_of_topic = round(per_average_rating_of_topic, 2)

                    query4 = "insert into reviews_topic(topic_name,noofreviews,poscomment,negcomment,avgrating,rrid1) VALUES ('%s','%s','%s','%s','%s','%s')" % (
                        topic_name, no_of_reviews, per_positive, per_negative, per_average_rating_of_topic, rrid)
                    cursor.execute(query4)
                    conn.commit()
            else:
                number_topics = 'Not Available'
                total_reviews = 'Not Available'
                number_ratings = 'Not Available'
                query3 = "insert into app_reviews_result(nooftopic,noofreviews,noofrating,app_id3) VALUES ('%d','%d','%d','%d')" % (
                    number_topics, total_reviews, number_ratings, app_id)
                cursor.execute(query3)
                conn.commit()
                rrid = int(cursor.lastrowid)
                topic_name='Not Available'
                no_of_reviews='Not Available'
                per_positive='Not Available'
                per_negative='Not Available'
                per_average_rating_of_topic='Not Available'

                query4 = "insert into reviews_topic(topic_name,noofreviews,poscomment,negcomment,avgrating,rrid1) VALUES ('%s','%s','%s','%s','%s','%s')" % (
                    topic_name, no_of_reviews, per_positive, per_negative, per_average_rating_of_topic, rrid)
                cursor.execute(query4)
                conn.commit()

        else:
            print("already presnt in database")
    else:
        print("not available on playstore")

def trending_nevigation(request):

    option=request.GET.get('guest')
    if(option=='Trending App'):
        return trending_application(request)
    if(option=='Trending Website'):
       return website(request)
    if(option=='Trending Software'):
        return trending_software(request)
def dashboar_navigation(request):

    option=request.GET.get('guest')
    if(option=='Application'):
        return trending_application(request)
    if(option=='Website'):
       return website(request)
    if(option=='Software'):
        return trending_software(request)



def recommendation(request):
    if (request.session.get('lid') is not None):
        conn = mysql.connector.connect(host='localhost', database='applications_data', user='root',
                               password='12345678'
                               , auth_plugin='mysql_native_password')
        cursor = conn.cursor()

        lid=request.session.get('lid')
        q="select * from registration where lid='%d'"%(lid)
        cursor.execute(q)
        a=cursor.fetchone()
        ##print("value of a",a)

        if(a[9]=='accepted'):
            age=a[2]
            age=age.lower()
            gender =a[3]
            gender=gender.lower()
            education=a[4]
            education=education.lower()
            #print("edu",education)
            q1="select * from user_interest where rid='%d'"%(a[0])
            cursor.execute(q1)
            interest=cursor.fetchall()
            ##print(interest)
            interest_list=[]
            for i in interest:
                interest_list.append(i[1])



            ##print(interest_list)
            if(interest_list[0] is not None):

                interest1 =interest_list[0]
                interest1=interest1.lower()
            if(interest_list[1] is not None):
                interest2 =interest_list[1]
                interest2=interest2.lower()
            else:
                interest2 =''
                interest2=interest2.lower()
            if(interest_list[2] is not None):
                interest3 =interest_list[2]
                interest3=interest3.lower()
            else:
                interest3 =interest_list[2]
                interest3=interest3.lower()

            # if(interest_list[3] is not None):
            #     interest4 =interest_list[3]
            #     interest4=interest4.lower()
            # else:
            #     interest4 =''
            #     interest4=interest4.lower()
            # if(interest_list[4] is not None):
            #     interest5 =interest_list[4]
            #     interest5=interest5.lower()
            # else:
            #     interest5 =interest_list[4]
            #     interest5=interest5.lower()


            list1=[]
            list2=[]
            list3=[]
            list4=[]
            q2="select *  from recommendation_data where age='%s' "%(age)
            cursor.execute(q2)
            re_data = cursor.fetchall()
            for i in re_data:
                if(i[1]==gender):
                    list1.append(i)


            for j in list1:
                if(j[8]==education):
                    list2.append(j)
            ##print(list2)
            for k in list2:
                if(k[2]==interest1 or k[3]==interest1 or k[4]==interest1 or k[5]==interest1 or k[6]==interest1):
                    list3.append(k)
            ##print(list3)
            ##print(len(list3))
            # for p in list3:
            #     if(p[2]==interest2 or p[3]==interest2 or p[4]==interest2 or p[5]==interest2 or p[6]==interest2):
            #         list4.append(p)
            #print(list4)
            #print(len(list4))




            ##print(len(list1))

            # for n in list1:
            #      ##print(n)
            #      if(n[2]==interest1 or n[3]==interest1 or n[4]==interest1 or n[5]==interest1 or n[6]==interest1):
            #             list2.append(n)
            #
            # #print("list2",list2)
            # for p in list2:
            #
            #      if(p[2]==interest2 or p[3]==interest2 or p[4]==interest2 or p[5]==interest2 or p[6]==interest2):
            #             list3.append(n)
                 # if(n[2]==interest3 or n[3]==interest3 or n[4]==interest3 or n[5]==interest3 or n[6]==interest3):
                 #        list2.append(n)
                 # if(n[2]==interest4 or n[3]==interest4 or n[4]==interest4 or n[5]==interest4 or n[6]==interest4):
                 #        list2.append(n)
                 #
                 # if(n[2]==interest5 or n[3]==interest5 or n[4]==interest5 or n[5]==interest5 or n[6]==interest5):
                 #        list2.append(n)
            # list_based_on_education=[]
            #
            # for w in list3:
            #     ##print("value of w ",w)
            #     if(w[8]== education ):
            #         list_based_on_education.append(w)
            # #print("educatio",list_based_on_education)
            list8=[]
            for k in list3:
                if k[7] in list8:
                    pass

                else:
                    list8.append(k[7])
            #print(list8)
            #print(len(list8))

            # google_app=[]
            # for name in list8:
            #     ##print(name)
            #     if(name == 'bank application'):
            #         name ='phonepe'
            #     app_name = play_scraper.search(name, page=1)
            #     app_search = app_name[0]
            #     title = app_search['title']
            #
            #
            #     query = "select * from app_details where title='%s'" % (title)
            #     cursor.execute(query)
            #     a = cursor.fetchall()
            #     # #print(a)
            #     # count = 0
            #     #print(a[0])
            #     google_app.append(a[0])
            #
            # rate = []
            # r = 0
            # for i in google_app:
            #     # rating=a[0]
            #     # #print(rating)
            #     rating = float(i[3])
            #     ##print("rating",rating)
            #     r = rating / 20
            #     rate.append(r)
            # list = (zip(google_app , rate))
            # l = set(list)
            google_app=[]
            count =0
            for name in list8:
                if(count<11):
                    print("name",name)
                    if(name == 'bank application'):
                        name ='phonepe'
                    app_name = play_scraper.search(name, page=1)
                    app_search = app_name[0]
                    title = app_search['title']
                    count =count+1


                    query = "select * from app_details where title='%s'" % (title)
                    cursor.execute(query)
                    rcatchapp = cursor.fetchall()
                    print(rcatchapp)

                    # #print(a)
                    # count = 0
                    #print(a[0])
                    print("catchapp",rcatchapp[0])
                    if(rcatchapp[0]!= []):
                        pass
                    else:
                        google_app.append(rcatchapp[0])

                rate = []
                r = 0
                for i in google_app:
                    # rating=a[0]
                    # ##print(rating)
                    rating = float(i[3])
                    ###print("rating",rating)
                    r = rating / 20
                    rate.append(r)
                list = (zip(google_app , rate))
                l = set(list)
                ##print("value of l",l)

            #print("value of l",l)
            return render(request,'app_recommendation.html',{'app':l})
            print(google_app)



        else:
            recommend_msg='''Dear user, As you choose other profession or educational backgrond at your registration time so we are not able to recommend you application,website and software because we have not enough data at this time but you can use other functionality of CatchApp.
            Sorry for inconvenience...'''
            return render(request,'app_recommendation.html',{'recommend_msg',recommend_msg})



    else:
        return render(request,'login.html')

def fdbk_data(request):
    name=request.POST.get('name')
    subject=request.POST.get('subject')
    email = request.POST.get('email')
    feedback = request.POST.get('feedback')

    q="insert into feedback(user_name,email,subject,message) VALUE ('%s','%s','%s','%s')  "%(name,subject,email,feedback)
    cursor.execute(q)
    conn.commit()


    feedback="Thank You For Your Feedback !!!"
    return render(request,'feedback.html',{'feedback':feedback})





