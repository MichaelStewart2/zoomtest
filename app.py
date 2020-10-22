from flask import Flask, redirect
from flask import render_template, session
from flask import request
from threading import Thread
from datetime import datetime as dt
from random import randint
import pytz
import smtplib
app = Flask(__name__)

SESSION_TYPE = 'redis'
app.config.from_object(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'



reminders = {}

@app.route('/')
def hello_world():
    name = "Ms.Rev"
    return render_template('hello.html', name=name)

@app.route('/howdy')
def hello():
    name = "Ms.Rev"
    return render_template('hello.html', name=name)

@app.route('/text', methods=['GET','POST'])
def text():
    txt = request.form['txt']
    num = request.form['num']
    num = num.replace("-", "").replace("(", "").replace(" ", "").replace(")", "")

    hr = str(request.form['hr'])
    min = str(request.form['min'])
    ampm = request.form['ampm']

    mon = str(request.form['mon'])
    day = str(request.form['day'])

    #generate messageid
    messageID = num + str(randint(1,500))
    while (messageID in reminders.keys()):
        messageID = num + str(randint(1,500))

    reminders[messageID] = "notSent"

    #print(hr + ":" + min + " " + ampm)
    if (ampm == "pm" or (hr == "0" or hr == "00")):
        hr = int(hr) + 12
        if(hr >= 24):
            hr = 0
        hr = str(hr)
    elif (ampm == "am" and (hr == "12")):
        hr = 0
        hr = str(hr)
    t = Thread(target=delay_msg, args=(txt,hr,min,num,mon,day,messageID))
    t.start()

    session["messageID"] = messageID
    #send_msg("campusculturalchallenge@gmail.com", "bestprogram", "", txt + hr,num)
    name = "Ms.Rev"
    return redirect('/success')
def send_msg(username, password, subj, msg,num):
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.ehlo
    s.login(username, password)
    headers = ["From: " + username, "Subject: " + subj, "To: " + username]
    headers = "\r\n".join(headers)
    s.sendmail(username,num + '@txt.att.net', headers + "\r\n\r\n" + msg)
    #s.sendmail(username, num + '@messaging.sprintpcs.com', headers + "\r\n\r\n" + msg)
    #s.sendmail(username, num + '@tmomail.net', headers + "\r\n\r\n" + msg)
    #s.sendmail(username, num + '@vtext.com', headers + "\r\n\r\n" + msg)
    #s.sendmail(username, num + '@mymetropcs.com', headers + "\r\n\r\n" + msg)

    #sendmail is sender mail,recip mail,headers
    print('Email sent!\n')
    s.quit()
def delay_msg(txt,hr,min,num,mon,day,messageID):
    print("starting delay")
    tz = pytz.timezone('America/Chicago')
    while(True):
        #print(hr + ":" + min + " ----------  "  + str(dt.now(tz).hour)  + ":" + str(dt.now(tz).minute))
        if (hr == str(dt.now(tz).hour) and min ==str(dt.now(tz).minute)    and (mon == str(dt.now(tz).month) and day == str(dt.now(tz).day))):
            send_msg("campusculturalchallenge@gmail.com", "xwnbnpvcmqwnjzmo", "", txt, num)
            reminders[messageID] = "sent"
            break;
        if (reminders[messageID] == "cancel"):
            break;


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/cancel')
def cancel():
    messageID = session.get('messageID')
    reminders[messageID] = "cancel"
    return redirect('/')

