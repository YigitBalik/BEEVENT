# fmt: off
import sys
from math import gcd
from werkzeug.utils import redirect
sys.path.append('..\\itudb2130')
from models import Image
import services.image as imageService
from flask import render_template, request
from flask_login.utils import *
from forms import ImageForm, LoginForm
# fmt: on

@login_required
def getImages():
    if session['role'] == 'admin':
        images = imageService.getImages()
        return render_template("images.html",images=images)
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can manage images. If you have an admin account please login."])

@login_required
def deleteImage(imageid):
    if session['role'] == 'admin':
        if imageid == 1:
            return url_for('images')
        Image = imageService.getImage(imageid)
        if Image is not None:
            imageService.deleteImage(imageid)
            return redirect(url_for('images'))
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can delete images. If you have an admin account please login."])

@login_required
def addImage():
    if session['role'] == 'admin':
        form = ImageForm()
        return render_template("addImage.html",form=form)
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can add images. If you have an admin account please login."])

@login_required
def createImage():
    if session['role'] == 'admin':
        form = ImageForm()
        if form.validate_on_submit():
            height = int(request.form['height'])
            width = int(request.form['width'])
            alt = request.form['alt']
            source = request.form['source']
            ratioDivisor = gcd(height,width)
            ratio = str(int(height/ratioDivisor)) + '_' + str(int(width/ratioDivisor))
            image = Image(None, ratio, source, height, width, alt)
            imageid = imageService.saveImage(image)
            if imageid is not None:
                return redirect(url_for("images"))
        return render_template("addImage.html",form = form ,messages=['Something went wrong with the database'])  
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can add images. If you have an admin account please login."])

@login_required
def updateImage(imageid):
    if session['role'] == 'admin':
        form = ImageForm()
        image = imageService.getImage(imageid)
        return render_template('addImage.html', form=form, image=image, type='update')
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can add images. If you have an admin account please login."])

@login_required
def saveUpdatedImage(imageid):
    if session['role'] == 'admin':
        form = ImageForm()
        if form.validate_on_submit():
            height = int(request.form['height'])
            width = int(request.form['width'])
            alt = request.form['alt']
            source = request.form['source']
            ratioDivisor = gcd(height,width)
            ratio = str(int(height/ratioDivisor)) + '_' + str(int(width/ratioDivisor))
            image = Image(None, ratio, source, height, width, alt)
            result = imageService.updateImage(imageid, image)
            if result:
                return redirect(url_for("images"))
        return render_template("addImage.html",form = form, image = imageService.getImage(imageid) ,messages=['Something went wrong with the database'], type='update')  
    loginForm = LoginForm()
    return render_template("login.html",form=loginForm, messages = ["Only admins can add images. If you have an admin account please login."])