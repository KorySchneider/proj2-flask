"""
Very simple Flask web site, with one page
displaying a course schedule.

"""

import flask
from flask import render_template
from flask import request
from flask import url_for

import json
import logging

# Date handling 
import arrow # Replacement for datetime, based on moment.js
from datetime import datetime # But we still need time
from dateutil import tz  # For interpreting local times

# Our own module
import pre  # Preprocess schedule file


###
# Globals
###
app = flask.Flask(__name__)
import CONFIG


###
# Helper functions
###

def getWeek(weeks, today):
    """
    Finds and returns the current week number based on today's date
    """
    for i in range(0, len(weeks)):
        startdate = datetime.strptime(weeks[i]['startdate'], '%m/%d/%Y')
        next_startdate = datetime.strptime(weeks[i+1]['startdate'], '%m/%d/%Y')

        if today > startdate:
            if today < next_startdate:
                return int(weeks[i]['week'])
            else:
                getWeek(weeks[1:], today)
        else:
            app.logger.debug("Could not find date in term")
            return


###
# Pages
###

@app.route("/")
@app.route("/index")
@app.route("/schedule")
def index():
    app.logger.debug("Main page entry")

    # Process schedule data
    app.logger.debug("Processing raw schedule file")
    pre.main()

    # Determine week to highlight
    currentWeek = getWeek(pre.schedule, datetime.now())
    for i in range(0, len(pre.schedule)):
        if int(pre.schedule[i]['week']) == currentWeek:
            pre.schedule[i]['highlight'] = True
        else:
            pre.schedule[i]['highlight'] = False

    flask.session['schedule'] = pre.schedule

    return flask.render_template('syllabus.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    flask.session['linkback'] =  flask.url_for("index")
    return flask.render_template('page_not_found.html'), 404

#################
#
# Functions used within the templates
#
#################

@app.template_filter( 'fmtdate' )
def format_arrow_date( date ):
    try: 
        normal = arrow.get( date )
        return normal.format("ddd MM/DD/YYYY")
    except:
        return "(bad date)"


#############
#    
# Set up to run from cgi-bin script, from
# gunicorn, or stand-alone.
#
app.secret_key = CONFIG.secret_key
app.debug=CONFIG.DEBUG
app.logger.setLevel(logging.DEBUG)
if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")

