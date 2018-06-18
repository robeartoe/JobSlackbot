import os
from main import db
from models import Settings

if __name__ == '__main__':
    print('Creating all database tables...')
    db.create_all()

    if Settings.query.filter_by(id=1).first() is None:
        settings = Settings(indeed=True,craigslist=True)
        try:
            db.session.add(settings)
            db.session.commit()
            db.session.close()
        except Exception as inst:
            print(inst)
            print("Error DB")
    user = Settings.query.filter_by(id=1).first()
    user.set_password(os.environ['PW'])
    user.username = "rob"
    db.session.commit()
    db.session.close()
    
    print('Done!')
