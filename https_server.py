#coding=utf-8
from flask import Flask,request,make_response,render_template,escape,redirect,url_for,session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,scoped_session
from user_db import Base,User
from werkzeug import secure_filename
import hashlib
import random
import string
import hmac
import bcrypt
app = Flask(__name__)

SALT = "salt-1"

user_engine = create_engine('sqlite:///users.db')
Base.metadata.bind = user_engine
# using scoped_session to fix issue of Program issue. cannot access database object in diffirent thread
dbsession = scoped_session(sessionmaker(bind=user_engine))

# dbsession = DBSession()

@app.route("/")
def hello():
    if 'username' in session:
        return 'Logged in as %s' % escape(session['username'])
    else:
        return redirect(url_for('login'))
@app.route("/cookie")
def cookie():
    visitstr = request.cookies.get('visits')
    visits = 0
    if visitstr:
        result = visitstr.split('|')
        if result[0].isdigit() and check_visits(result[0],result[1]):
            visits = int(result[0])+1
    resp = make_response(("this is the %s visit" % visits,200,None))
    resp.set_cookie('visits',"%s|%s" % (str(visits),hash_salt(str(visits))))
    return resp

def hash_salt(s):
    hashstr = "%s+%s" % (SALT,s)
    # return hashlib.sha256(hashstr).hexdigest()
    return hmac.new(SALT,s).hexdigest()
def check_visits(v,result):
    if result == hash_salt(v):
        return True
    else:
        return False
def make_salt():
    return ''.join(random.choice(string.letters) for x in xrange(5))
@app.route("/login",methods=['POST','GET'])
def login():
    print request.method
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['user_name']
        password = request.form['password']
        check_user = dbsession.query(User).filter_by(name=username).one_or_none()
        if check_user and checkPassword(password,check_user.hash_pw):
            print check_user.hash_pw
            session['username'] = username
            return "Welcome Dear User"
        elif check_user:
            return "Password wrong!!!"
        else:
            return "User not regiestered"
@app.route("/logout",methods=['GET'])
def logout():
    session.pop('username',None)
    return redirect(url_for('/'))
def checkHashPW(un,pw,hash_pw):
    salt = hash_pw.split('|')[1]
    print salt
    return hash_pw == getHashedPW(un,pw,salt)
@app.route("/register",methods=['POST','GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        username = request.form['user_name']
        password = request.form['password']
        another_user = dbsession.query(User).filter_by(name=username).one_or_none()
        if another_user:
            return "Username has been registerd!!!!"
        else:
            user = User(name=username,hash_pw=getHashedPW(password))
            dbsession.add(user)
            dbsession.commit()
            return "Register Success!"

@app.route("/upload",methods=['POST','GET'])
def upload():
    if request.method == 'GET':
        print "get Get request"
        return render_template("upload.html")
    elif request.method == 'POST':
        print "get post request"
        f = request.files['file']
        f.save(secure_filename(f.filename))
        return 'file uploaded successfully'

def getHashedPW(password):
    print password
    return bcrypt.hashpw(password.encode(encoding='utf-8'),bcrypt.gensalt(rounds=14,prefix=b"2b"))
def checkPassword(password,hashedpw):
    return bcrypt.hashpw(password.encode(encoding='utf-8'),hashedpw.encode(encoding='utf-8')) == hashedpw
# def getHashedPW(username,pw,salt=None):
#     print username
#     print pw
#     if not salt:
#         salt = make_salt()
#     return "%s|%s" % (hashlib.sha256("%s%s|%s" %(salt,username,pw)).hexdigest(),salt)
if __name__ == "__main__":
    context = ('mysitename.crt','mysitename.key')
    app.secret_key='7\x8a)\x1a\xa8\xe4\x8b\x0e\x0e\x1d\xa8\xf0\x98*\xd2\x1d(\x89\xbf\x0fV\xbf\xb1\x1f'
    app.run(host='0.0.0.0',port=5001,ssl_context=context,threaded=True,debug=True)

