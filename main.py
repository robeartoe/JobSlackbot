import time, traceback, sys, logging, os
from dotenv import load_dotenv
load_dotenv()
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from scrape import do_scrape

# engine = create_engine('sqlite:///listings.db',connect_args={'check_same_thread': False}, echo=False)
# Base = declarative_base()

# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)
# session = scoped_session(Session)

class Listing(db.Model):
    """
    Hold all types of data on listing.
    """
    __tablename__ = 'listings'

    id = db.Column(db.Integer , primary_key = True)
    link = db.Column(db.String(400), unique = True) #'url' for both Indeed and Craigslist
    created = db.Column(db.String(400)) #'date' for Indeed and 'datetime' for Craigslist
    name = db.Column(db.String(400),nullable = True) #'company' Name Only for Indeed
    title = db.Column(db.String(400)) # 'jobtitle' for Indeed and and 'name' forCraigslist
    location = db.Column(db.String(400)) #'formattedLocation', and 'where' for craigslist
    city = db.Column(db.String(400)) #Los Angeles or New York
    JobKeyOrID = db.Column(db.String(400), unique=True) #'jobkey' for Indeed and 'id' for Craigslist


@app.route("/")
def main():
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

if __name__ == '__main__':
    # This is used when running locally. Gunicorn is used to run the
    # application on Google App Engine. See entrypoint in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
