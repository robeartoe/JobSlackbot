import time, traceback, sys, logging
try:
    from dotenv import load_dotenv
    load_dotenv()
    import os
except:
    import os
from flask import Flask, request,render_template,url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
db = SQLAlchemy(app)

from scrape import do_scrape
from models import Settings

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/settings")
def settings():
    return render_template("settings.html")

@app.route("/update",methods=["GET","POST"])
def update():
    success = True
    return render_template("update.html",success=success)

@app.route("/scrape")
def scrape():
    starttime = time.time()
    print("{} : Starting scrape cycle".format(time.ctime()))
    try:
        do_scrape()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit(1)
    except Exception as exc:
        print("Error with scraping".format(time.ctime()))
        traceback.print_exc()
    else:
        print("{}: Finished scraping with no issues".format(time.ctime()))
        print("{} Amount of time it took to complete.".format(time.time() - starttime))
    return 'Finished Scraping with no issues',200

@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

# if __name__ == '__main__':
#     # This is used when running locally. Gunicorn is used to run the
#     # application on Google App Engine. See entrypoint in app.yaml.
#     app.run(host='127.0.0.1', port=8080, debug=True)
