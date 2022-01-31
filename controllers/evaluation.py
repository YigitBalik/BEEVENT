from hashlib import sha256
import sys
import datetime
from flask_login.utils import login_required, logout_user
from psycopg2 import connect
sys.path.append('..\\itudb2130')
import services.evaluation as evaluationService
import services.userEvent as userEventService
from models import Evaluation, User, UserEvent
from flask import render_template, request, redirect, url_for, session
from forms import AddEvaluationForm

@login_required
def addEvaluation(eventid):
    form = AddEvaluationForm()
    return render_template("addEvaluation.html", form=form, eventid = eventid)

@login_required
def updateEvaluation(eventid, evaluationid):
    form = AddEvaluationForm()
    evaluation = evaluationService.getEvaluation(evaluationid)
    print(eventid)
    return render_template("updateEvaluation.html", form=form,evaluation = evaluation, eventid=eventid)

@login_required
def saveEvaluation(type, eventid):
    form = AddEvaluationForm()
    evaluationid = userEventService.getEvaluationId(session['id'],eventid)
    evaluation = evaluationService.getEvaluation(evaluationid)
    if form.validate_on_submit():
        timestamp = datetime.datetime.now()
        comment = request.form['comment']
        priceRate = request.form['priceRate']
        funRate = request.form['funRate']
        today = datetime.date.today()
        eventDate = userEventService.getEventStartDate(session['id'],eventid)
        checkedin = False
        if today > eventDate:
            checkedin = True
        evaluation = Evaluation(evaluationid,timestamp,comment,priceRate,funRate,checkedin)
        if evaluationService.saveEvaluation(evaluation):
            return redirect(url_for("userEvents"))
    else:
        if type == 0:
            return render_template("updateEvaluation.html", form=form, eventid = eventid, evaluation = evaluation)
        else:
            return render_template("addEvaluation.html", form=form, eventid = eventid)

@login_required
def deleteEvaluation(eventid,evaluationid):
    evaluationService.deleteEvaluation(evaluationid)
    evaluation = Evaluation(None, None, None, None, None, True)
    newevaluationid = evaluationService.createEvaluation(evaluation)
    userEvent = UserEvent(session['id'],eventid,newevaluationid)
    userEventService.updateUserEvent(userEvent)
    return redirect(url_for("event", eventid=eventid))