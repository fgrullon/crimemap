from dbhelper import DBHelper
from flask import Flask
from flask import render_template
from flask import request
import json
import datetime
import dateparser
import string


app = Flask(__name__)
DB = DBHelper()

categories = ['mugging', 'break-in']

@app.route("/")
def home(error_message=None):
    crimes = DB.get_all_crimes()
    crimes = json.dumps(crimes)
    return render_template("home.html", crimes=crimes, categories=categories, error_message=error_message)

@app.route("/submitcrime", methods=['POST'])
def submitcrime():
    #catergory
    category = request.form.get("category")
    if category not in categories:
        return home()
        #date
    date = format_date(request.form.get("date"))
    if not date:
        return home("Invalid date. Please use yyyy-mm-dd format.")
    #location    
    try:
        latitude = float(request.form.get("latitude"))
        longitude = float(request.form.get("longitude"))
    except ValueError:
        return home()
    #description
    description = sanitize_string(request.form.get("description"))
    #send data to db
    DB.add_crime(category, date, latitude, longitude, description)
    return home()

def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except:
        return None

def sanitize_string(userinput):
    whitelist = string.letters + string.digits + "!?$.,;:-'()&"
    return filter(lambda x: z in whitelist, userinput)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
