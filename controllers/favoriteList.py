# fmt: off
import sys
from werkzeug.utils import redirect
sys.path.append('..\\itudb2130')
from models import FavoriteList
from flask import render_template, request
import services.favoriteList as favoriteListService
import services.user as userService
from services.evaluation import createEvaluation
from services.event import getDate
from flask_login.utils import *
from datetime import datetime
from forms import CreateFavoriteListForm
# fmt: on

@login_required
def getFavoriteList():
    userid = session['id']
    favoriteList = favoriteListService.getFavoriteList(userid)
    return render_template("myFavoriteList.html", favoriteList=favoriteList)

@login_required
def createFavoriteList():
    form = CreateFavoriteListForm() #an empty form
    return render_template("createFavoriteList.html", form = form) #load page for empty update user form and current user

@login_required
def saveCreatedFavoriteList():
    form = CreateFavoriteListForm()
    userid = session['id']
    if form.validate_on_submit():
        timestamp = datetime.now()
        description = request.form['description']
        list_name = request.form['list_name']
        public = request.form['public']
        favoriteList = FavoriteList(None,list_name,description,timestamp,None,public)
        if favoriteListService.saveCreatedFavoriteList(favoriteList,userid):
            return redirect(url_for("favoriteList"))
    else:
        return render_template("createFavoriteList.html", form=form)

@login_required
def updateFavoriteList():
    userid = session['id']
    favoriteList = favoriteListService.getFavoriteList(userid)
    form = CreateFavoriteListForm() #an empty form
    return render_template("updateFavoriteList.html", favoriteList = favoriteList, form = form) #load page for empty update user form and current user

@login_required
def saveUpdatedFavoriteList():
    form = CreateFavoriteListForm()
    userid = session['id']
    favListID = userService.getFavoriteListId(userid)
    if form.validate_on_submit():
        timestamp = datetime.now()
        description = request.form['description']
        list_name = request.form['list_name']
        public = request.form['public']
        favoriteList = FavoriteList(favListID,list_name,description,None,timestamp,public)
        if favoriteListService.saveUpdatedFavoriteList(favoriteList,userid):
            return redirect(url_for("favoriteList"))
        else:
            favList = favoriteListService.getFavoriteList(userid)
            return render_template("updateFavoriteList.html",favoriteList = favList, form=form)
    else:
        favList = favoriteListService.getFavoriteList(userid)
        return render_template("updateFavoriteList.html",favoriteList = favList, form=form)

@login_required
def deleteFavoriteList(favoriteListID):
    if favoriteListService.deleteFavoriteList(favoriteListID):
        return redirect(url_for("favoriteList"))
    else: 
        return redirect(url_for("favoriteList"))

@login_required
def getPublicFavoriteLists():
    publicFavoriteLists = favoriteListService.getPublicFavoriteLists()
    return render_template("publicFavoriteLists.html", publicFavoriteLists=publicFavoriteLists)
