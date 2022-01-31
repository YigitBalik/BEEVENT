from hashlib import sha256
import sys

from flask_login.utils import login_required, logout_user
sys.path.append('..\\itudb2130')
import services.user as userService
from models import User
from flask import render_template, request, redirect, url_for, session
from forms import LoginForm, RegisterForm, UpdateUserForm, ChangePasswordForm
from flask_login import login_user, UserMixin

class CurrentUser(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

    def get_id(self):
        return self.id

    def getUsername(self):
        return self.username

    def getRole(self):
        return self.role

def getUser(userid):
    if 'role' in session:
        user = userService.getUserById(userid)
        if user is None:
            return None
        return CurrentUser(userid,user.username,'user' if (user.role == 0 or user.role == 1) else 'admin')

@login_required
def getUserProfile():
    user = userService.getUserById(session['id'])
    return render_template("myprofile.html", user = user)


@login_required
def updateUserProfile():
    user = userService.getUserById(session['id']) #current user
    form = UpdateUserForm() #an empty form
    return render_template("editUserProfile.html", user = user, form = form) #load page for empty update user form and current user

@login_required
def saveUpdatedUserProfile():
    form = UpdateUserForm()
    userid = session['id']
    if form.validate_on_submit():
        username = request.form['username']
        email = request.form['email']
        country = request.form['country']
        age = request.form['age']
        user = User(None,username,email,None,country,age,None,None)
        result = userService.updateUser(userid,user)
        print(result)
    return redirect(url_for("profile"))    

@login_required
def changeUserPassword():
    user = userService.getUserById(session['id']) #current user
    form = ChangePasswordForm() #an empty form
    return render_template("ChangePassword.html", user = user, form = form) #load page for empty update user form and current user

@login_required
def saveChangedUserPassword():
    form = ChangePasswordForm()
    userid = session['id']
    if form.validate_on_submit():
        password = request.form['password']
        password = sha256(password.encode('utf-8')).hexdigest()
        result = userService.changePassword(userid,password)
        print(result)
        return redirect(url_for("profile")) 
    else:
        return redirect(url_for("changePassword")) 
           
@login_required
def getUsers():
    if session['role'] == 'admin':
        users = userService.getUsers()
        return render_template("users.html",users=users)
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can manage users. If you have an admin account please login."])

@login_required
def assignRole(userid, role):
    if session['role'] == 'admin':
        userService.updateUserRole(userid, role)
        return redirect(url_for('users'))
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can manage users. If you have an admin account please login."])

@login_required
def deleteUser(userid):
    if session['role'] == 'admin':
        User = userService.getUserById(userid)
        if User is not None:
            userService.deleteUser(userid)
            if session['id'] == userid:
                logout_user()
                if 'role' in session:
                    session.pop('role')
                if 'id' in session:
                    session.pop('id')
                return redirect(url_for('login'))
            return redirect(url_for('users'))
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can delete users. If you have an admin account please login."])

def login():
    form = LoginForm()
    return render_template("login.html", form=form)

def register():
    form = RegisterForm()
    return render_template("register.html", form=form)

def registerUser():
    form = RegisterForm()
    if form.validate_on_submit():
       username = request.form['username']
       email = request.form['email']
       password = request.form['password']
       country = request.form['country']
       age = request.form['age']
       user = User(None, username, email, password, country, age, 1 if 'admin_request' not in request.form else 0,None)
       if userService.saveUser(user):
        return redirect(url_for("events"))

    else:
        return render_template("register.html", form=form)
def logout():
    logout_user()
    if 'role' in session:
        session.pop('role')
    if 'id' in session:
        session.pop('id')
    return redirect(url_for('login'))
def loginUser():
    form = LoginForm()
    if form.validate_on_submit():
        username = request.form['username']
        password = sha256(request.form['password'].encode('utf-8')).hexdigest()
        user = userService.getUserByUsername(username)
        if user is not None and password == user.password:
            currentUser = CurrentUser(user.id,user.username,'user' if (user.role == 0 or user.role == 1) else 'admin')
            login_user(currentUser)
            session['id'] = currentUser.get_id()
            session['role'] = currentUser.getRole()
            return redirect(url_for('events'))
        else:
            return render_template('login.html',form=form,messages=["Wrong password or username"])
    else:
        return render_template("login.html", form=form)