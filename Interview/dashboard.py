from flask import render_template, request, redirect, session, Blueprint
from iGeekFirebase.firebase import firebase
import datetime, time, string, math
from iGeekAuth.auth import signin
from email.mime import multipart, text as mailText
import smtplib

db = firebase.database()
auth = firebase.auth()

app = Blueprint('dashboard', __name__)


@app.route("/dashboard")
def dashBoard():
    if 'username' not in session.keys():
        return signin(None, "/blog/")

    data = getData(session['username'])
    # print(data)

    data.sort(key=lambda data: data['date'])
    # print(data)
    # for d in data:
    #     print(d['daytime'])

    if len(data) == 0:
        tup = ""
    else:
        tup = data[0]

    return render_template("Interview/dashboard.html", list=data, tuple=tup)


@app.route("/scheduleInterview", methods=['POST', 'GET'])
def scheduleNewInterview():
    # print(request.form["link"])
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        name = data['username']
        data['username'] = session['username']
        data['status'] = "N/A"
        # print(data)
        db.child("Dashboard").child(name).push(data)

        data["username"] = name
        name = session['username']
        # print(data)
        db.child("Dashboard").child(name).push(data)

    return redirect('/dashboard')


@app.route("/openIDE", methods=['POST', 'GET'])
def openIDE():
    if 'username' not in session.keys():
        return signin(None, "/openIDE/")

    print(request.method)
    if request.method == 'POST':
        print("xxxxxxxxxxxxx")
        data = request.form.to_dict()
        print(data)

        link = data["Ilink"]
        print(link)
        return render_template("Interview/interviewplatform2.html", link=link)


# data = getData(session['username'])
# data.sort(key=lambda data: data['daytime'])
#
# for item in data:
#     name = item["username"]
#     link = item["link"]
#     break

# key = ""
# data = db.child("Dashboard").child(session['username']).get().val()
# print("aaaaaaaaaaaaaaaaaaaaaaaaa")
# print(data)
# for item in data:
#     if data[item]["link"] == link:
#         rmv = item
#         key = item
#         break
#
# print("xxxxxxxxxx")
# print(key)
# print(name)
# print(link)
#
# if key != "":
#     db.child("Dashboard").child(session['username']).remove(key)
#
# # print("xxxxxxxxxx")
# # print(key)
# # print(name)
# # print(link)
# # print("yyyyyyyyyyy")
# # db.delete(key, None)
# # print(getData(session['username']))
#
# key = ""
# data = db.child("Dashboard").child(name).get().val()
# for item in data:
#     key = item
#     break
#
# if key != "":
#     db.child("Dashboard").child(name).remove(key)


# link = "http://127.0.0.1:5000/p2pchatting#27942899861995983"



@app.route("/updateDB")
def updateDB():
    if 'username' not in session.keys():
        return signin(None, "/updateDB/")

    return redirect('/dashboard')


@app.route("/startVideoChatting", methods=['POST', 'GET'])
def startVideoChatting():
    if 'username' not in session.keys():
        return signin(None, "/startVideoChatting/")

    if request.method == 'POST':
        data = request.form.to_dict()
        link = data['Ilink']
    return render_template("videoChat.html",link=link)


def getData(name):
    data = db.child("Dashboard").child(name).get().val()
    # print(data)
    list = []
    if data:
        for item in data:
            list.append(data[item])
            # print(data['daytime'])
        # print(list)

    return list


@app.route("/circular")
def interviewCircular():
    if 'username' not in session.keys():
        return signin(None, "/circular/")

    data = db.child("Circulars").get().val()
    # print(data)
    list = []
    if data:
        for item in data:
            list.append(data[item])
    print(list)

    return render_template("Interview/jobCircular.html", list=list)


@app.route("/newJobCircular", methods=['POST', 'GET'])
def newJobCircular():
    if 'username' not in session.keys():
        return signin(None, "/newJobCircular/")

    if request.method == 'POST':
        data = request.form.to_dict()
        # print(data)

        print(data)

        data["candidateID"] = session['username']
        data["circularID"] = ""
        id = db.child("Circulars").push(data)

        db.child("Circulars").child(id['name']).child("circularID").set(id['name'])

    return redirect('/circular')


@app.route("/apply_interview", methods=['POST', 'GET'])
def applyInterview():
    if 'username' not in session.keys():
        return signin(None, "/apply_interview/")

    data = request.form.to_dict()
    print(data)

    fromaddr = "interviewgeek7@gmail.com"
    msg = multipart.MIMEMultipart()
    msg['From'] = "interview Geek"
    # msg['To'] = toaddr
    toaddr = data["email"]
    msg['Subject'] = "New response to your interview circular"

    msg_body = "A user named " + session[
        "username"] + " from interview Geek responds to your interview circular!!! \n\n Thank You."

    msg.attach(mailText.MIMEText(msg_body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login("interviewgeek7@gmail.com", "iplab2019")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

    return redirect("/circular")
