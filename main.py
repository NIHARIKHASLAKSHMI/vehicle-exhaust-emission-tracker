from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
import numpy as np 
import pandas as pd
import matplotlib.pyplot as plt
import os
import base64
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
from math import pi
import json
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser

import mysql.connector


import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
from plotly.subplots import make_subplots

import plotly.express as px
from plotly.offline import init_notebook_mode, iplot 
import plotly.graph_objs as go
import plotly.offline as py
from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
import chart_studio.plotly as py

import matplotlib.colors as mcolors
import plotly.express as px
import plotly.graph_objs as go
import plotly.figure_factory as ff
cnf, dth, rec, act,wth,sth = '#393e46', '#ff2e63', '#21bf73', '#fe9801','#456fe3','#78ffee' 

import glob
from sklearn.preprocessing import LabelEncoder, StandardScaler


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="vehicle_exhaust"
)


app = Flask(__name__)
app.secret_key = 'abcdef'
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""
   
    return render_template('index.html',msg=msg)

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        lat=request.form['lat']
        lon=request.form['lon']

        loc=lat+", "+lon
        ff=open("static/loc.txt","w")
        ff.write(loc)
        ff.close()

        
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM ve_admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('admin'))
        else:
            msg = 'Incorrect username/password!'

        
    
    return render_template('login.html',msg=msg)

@app.route('/login_cpcb', methods=['GET', 'POST'])
def login_cpcb():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM ve_cpcb WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            ff=open("static/cpcb.txt","w")
            ff.write(uname)
            ff.close()
            
            session['username'] = uname
            return redirect(url_for('cpcb_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_cpcb.html',msg=msg)

@app.route('/login_rto', methods=['GET', 'POST'])
def login_rto():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM ve_rto WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('add_vo'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_rto.html',msg=msg)

@app.route('/login_vo', methods=['GET', 'POST'])
def login_vo():
    msg=""

    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM ve_register WHERE uname = %s AND pass = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            session['username'] = uname
            return redirect(url_for('vo_home'))
        else:
            msg = 'Incorrect username/password!'
    return render_template('login_vo.html',msg=msg)

@app.route('/add_rto', methods=['GET', 'POST'])
def add_rto():
    msg=""
    mess=""
    email=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM ve_rto")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    
        
    if request.method=='POST':
        
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        location=request.form['location']

        uname="R"+str(maxid)
        rn=randint(1000,9999)
        pass1=str(rn)

        mess="Dear "+name+", RTO Admin ID:"+uname+", Password:"+pass1
        
        sql = "INSERT INTO ve_rto(id,name,mobile,email,location,uname,pass) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,name,mobile,email,location,uname,pass1)
        mycursor.execute(sql, val)
        mydb.commit()            
        print(mycursor.rowcount, "Registered Success")
        msg="success"
        #return redirect(url_for('add_rto',act='1'))

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ve_rto where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_rto'))
        

    mycursor.execute("SELECT * FROM ve_rto")
    data = mycursor.fetchall()

    return render_template('web/add_rto.html',msg=msg,act=act,data=data,mess=mess,email=email)



@app.route('/add_cpcb', methods=['GET', 'POST'])
def add_cpcb():
    msg=""
    mess=""
    email=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM ve_cpcb")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    
        
    if request.method=='POST':
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        
        
        area=request.form['area']
        city=request.form['city']

        uname="T"+str(maxid)
        pass1="1234"


        mess="Dear "+name+", CPCB ID:"+uname+", Password:"+pass1
        
        sql = "INSERT INTO ve_cpcb(id,name,mobile,email,area,city,uname,pass) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (maxid,name,mobile,email,area,city,uname,pass1)
        mycursor.execute(sql, val)
        mydb.commit()            
        
        msg="success"
      

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ve_cpcb where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_tc'))
        

    mycursor.execute("SELECT * FROM ve_cpcb")
    data = mycursor.fetchall()

    return render_template('web/add_cpcb.html',msg=msg,act=act,data=data,mess=mess,email=email)


@app.route('/add_vo', methods=['GET', 'POST'])
def add_vo():
    msg=""
    fn=""
    email=""
    mess=""
    vid=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT max(id)+1 FROM ve_register")
    maxid = mycursor.fetchone()[0]
    if maxid is None:
        maxid=1
    
        
    if request.method=='POST':
        
        name=request.form['name']
        vno=request.form['vno']
        gender=request.form['gender']
        dob=request.form['dob']
        address=request.form['address']
        mobile=request.form['mobile']
        email=request.form['email']
        rdate=request.form['rdate']
        

        vno=request.form['vno']
        vcolor=request.form['vcolor']
        vname=request.form['vname']
        vmodel=request.form['vmodel']
        vtype=request.form['vtype']

        mycursor.execute("SELECT count(*) FROM ve_register where vno=%s",(vno,))
        cnt = mycursor.fetchone()[0]
        if cnt==0:
    
            fuel_type=request.form['fuel_type']
            file = request.files['file']
            file2 = request.files['file2']

            

            uname="V"+str(maxid)
            vid=uname
            rn=randint(1000,9999)
            pass1=str(rn)

            rn2=randint(1000,5000)
            rn3=randint(5001,9000)

            eeid="EI"+str(maxid)+"-"+str(rn2)+"-"+str(rn3)

            filename=file.filename
            photo="C"+str(maxid)+filename
            file.save(os.path.join("static/vehicle", photo))

            filename2=file2.filename
            dno="D"+str(maxid)+filename2
            file2.save(os.path.join("static/vehicle", dno))


            mess="Dear "+name+", Vehicle Owner ID:"+uname+", Password:"+pass1

            
            sql = "INSERT INTO ve_register(id,name,vno,filename,gender,dob,address,mobile,email,register_date,vtype,vmodel,vcolor,uname,pass,vname,driving,fuel_type,eei_device) VALUES (%s,%s,%s,%s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s)"
            val = (maxid,name,vno,photo,gender,dob,address,mobile,email,rdate,vtype,vmodel,vcolor,uname,pass1,vname,dno,fuel_type,eeid)
            mycursor.execute(sql, val)
            mydb.commit()            
            print(mycursor.rowcount, "Registered Success")
            msg="success"
        else:
            msg="fail"
        #return redirect(url_for('add_info',act='1'))

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ve_register where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('add_vo'))
        

    mycursor.execute("SELECT * FROM ve_register")
    data = mycursor.fetchall()

    return render_template('web/add_vo.html',msg=msg,act=act,data=data,email=email,mess=mess,vid=vid)

@app.route('/edit_vo', methods=['GET', 'POST'])
def edit_vo():
    msg=""
    vid=request.args.get("vid")
    fn=""
    email=""
    mess=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        
        name=request.form['name']
        vno=request.form['vno']
        gender=request.form['gender']
        dob=request.form['dob']
        address=request.form['address']
        mobile=request.form['mobile']
        email=request.form['email']
        rdate=request.form['rdate']
        
        vcolor=request.form['vcolor']
        vname=request.form['vname']
        vmodel=request.form['vmodel']
        vtype=request.form['vtype']
        fuel_type=request.form['fuel_type']

        mycursor.execute("update ve_register set name=%s,vno=%s,gender=%s,dob=%s,address=%s,mobile=%s,email=%s,register_date=%s,vcolor=%s,vname=%s,vmodel=%s,vtype=%s,fuel_type=%s where id=%s",(name,vno,gender,dob,address,mobile,email,rdate,vcolor,vname,vmodel,vtype,fuel_type,vid))
        mydb.commit()
        msg="success"
        
       

    mycursor.execute("SELECT * FROM ve_register where id=%s",(vid,))
    data = mycursor.fetchone()

    return render_template('web/edit_vo.html',msg=msg,act=act,data=data,email=email,mess=mess)

@app.route('/edit_cpcb', methods=['GET', 'POST'])
def edit_cpcb():
    msg=""
    vid=request.args.get("vid")
    fn=""
    email=""
    mess=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        area=request.form['area']
        
        city=request.form['city']
       
        mycursor.execute("update ve_cpcb set name=%s,mobile=%s,email=%s,area=%s,city=%s where id=%s",(name,mobile,email,area,city,vid))
        mydb.commit()
        msg="success"
        
       

    mycursor.execute("SELECT * FROM ve_cpcb where id=%s",(vid,))
    data = mycursor.fetchone()

    return render_template('web/edit_cpcb.html',msg=msg,act=act,data=data)


@app.route('/edit_rto', methods=['GET', 'POST'])
def edit_rto():
    msg=""
    vid=request.args.get("vid")
    fn=""
    email=""
    mess=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
    
    if request.method=='POST':
        
        name=request.form['name']
        mobile=request.form['mobile']
        email=request.form['email']
        location=request.form['location']
    
       
        mycursor.execute("update ve_rto set name=%s,mobile=%s,email=%s,location=%s where id=%s",(name,mobile,email,location,vid))
        mydb.commit()
        msg="success"
        
       

    mycursor.execute("SELECT * FROM ve_rto where id=%s",(vid,))
    data = mycursor.fetchone()

    return render_template('web/edit_rto.html',msg=msg,act=act,data=data)



@app.route('/view_vo', methods=['GET', 'POST'])
def view_vo():
    msg=""
    fn=""
    
    act=request.args.get("act")
    mycursor = mydb.cursor()

    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from ve_register where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('view_vo'))

    
    mycursor.execute("SELECT * FROM ve_register order by id desc")
    data = mycursor.fetchall()

    return render_template('web/view_vo.html',msg=msg,act=act,data=data)

@app.route('/track', methods=['GET', 'POST'])
def track():
    msg=""
    mycursor = mydb.cursor()

    mycursor.execute("update ve_vehicle_data set status=1")
    mydb.commit()

    mycursor.execute("update ve_register set service_st=0 where service_st=1")
    mydb.commit()

    ff=open("static/loc.txt","r")
    loc=ff.read()
    ff.close()

    return render_template('web/track.html',msg=msg,loc=loc)

@app.route('/track1', methods=['GET', 'POST'])
def track1():
    msg=""
    data=[]
    act=request.args.get("act")
    mycursor = mydb.cursor()
    mycursor.execute("SELECT count(*) FROM ve_register where ban_st=0 order by rand()")
    cnt = mycursor.fetchone()[0]
    
    mycursor.execute("SELECT * FROM ve_register where ban_st=0 order by rand()")
    dd = mycursor.fetchall()

    rn=randint(1,cnt)
    print(rn)
    i=1
    dt=[]
    for d1 in dd:
        
        if i<=rn:
            mycursor.execute("SELECT * FROM ve_register where id=%s",(d1[0],))
            d2 = mycursor.fetchone()

            vt=d2[10]
            vv=""
            if vt=="Car":
                rn2=randint(1,3)
                vv="c"+str(rn2)+".png"
            else:
                if vt=="Bus":
                    vv="c5.png"
                elif vt=="Van":
                    vv="c4.png"
                else:
                    vv="c6.png"
            val=str(d2[0])+"|"+vv
            dt.append(val)
            data.append(vv)
        
        i+=1

    dat=",".join(dt)
    ff=open("static/det.txt","w")
    ff.write(dat)
    ff.close()

    print(data)


    
    

    return render_template('web/track1.html',msg=msg,act=act,data=data)

@app.route('/track2', methods=['GET', 'POST'])
def track2():
    msg=""
    data=[]
    act=request.args.get("act")

    ff=open("static/det.txt","r")
    dat=ff.read()
    ff.close()

    d1=dat.split(",")

    for d11 in d1:
        d2=d11.split("|")
        data.append(d2[1])

    return render_template('web/track2.html',msg=msg,act=act,data=data)

@app.route('/track3', methods=['GET', 'POST'])
def track3():
    msg=""
    act=request.args.get("act")
    return render_template('web/track3.html',msg=msg,act=act)




@app.route('/cpcb_home', methods=['GET', 'POST'])
def cpcb_home():
    msg=""
    uname=""
    photo=""
    st=""
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']

    mycursor=mydb.cursor()
    mycursor.execute("SELECT * FROM ve_cpcb where uname=%s",(uname,))
    rs = mycursor.fetchone()

    
    mycursor.execute("SELECT * FROM ve_vehicle_data where status=2 order by id desc")
    data = mycursor.fetchall()

    
    return render_template('web/cpcb_home.html',msg=msg,rs=rs,data=data)

@app.route('/vo_home', methods=['GET', 'POST'])
def vo_home():
    msg=""
    uname=""
    photo=""
    st=""
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']

    mycursor=mydb.cursor()
    mycursor.execute("SELECT * FROM ve_register where uname=%s",(uname,))
    rs = mycursor.fetchone()

    return render_template('web/vo_home.html',msg=msg,rs=rs)

@app.route('/vo_eei', methods=['GET', 'POST'])
def vo_eei():
    msg=""
    fn=""
    uname=""
    act=request.args.get("act")
    if 'username' in session:
        uname = session['username']
    mycursor = mydb.cursor()

    
    mycursor.execute("SELECT * FROM ve_register where uname=%s",(uname,))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM ve_vehicle_data where owner=%s",(uname,))
    data1 = mycursor.fetchall()

    if act=="yes":
        mycursor.execute("update ve_register set service_st=0,status='' where uname=%s",(uname,))
        mydb.commit()
        msg="ok"

    return render_template('web/vo_eei.html',msg=msg,act=act,data=data,data1=data1)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    uname=""
    msg=""
    act = request.args.get('act')
    
    if 'username' in session:
        uname = session['username']

    
    
    return render_template('web/admin.html')

@app.route('/process1', methods=['GET', 'POST'])
def process1():
    uname=""
    msg=""
    file_arr=[]
    for dirname, _, filenames in os.walk('dataset'):
        for filename in filenames:
            #print(os.path.join(dirname, filename))
            file_arr.append(filename)
           
    path='dataset/'
    city_day=pd.read_csv(path+'city_day.csv')
    
    dat1=city_day.head(100)
    ##
    data1=[]
    for ss1 in dat1.values:
        data1.append(ss1)
    ##
    dat2=city_day.shape
    
    dat3=city_day.head()
    ##
    data3=[]
    for ss3 in dat3.values:
        data3.append(ss3)
    ##
    dat4=city_day.shape

    
    return render_template('web/process1.html',file_arr=file_arr,data1=data1,dat2=dat2,data3=data3,dat4=dat4)



def Missing (X):
    total = X.isnull().sum().sort_values(ascending = False)
    percent = round(X.isnull().sum().sort_values(ascending = False)/len(X)*100, 2)
    missing = pd.concat([total, percent], axis = 1,keys= ['Total', 'Percent'])
    
    return(missing) 

def SideSide(*args):
    html_str=''
    dt=[]
    for df in args:
        html_str+=df.to_html()
        
        
   
    
@app.route('/process2', methods=['GET', 'POST'])
def process2():
    msg=""
    data4=[]
    mem=0
    cnt=0
    cols=0
    rows=0
    rowsn=0
    nullcount=0
    filename = 'dataset/city_day.csv'
    data1 = pd.read_csv(filename)
    data2 = list(data1.values.flatten())

    

        
    cname=[]
    data=[]
    dtype=[]
    dtt=[]
    nv=[]
    i=0
    
    sd=len(data1)
    rows=len(data1.values)
    
    print(data1.columns)
    col=data1.columns
    #print(data1[0])
    for ss in data1.values:
        cnt=len(ss)
        i=0
        x=0
        
        while i<cnt:
            if pd.isnull(ss[i]):
                ss[i]=-1
                nullcount+=1
                x+=1
            i+=1
        if x>0:
            if rowsn<100:
                data4.append(ss)
            rowsn+=1
        

    i=0
    while i<cnt:
        j=0
        x=0
        for rr in data1.values:
            dt=type(rr[i])
            if rr[i]!="":
                x+=1
            
            j+=1
        dtt.append(dt)
        nv.append(str(x))
        
        i+=1

    arr1=np.array(col)
    arr2=np.array(nv)
    data3=np.vstack((arr1, arr2))
    rows=rows-rowsn

    arr3=np.array(data3)
    arr4=np.array(dtt)
    
    data=np.vstack((arr3, arr4))
   
    #print(data)
    cols=cnt
    mem=float(rows)*0.75

    #if request.method=='POST':
    #    return redirect(url_for('feature_ext'))
    
    return render_template('web/process2.html',data=data,data4=data4, msg=msg, rows=rows,nullcount=nullcount, cols=cols, dtype=dtype, mem=mem)


#Feature Extraction
@app.route('/calculate_EEI', methods=['GET', 'POST'])
def calculate_EEI():
    # Missing values
    def missing_values(df):
            # Total missing values
            mis_val = df.isnull().sum()
            
            # Percentage of missing values
            mis_val_percent = 100 * df.isnull().sum() / len(df)
            
            # Make a table with the results
            mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
            
            # Rename the columns
            mis_val_table_ren_columns = mis_val_table.rename(columns = {0 : 'Missing Values', 1 : '% of Total Values'})
            
            # Sort the table by percentage of missing descending
            mis_val_table_ren_columns = mis_val_table_ren_columns[mis_val_table_ren_columns.iloc[:,1] != 0].sort_values('% of Total Values', ascending=False).round(1)
            
            # Print some summary information
            #print ("Your selected dataframe has " + str(df.shape[1]) + " columns.\n"+"There are " + str(mis_val_table_ren_columns.shape[0]) +" columns that have missing values.")
            

            return mis_val_table_ren_columns.style.background_gradient(cmap='Reds')

    df_city_day     = pd.read_csv("static/js/city_day.csv")

    dat1=df_city_day.head(100)
    #print(dat1)
    data1=[]
    #for ss1 in dat1.values:
    #    data1.append(ss1)
    cnt=0
    data=[]
    rows=0
    rowsn=0
    nullcount=0
    cols=0
    
    for ss in dat1.values:
        cnt=len(ss)
        i=0
        x=0
        while i<cnt:
            if pd.isnull(ss[i]):
                nullcount+=1
                x+=1
            i+=1
        if x>0:
            rowsn+=1
        else:

           
            data1.append(ss)
    
    
    np.unique(df_city_day['EEI_Bucket'][df_city_day['EEI_Bucket'].notnull()].values)
    dat2=df_city_day.head()
    data2=[]
    for ss2 in dat2.values:
        data2.append(ss2)


    ## PM2.5 Sub-Index calculation
    def get_PM25_subindex(x):
        if x <= 30:
            return x * 50 / 30
        elif x <= 60:
            return 50 + (x - 30) * 50 / 30
        elif x <= 90:
            return 100 + (x - 60) * 100 / 30
        elif x <= 120:
            return 200 + (x - 90) * 100 / 30
        elif x <= 250:
            return 300 + (x - 120) * 100 / 130
        elif x > 250:
            return 400 + (x - 250) * 100 / 130
        else:
            return 0

    #df["PM2.5_SubIndex"] = df["PM2.5_24hr_avg"].apply(lambda x: get_PM25_subindex(x))
    ## PM10 Sub-Index calculation
    def get_PM10_subindex(x):
        if x <= 50:
            #return x * 50/ 50
            return x
        elif x <= 100:
            #return  50 + (x -  50) *  50 / 50
            return x
        elif x <= 250:
            return 100 + (x - 100) * 100 / 150
        elif x <= 350:
            return 200 + (x - 250)
        elif x <= 430:
            return 300 + (x - 350) * 100 / 80
        elif x > 430:
            return 400 + (x - 430) * 100 / 80
        else:
            return 0

   
    def get_SO2_subindex(x):
        if x <= 40:
            return x * 50 / 40
        elif x <= 80:
            return 50 + (x - 40) * 50 / 40
        elif x <= 380:
            return 100 + (x - 80) * 100 / 300
        elif x <= 800:
            return 200 + (x - 380) * 100 / 420
        elif x <= 1600:
            return 300 + (x - 800) * 100 / 800
        elif x > 1600:
            return 400 + (x - 1600) * 100 / 800
        else:
            return 0

    #df["SO2_SubIndex"] = df["SO2_24hr_avg"].apply(lambda x: get_SO2_subindex(x))

    ## NOx Sub-Index calculation
    def get_NOx_subindex(x):
        if x <= 40:
            return x * 50 / 40
        elif x <= 80:
            return 50 + (x - 40) * 50 / 40
        elif x <= 180:
            return 100 + (x - 80) * 100 / 100
        elif x <= 280:
            return 200 + (x - 180) * 100 / 100
        elif x <= 400:
            return 300 + (x - 280) * 100 / 120
        elif x > 400:
            return 400 + (x - 400) * 100 / 120
        else:
            return 0

    #df["NOx_SubIndex"] = df["NOx_24hr_avg"].apply(lambda x: get_NOx_subindex(x))
    ## NH3 Sub-Index calculation
    def get_NH3_subindex(x):
        if x <= 200:
            return x * 50 / 200
        elif x <= 400:
            return 50 + (x - 200) * 50 / 200
        elif x <= 800:
            return 100 + (x - 400) * 100 / 400
        elif x <= 1200:
            return 200 + (x - 800) * 100 / 400
        elif x <= 1800:
            return 300 + (x - 1200) * 100 / 600
        elif x > 1800:
            return 400 + (x - 1800) * 100 / 600
        else:
            return 0

    #df["NH3_SubIndex"] = df["NH3_24hr_avg"].apply(lambda x: get_NH3_subindex(x))
    ## CO Sub-Index calculation
    def get_CO_subindex(x):
        if x <= 1:
            return x * 50 / 1
        elif x <= 2:
            return 50 + (x - 1) * 50 / 1
        elif x <= 10:
            return 100 + (x - 2) * 100 / 8
        elif x <= 17:
            return 200 + (x - 10) * 100 / 7
        elif x <= 34:
            return 300 + (x - 17) * 100 / 17
        elif x > 34:
            return 400 + (x - 34) * 100 / 17
        else:
            return 0

    #df["CO_SubIndex"] = df["CO_8hr_max"].apply(lambda x: get_CO_subindex(x))
    ## O3 Sub-Index calculation
    def get_O3_subindex(x):
        if x <= 50:
            return x * 50 / 50
        elif x <= 100:
            return 50 + (x - 50) * 50 / 50
        elif x <= 168:
            return 100 + (x - 100) * 100 / 68
        elif x <= 208:
            return 200 + (x - 168) * 100 / 40
        elif x <= 748:
            return 300 + (x - 208) * 100 / 539
        elif x > 748:
            return 400 + (x - 400) * 100 / 539
        else:
            return 0

    
    def get_AQI_bucket(x):
        if x <= 50:
            return "Good"
        elif x <= 100:
            return "Satisfactory"
        elif x <= 200:
            return "Moderate"
        elif x <= 300:
            return "Poor"
        elif x <= 400:
            return "Very Poor"
        elif x > 400:
            return "Severe"
        else:
            return np.NaN

   

   


    return render_template('web/calculate_EEI.html',data1=data1)


##LSTM
def load_data(stock, seq_len):
    amount_of_features = len(stock.columns)
    data = stock.as_matrix() #pd.DataFrame(stock)
    sequence_length = seq_len + 1
    result = []
    for index in range(len(data) - sequence_length):
        result.append(data[index: index + sequence_length])

    result = np.array(result)
    row = round(0.9 * result.shape[0])
    train = result[:int(row), :]
    x_train = train[:, :-1]
    y_train = train[:, -1][:,-1]
    x_test = result[int(row):, :-1]
    y_test = result[int(row):, -1][:,-1]

    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], amount_of_features))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], amount_of_features))  

    return [x_train, y_train, x_test, y_test]

def train(train_iter, dev_iter, test_iter, model, args):
    if args.cuda:
        model.cuda()

    if args.Adam is True:
        print("Adam Training......")
        optimizer = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.init_weight_decay)
    elif args.SGD is True:
        print("SGD Training.......")
        optimizer = torch.optim.SGD(model.parameters(), lr=args.lr, weight_decay=args.init_weight_decay,
                                    momentum=args.momentum_value)
    elif args.Adadelta is True:
        print("Adadelta Training.......")
        optimizer = torch.optim.Adadelta(model.parameters(), lr=args.lr, weight_decay=args.init_weight_decay)

    steps = 0
    model_count = 0
    best_accuracy = Best_Result()
    model.train()
    for epoch in range(1, args.epochs+1):
        steps = 0
        print("\n## The {} Epoch, All {} Epochs ! ##".format(epoch, args.epochs))
        for batch in train_iter:
            feature, target = batch.text, batch.label.data.sub_(1)
            if args.cuda is True:
                feature, target = feature.cuda(), target.cuda()

            target = autograd.Variable(target)  # question 1
            optimizer.zero_grad()
            logit = model(feature)
            loss = F.cross_entropy(logit, target)
            loss.backward()
            if args.init_clip_max_norm is not None:
                utils.clip_grad_norm_(model.parameters(), max_norm=args.init_clip_max_norm)
            optimizer.step()

            steps += 1
            if steps % args.log_interval == 0:
                train_size = len(train_iter.dataset)
                corrects = (torch.max(logit, 1)[1].view(target.size()).data == target.data).sum()
                accuracy = float(corrects)/batch.batch_size * 100.0
                sys.stdout.write(
                    '\rBatch[{}/{}] - loss: {:.6f}  acc: {:.4f}%({}/{})'.format(steps,
                                                                            train_size,
                                                                             loss.item(),
                                                                             accuracy,
                                                                             corrects,
                                                                             batch.batch_size))
            if steps % args.test_interval == 0:
                print("\nDev  Accuracy: ", end="")
                eval(dev_iter, model, args, best_accuracy, epoch, test=False)
                print("Test Accuracy: ", end="")
                eval(test_iter, model, args, best_accuracy, epoch, test=True)
            if steps % args.save_interval == 0:
                if not os.path.isdir(args.save_dir): os.makedirs(args.save_dir)
                save_prefix = os.path.join(args.save_dir, 'snapshot')
                save_path = '{}_steps{}.pt'.format(save_prefix, steps)
                torch.save(model.state_dict(), save_path)
                if os.path.isfile(save_path) and args.rm_model is True:
                    os.remove(save_path)
                model_count += 1
    return model_count


def eval(data_iter, model, args, best_accuracy, epoch, test=False):
    model.eval()
    corrects, avg_loss = 0, 0
    for batch in data_iter:
        feature, target = batch.text, batch.label
        target.data.sub_(1)
        if args.cuda is True:
            feature, target = feature.cuda(), target.cuda()
        logit = model(feature)
        loss = F.cross_entropy(logit, target)

        avg_loss += loss.item()
        corrects += (torch.max(logit, 1)[1].view(target.size()).data == target.data).sum()

    size = len(data_iter.dataset)
    avg_loss = loss.item()/size
    accuracy = float(corrects)/size * 100.0
    model.train()
    print(' Evaluation - loss: {:.6f}  acc: {:.4f}%({}/{}) '.format(avg_loss, accuracy, corrects, size))
    if test is False:
        if accuracy >= best_accuracy.best_dev_accuracy:
            best_accuracy.best_dev_accuracy = accuracy
            best_accuracy.best_epoch = epoch
            best_accuracy.best_test = True
    if test is True and best_accuracy.best_test is True:
        best_accuracy.accuracy = accuracy

    if test is True:
        print("The Current Best Dev Accuracy: {:.4f}, and Test Accuracy is :{:.4f}, locate on {} epoch.\n".format(
            best_accuracy.best_dev_accuracy, best_accuracy.accuracy, best_accuracy.best_epoch))
    if test is True:
        best_accuracy.best_test = False
        
def build_model(layers):
    model = Sequential()

    model.add(LSTM(
        input_dim=layers[0],
        output_dim=layers[1],
        return_sequences=True))
    model.add(Dropout(0.2))

    model.add(LSTM(
        layers[2],
        return_sequences=False))
    model.add(Dropout(0.2))

    model.add(Dense(
        output_dim=layers[2]))
    model.add(Activation("linear"))

    start = time.time()
    model.compile(loss="mse", optimizer="rmsprop",metrics=['accuracy'])
    print("Compilation Time : ", time.time() - start)
    return model

def build_model2(layers):
        d = 0.2
        model = Sequential()
        model.add(LSTM(128, input_shape=(layers[1], layers[0]), return_sequences=True))
        model.add(Dropout(d))
        model.add(LSTM(64, input_shape=(layers[1], layers[0]), return_sequences=False))
        model.add(Dropout(d))
        model.add(Dense(16,init='uniform',activation='relu'))        
        model.add(Dense(1,init='uniform',activation='linear'))
        model.compile(loss='mse',optimizer='adam',metrics=['accuracy'])
        return model



@app.route('/classification', methods=['GET', 'POST'])
def classification():
    
    
    path='static/js/'
    city_day=pd.read_csv(path+'city_day.csv')
    data4=[]
    p1=0
    p2=0
    p3=0
    p4=0
    for ss4 in city_day.values:
        if ss4[14]=="Good":
            p1+=1
        if ss4[14]=="Satisfactory":
            p2+=1
        if ss4[14]=="Poor":
            p3+=1
        if ss4[14]=="Phase out":
            p4+=1
            
        

    
    dat1=city_day.head()
    
    mycursor = mydb.cursor()
    
    
    
    dat2=city_day.shape
    
    dat3=city_day.head()
    
    dat4=city_day.shape


    g2=0
    data44=[p1,p2,p3,p4]
    if p1>p2 and p1>p3 and p1>p4:
        g2=p1
    elif p2>p3 and p2>p4:
        g2=p2
    elif p3>p4:
        g2=p3
    else:
        g2=p4
        
    g2=g2+5
    doc=['Good','Satisfactory','Poor','Phase out']
    
    fig = plt.figure(figsize = (11, 8))
     
    
    c=['green', 'blue','yellow','red']
    plt.bar(doc, data44, color =c,
            width = 0.4)
 

    plt.ylim((1,g2))
    plt.xlabel("EEI Bucket")
    plt.ylabel("Count")
    plt.title("")

    rr=randint(100,999)
    
    plt.xticks(rotation=20)
    plt.savefig('static/graph/graph2.png')
    
    plt.close()
    
    
    
    return render_template('web/classification.html',data44=data44)


def get_EEI_classify(location):
        x=0
        x1=0
        y1=0
        z1=0
        s1=0
        val=[]
        city_hour1=pd.read_csv('dataset/city_day.csv')
        for ks5 in city_hour1.values:
            if ks5[0]==location:
                x1+=1
                if pd.isnull(ks5[14]):
                    y1+=1
                else:
                    s1+=ks5[14]
                    z1+=1

        if z1>0:        
            aqi1=s1/z1
            x=int(aqi1)
            
            if x >30:
                aq="Phase out"
            elif x >20:
                aq="Poor"
            elif x >10:
                aq="Satisfactory"
            elif x <= 300:
                aq="Good"
            
        else:
            x=0
            aq=""

        val.append(x)
        val.append(aq)
        return val



@app.route('/logout')
def logout():
    
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True,host='0.0.0.0', port=5000)
