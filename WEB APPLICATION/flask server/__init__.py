from flask import Blueprint,render_template, flash, redirect, session, url_for, request, g, json, Response
from flask import Flask
import MySQLdb
import string
import random
import checkmailchip
from flask.json import jsonify
import os
from random import randint
import sys
import cv2
import glob
import select
import configf
import face
import base64
from camera import VideoCamera
import json
import subprocess

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

app = Flask(__name__)
app.config.from_object('config')

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)

@app.route("/", subdomain='<var>')
def index(var):
  if var=="www":
        #forward to home page
        return redirect(url_for('profile'))
  else:
      #show no exists
      return render_template('suberror.html')

@app.route('/')
@app.route('/index')
def profile():
  dbql = MySQLdb.connect("localhost","root","bobbyda16","project")
  cursor = dbql.cursor()

  if 'email' not in session:
      return redirect(url_for('signin'))


  msql = """SELECT uid FROM users WHERE uid=%s"""
  cursor.execute(msql,[str(session['email'])])
  checkmail = cursor.rowcount
  if checkmail:
    #find the type of account
    acsql = """SELECT * FROM users WHERE uid=%s"""
    cursor.execute(acsql,[str(session['email'])])
    dataofv = cursor.fetchall()
    for u in dataofv:
        actype = str(u[4])
        acname = str(u[3])
        image = str(u[7])
    if actype=="1":
        #its a company man
        dasql = """SELECT * FROM users WHERE uid=%s"""
        cursor.execute(dasql,[str(session['email'])])
        #extract the data from db
        dataofv = cursor.fetchall()
        statusf = ""
        for u in dataofv:
            recfname = str(u[3])
            companyfname = str(u[5])
            useremail = str(u[1])
            statusf = str(u[6])
            image = str(u[7])
        dcsql = """SELECT * FROM companies"""
        cursor.execute(dcsql)
        datacfv = cursor.fetchall()
        companyfname = ""
        for c in datacfv:
            companyfname = str(c[1])
        dbql.commit()
        dbql.close()
        if statusf == "1":
            #the page will ask the user to verify their account
            return render_template('locked.html',recfname = recfname,companyfname=companyfname,statusf=statusf,actype="company man",useremail=useremail)
        elif statusf == "2":
            #show the user all the options
            return render_template('recdashang.html',name = recfname,cname = companyfname)

    elif actype=="2":
        return render_template('candashang.html', name = acname,image = image)


  else:
    return redirect(url_for('signin'))

@app.route('/canang', methods=['POST'])
def canang():
  dbql = MySQLdb.connect("localhost","root","bobbyda16","project")
  cursor = dbql.cursor()
  if 'email' not in session:
    return redirect(url_for('signin'))
  else:
    if request.method == 'POST':
	data = json.loads(request.data.decode())
    	inamedbcode = data["inamecode"]
	ncsql = """SELECT * FROM invitations WHERE canid=%s"""
    	cursor.execute(ncsql,[str(session['email'])])
    	dataofv = cursor.fetchall()
    	ary = []
    	for da in dataofv:
        	emdict = {}
        	emdict['recid'] = str(da[1])
        	emdict['company'] = str(da[2])
        	emdict['status'] = str(da[4])
        	ary.append(emdict)
    	dbql.commit()
    	dbql.close()
	return jsonify(datajson = ary)

@app.route('/invitecan', methods=['GET', 'POST'])
def invitecan():

  dbql = MySQLdb.connect("localhost","root","bobbyda16","project")
  cursor = dbql.cursor()

  if 'email' not in session:
    return redirect(url_for('signin'))

  if request.method == 'POST':
    data = json.loads(request.data.decode())
    cemaildb = data["cemaildb"]
    mc = data["mc"]

    dbql = MySQLdb.connect("localhost","root","bobbyda16","project")
    cursor = dbql.cursor()
    sql = """SELECT email FROM users WHERE email=%s and type='1'"""
    cursor.execute(sql,[str(cemaildb)])
    check = cursor.rowcount
    if check:
        #mail id already thr so break
        ficheck = 1
        dbql.commit()
        dbql.close()
        return "1"
    else:
      #all clear
      #find the company name
      dasql = """SELECT * FROM users WHERE uid=%s"""
      cursor.execute(dasql,[str(session['email'])])
      #extract the data from db
      dataofv = cursor.fetchall()
      recfname = ""
      companyfname = ""
      statusf = ""
      for u in dataofv:
          recfname = str(u[3])
          companyfname = str(u[5])
          statusf = str(u[6])
      #entry in invitations
      mailid = str(cemaildb)
      mailid = mailid.replace(" ","")
      #find the uid i.e, existing member or not
      fdsql = """SELECT * FROM users WHERE email=%s"""
      cursor.execute(fdsql,[mailid])
      dataofv = cursor.fetchall()
      uidf = ''
      for u in dataofv:
          uidf = str(u[0])
      if uidf:
          #member already existing so just put the old uid
          cansql = """INSERT INTO invitations(recid,companyid,canid,status,nickemail) VALUES(%s,%s,%s,%s,%s)"""
          cursor.execute(cansql,[str(session['email']),companyfname,str(uidf),"1",str(mailid)])
          subject = 'Request for Information'
          mass=str(mailid)
          msgtocom = 'Existing candidate invitation kindly signin http://localhost:5000/signin'
          checkmailchip.startda(subject,mass,msgtocom)
	  dbql.commit()
          dbql.close()
	  return "2"
      else:
          #member is new so leave the canid field empty
          cansql = """INSERT INTO invitations(recid,companyid,status,nickemail) VALUES(%s,%s,%s,%s)"""
          cursor.execute(cansql,[str(session['email']),companyfname,"1",str(mailid)])
          dbql.commit()
          #find the iid of the invitation to send email unilink url
          iisql = """SELECT * FROM invitations WHERE nickemail=%s"""
          cursor.execute(iisql,[str(mailid)])
          dataofv = cursor.fetchall()
          pkvalofinv = ''
          for u in dataofv:
              pkvalofinv = str(u[0])
          #create the url
          unilink1 = id_generator(25)
          #now append the task of the url, here it is veryify company man, he is going to be 1
          unilink2 = id_generator(50)
          #now append the value of task, here it is pkvalofusr
          #now form the super url
          unilink = str(unilink1)+"2"+str(unilink2)+str(pkvalofinv)
          subject = 'Request for Information'
          mass=str(mailid)
          msgtocom = mc+'\nPlease click the following url to accept the invitation and to share your information\n http://localhost:5000/invitationaccept/'+str(unilink)
          checkmailchip.startda(subject,mass,msgtocom)
          dbql.commit()
          dbql.close()
          #flash('You have successfully sent invitaions to all    '+str(msgtocom))
          return "2"

@app.route('/signin', methods=['GET','POST'])
def signin():
  dbql = MySQLdb.connect("localhost","root","bobbyda16","project")
  cursor = dbql.cursor()
  if 'email' in session:
    return redirect(url_for('profile'))

  if request.method == 'POST':
      data = json.loads(request.data.decode())
      usernamedb = data["usernamedb"]
      pwddb = data["pwddb"]
      sql = """SELECT * FROM users WHERE email=%s"""
      #request.form['usernamedb']
      #lemail = self.email.data.lower()
      lemail = str(usernamedb)


      lemail = lemail.replace(" ","")
      cursor.execute(sql,[str(lemail)])
      check = cursor.rowcount
      if check:
        dataofv = cursor.fetchall()
        status = 'fail'
        for ch in dataofv:
          #if ch[2]==self.password.data:
          if ch[2]==str(pwddb):
            acsql = """SELECT * FROM users WHERE email=%s"""
            cursor.execute(acsql,[str(usernamedb)])
            dataofv = cursor.fetchall()
            actype = ''
            usrid = ''
            for u in dataofv:
                actype = str(u[4])
                usrid = str(u[0])
            session['email'] = str(usrid)
            if actype=="1":
                #company man redirect to subdomain
                #get the company id
                comid = ''
                for u in dataofv:
                    comid = str(u[5])
                dasql = """SELECT * FROM companies WHERE cid=%s"""
                cursor.execute(dasql,[str(comid)])
                #extract the data from db
                dataofv = cursor.fetchall()
                companyfname = ""
                for u in dataofv:
                    companyfname = str(u[1])

                dbql.commit()
                dbql.close()
                status = str(companyfname)
            else:
                status = '2'

        if status == 'fail':
          dbql.commit()
          dbql.close()
        return status
      else:
        #self.email.errors.append("Invalid_username")
        dbql.commit()
        dbql.close()
        status = 'fail'
        return status
      #session['email'] = form.email.data.lower()
      #find whether company man or candidate request.form['personId']

  elif request.method == 'GET':
    return render_template('signpage.html')

@app.route('/signout')
def signout():

  if 'email' not in session:
    return redirect(url_for('signin'))

  session.pop('email', None)
  return redirect(url_for('signin'))



@app.route('/verification/<var>')
def verification(var):
  dbql = MySQLdb.connect("localhost","root","bobbyda16","project")
  cursor = dbql.cursor()
  unimanlink = str(var)
  typeoftask = unimanlink[25]
  valoftask = str(unimanlink[76:len(unimanlink)])
  if typeoftask == '1':
      #update the status value in the users table
      #flash('enter this '+str(valoftask))
      comsql = """UPDATE users SET status='2' WHERE uid=%s"""
      cursor.execute(comsql,[str(valoftask)])
  dbql.commit()
  dbql.close()
  flash("Your account has been verified")
  if 'email' not in session:
    return redirect(url_for('signin'))
  elif session['email'] == valoftask:
    return redirect(url_for('profile'))
  else:
    session.pop('email', None)
    return redirect(url_for('signin'))


@app.route('/invitationaccept/<var>',methods=['GET', 'POST'])
def invitationaccept(var):
  dbql = MySQLdb.connect("localhost","root","bobbyda16","project")
  cursor = dbql.cursor()
  unimanlink = str(var)
  typeoftask = unimanlink[25]
  valoftask = str(unimanlink[76:len(unimanlink)])
  if typeoftask == '2':
      #update the status value in the users table
      if 'email' in session:
        session.pop('email', None)
      if request.method == 'POST':
        data = json.loads(request.data.decode())
        cannamedb = data["cannamedb"]
        canemaildb = data["canemaildb"]
	canimagedb = data["canimagedb"]
        #extract data from inivitation table using taskvalue
        isql = """SELECT * FROM invitations WHERE iid = %s"""
        cursor.execute(isql,[str(valoftask)])
        dataofv = cursor.fetchall()
        nemail = ''
        for u in dataofv:
          nemail = str(u[5])
	  stago = str(u[4])
	if stago=='2':
		#crack is clicking the link again
		#don't do the entry thing
		return 'hell'
	else:
		#entry in users table
		tsql = """INSERT INTO users (email,name,type,status,imageurl) VALUES (%s,%s,%s,%s,%s)"""
		cursor.execute(tsql,[str(canemaildb),str(cannamedb),"2","2",str(canimagedb)])
		dbql.commit()
		#get the uid from users table
		usql = """SELECT * FROM users WHERE email=%s"""
		cursor.execute(usql,[str(canemaildb)])
		dataofv = cursor.fetchall()
		uidofcan = ''
		for u in dataofv:
		  uidofcan = str(u[0])
		#update the invitation table
		insql = """UPDATE invitations SET canid=%s,status='2' WHERE iid=%s"""
		cursor.execute(insql,[str(uidofcan),str(valoftask)])
		session['email'] = str(uidofcan)
		dbql.commit()
		dbql.close()
		#flash("Thankyou for joining Xobin")

		return 'heaven'

      elif request.method == 'GET':
        nicksql = """SELECT * FROM invitations"""
        cursor.execute(nicksql)
        datan = cursor.fetchall()
        for d in datan:
            nname = str(d[5])
        dbql.commit()
        dbql.close()
        return render_template('csignup.html',univar = var,nname= nname)
  else:
    flash("you just tried to do something which is not to be done, becareful! we are watching you very closely")
    return redirect(url_for('signin'))


@app.route('/recang', methods=['POST'])
def recang():
  dbql = MySQLdb.connect("localhost","root","bobbyda16","project")
  cursor = dbql.cursor()
  if 'email' not in session:
    return redirect(url_for('signin'))
  else:
    if request.method == 'POST':
	data = json.loads(request.data.decode())
    	inamedbcode = data["inamecode"]
	ncsql = """SELECT * FROM invitations WHERE recid=%s"""
    	cursor.execute(ncsql,[str(session['email'])])
    	dataofv = cursor.fetchall()
    	ary = []
    	for da in dataofv:
        	emdict = {}
        	emdict['nickemail'] = str(da[5])
        	emdict['status'] = str(da[4])
		emdict['canid'] = str(da[3])
        	ary.append(emdict)
    	dbql.commit()
    	dbql.close()
	return jsonify(datajson = ary)

@app.route('/postinfo', methods=['GET', 'POST'])
def postinfo():

  dbql = MySQLdb.connect("localhost","root","bobbyda16","project")
  cursor = dbql.cursor()
  if 'email' not in session:
    return redirect(url_for('signin'))
  if request.method == 'POST':
    data = json.loads(request.data.decode())
    fnamedb = data["fnamedb"]
    agedb = data["agedb"]
    genderdb = data["genderdb"]
    relationshipdb = data["relationshipdb"]
    otherinfodb = data["otherinfodb"]
    dasql = """SELECT * FROM invitations WHERE recid=%s"""
    cursor.execute(dasql,[str(session['email'])])
    #extract the data from db
    dataofv = cursor.fetchall()
    icompanyid = ''
    for u in dataofv:
        icompanyid = str(u[2])
    jsql = """INSERT INTO info(uid,fname,age,gender,relationship,otherinfo,companyid) VALUES(%s,%s,%s,%s,%s,%s,%s)"""
    cursor.execute(jsql,[str(session['email']),str(fnamedb),str(agedb),str(genderdb),str(relationshipdb),str(otherinfodb),str(icompanyid)])
    dbql.commit()
    dbql.close()
    return "2"

@app.route('/video_feed')
def video_feed():
    return render_template('detect.html')

@app.route('/facedetect')
def facedetect():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/reloader')
def reloader():
	cv2.VideoCapture(0).release()
	return redirect(url_for('profile'))

@app.route('/capsend')
def capsend():
    return render_template('capsend.html')

@app.route('/capimg', methods=['GET', 'POST'])
def capimg():
    dbql = MySQLdb.connect("localhost","root","bobbyda16","project")
    cursor = dbql.cursor()
    dasql = """SELECT * FROM info WHERE uid=%s"""
    cursor.execute(dasql,[str(session['email'])])
    dataofv = cursor.fetchall()
    uname = ''
    uid = ''
    for u in dataofv:
        uname = str(u[2])
	uid = str(u[1])
    path = 'static/captured/'+uid+uname+'/'
    target = os.path.join(APP_ROOT, path)
    print(target)
    if not os.path.isdir(target):
        os.mkdir(target)
    nfiles = sorted(glob.glob(os.path.join('static/captured/'+uid+uname+'/',
		uname+'[0-9][0-9][0-9].png')))
    count = 0
    if len(nfiles) > 0:
	count = int(nfiles[-1][-7:-4])+1
    if request.method == 'POST':
      count1 = str(count)
      img = request.json['imageData']
      imgdata = base64.b64decode(img)
      if int(count1)<10:
      	filename = uname+'00'+count1+'.png'
      else:
	filename = uname+'0'+count1+'.png'
      completeName = os.path.join(target, filename)
      with open(completeName, 'wb') as f:
          f.write(imgdata)
    dbql.commit()
    dbql.close()
    return render_template("capsend.html")

@app.route('/process', methods=['GET', 'POST'])
def process():
    POSITIVE_FILE_PREFIX = 'positive_'
    dbql = MySQLdb.connect("localhost","root","bobbyda16","project")
    cursor = dbql.cursor()
    dasql = """SELECT * FROM info WHERE uid=%s"""
    cursor.execute(dasql,[str(session['email'])])
    dataofv = cursor.fetchall()
    uname = ''
    uid = ''
    for u in dataofv:
        uname = str(u[2])
	uid = str(u[1])
    ncount = 0
    if not os.path.exists('static/training/'+uid+uname):
	os.makedirs('static/training/'+uid+uname)
    pfiles = sorted(glob.glob(os.path.join('static/training/'+uid+uname,
		POSITIVE_FILE_PREFIX + '[0-9][0-9][0-9].pgm')))
    pcount = 0
    if len(pfiles) > 0:
	pcount = int(pfiles[-1][-7:-4])+1
    if request.method == 'POST':
	while pcount<=10:
		imageraw = 'static/captured/'+uid+uname+'/'+uname+'00'+str(ncount)+'.png'
		imageread = cv2.imread(imageraw)
		image = cv2.cvtColor(imageread, cv2.COLOR_BGR2GRAY)
		result = face.detect_single(image)
		if result is None:
			print 'Could not detect face'
			continue
		x, y, w, h = result
		crop = face.crop(image, x, y, w, h)
		filename = os.path.join('static/training/'+uid+uname, POSITIVE_FILE_PREFIX + '%03d.pgm' % pcount)
		cv2.imwrite(filename, crop)
		print 'Found face and wrote training image', filename
		pcount += 1
		ncount += 1
    ssql = """SELECT * FROM info"""
    cursor.execute(ssql)
    datas = cursor.fetchall()
    fields = ['infoid', 'uid', 'fname', 'age', 'gender','relationship','otherinfo','companyid']
    dicts = [dict(zip(fields, d)) for d in datas]
    with open('static/training/info.json', 'w') as fp:
        json.dump(dicts, fp)
    command = 'scp -r static/training/ pi@192.168.1.213:~/Desktop/fromserver/'
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    process.wait()
    flash("Images are processed and sent to the Raspberry Pi")
    dbql.commit()
    dbql.close()
    return redirect(url_for('profile'))


if __name__ == "__main__":
    app.run(host = "0.0.0.0",debug=True)
