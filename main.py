import time, traceback, sys, logging,json
try:
    from dotenv import load_dotenv
    load_dotenv()
    import os
except:
    import os
from flask import Flask,request,render_template,url_for,redirect
from flask_login import LoginManager,logout_user,login_required,login_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sqlalchemy
from sqlalchemy import create_engine,desc
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker, scoped_session

app = Flask(__name__)
login = LoginManager(app)
login.login_view ='login'

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from scrape import do_scrape
from models import Settings, Listing, indeedModel,craigslistModel

@app.route("/")
@app.route("/index")
@login_required
def main():
    if userSettings:
        inSetting = Settings.query.get(1).indeed
        clSetting = Settings.query.get(1).craigslist
    inListing = Listing.query.filter_by(InorCl="IN").order_by(desc(Listing.created)).limit(50).all()
    clListings = Listing.query.filter_by(InorCl="CL").order_by(desc(Listing.created)).limit(50).all()
    return render_template("main.html",inListing=inListing,clListings=clListings)

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method =="POST":
        print(request.form)
        username = request.form['username']
        pw = request.form['password']
        user = Settings.query.get(1)
        if user.check_password(pw):
            login_user(user)
            return redirect(url_for('main'))
        else:
            return render_template("login.html")
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/settings")
def settings():
    if userSettings:
        inSetting = Settings.query.get(1).indeed
        clSetting = Settings.query.get(1).craigslist
    clQuery = craigslistModel.query.all()
    inQuery = indeedModel.query.all()
    return render_template("settings.html",inSetting=inSetting,clSetting=clSetting,inQuery=inQuery,clQuery=clQuery)


@app.route("/update",methods=["POST"])
def update():
    status = request.json['status']
    print(request.get_json())

    if status == "updateService":
        setting = Settings.query.get(1)
        if request.json['service'] == "craigslist":
            if request.json['currSetting']:
                setting.craigslist = True
            else:
                setting.craigslist = False
            db.session.commit()
            db.session.close()
            return json.dumps({'status':'OK'})
        else:
            if request.json['currSetting']:
                setting.indeed = True
            else:
                setting.indeed = False
            db.session.commit()
            db.session.close()
            return json.dumps({'status':'OK'})

    elif status == "addRow":
        userSetting = Settings.query.get(1)
        if request.json['service'] == "craigslist":
            if request.json['internship'] == '0':
                internship = False
            else:
                internship = True
            for area in request.json['areas']:
                for category in request.json['categories']:
                    clEntry = craigslistModel(user_id=userSetting.id,
                                            city=request.json['city'],
                                            area=area,
                                            internship=internship,
                                            category=category,
                                            slackChannel=request.json['sChannel'],
                                            icon=request.json['icon'])
                    db.session.add(clEntry)
        else:
            for keys in request.json["keywords"]:
                inEntry = indeedModel(user_id=userSetting.id,
                                    city=request.json['city'],
                                    keyword=keys,
                                    slackChannel=request.json['sChannel'],
                                    icon=request.json['icon'])
                db.session.add(inEntry)
        db.session.commit()
    elif status == "deleteRow":
        if request.json['service'] == 'craigslist':
            if request.json['internship'] == 'True':
                internship = True
            else:
                internship = False
            row = craigslistModel.query.filter_by(city=request.json['city'],
                                                    area=request.json['area'],
                                                    category=request.json['category'],
                                                    internship=internship,
                                                    slackChannel=request.json['slackChannel']).first()

            db.session.delete(row)
            db.session.commit()
        else:
            row = indeedModel.query.filter_by(city = request.json['city'],
                                                keyword=request.json['keyword'],
                                                slackChannel=request.json['slackChannel']).first()
            db.session.delete(row)
            db.session.commit()
    return json.dumps({'status':'FAIL'})

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

def userSettings():
    if Settings.query.filter_by(id=1).first() is None:
        settings = Settings(indeed=True,craigslist=True)
        try:
            db.session.add(settings)
            db.session.commit()
            db.session.close()
            return True
        except Exception as inst:
            print(inst)
            print("Error DB")
            return False
    return True


# if __name__ == '__main__':
#     # This is used when running locally. Gunicorn is used to run the
#     # application on Google App Engine. See entrypoint in app.yaml.
#     app.run(host='127.0.0.1', port=8080, debug=True)
