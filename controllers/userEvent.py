# fmt: off
import sys
from werkzeug.utils import redirect
sys.path.append('..\\itudb2130')
from models import Evaluation, Event, UserEvent
from flask import render_template, request
import services.userEvent as userEventService
from services.evaluation import createEvaluation
from services.event import getDate
from flask_login.utils import *
from datetime import datetime
# fmt: on

@login_required
def addUserEvent(eventid):
    userid = session['id']
    date = getDate(eventid)
    isCheckedIn = date <= datetime.now()
    evaluation = Evaluation(None, None, None, None, None, isCheckedIn)
    evaluationid = createEvaluation(evaluation)
    userEvent = UserEvent(userid, eventid, evaluationid)
    result = userEventService.saveUserEvent(userEvent)
    return redirect(url_for('event', eventid=eventid))

@login_required
def getUserEvents():
    userid = session['id']
    userEvents = userEventService.getUserEvents(userid)
    return render_template("myEvents.html", events=userEvents)