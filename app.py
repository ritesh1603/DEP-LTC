import os
from flask import Flask, send_from_directory,redirect, request
from flask_session import Session
from flask_cors import CORS
import sys
import json
import collections
from routes import router
from models import db, User, Role, TAInfo, LTCInfo
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import Select2Widget
from flask_migrate import Migrate
from flask_admin.form import ImageUploadField
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.date import DateTrigger
# from functions import sendReminders
from datetime import datetime,timezone,timedelta
from helper import remindStakeholder, remindStakeholderta

os.environ['DATABASE_URL'] = 'postgresql://dep_database_render_user:lEejAMNz4Lp312Fgj26l3ZWNwHTLRSyK@dpg-co0t6k7109ks73biiv0g-a.singapore-postgres.render.com/dep_database_render'

if sys.version_info.major == 3 and sys.version_info.minor >= 10:
    from collections.abc import MutableSet
    collections.MutableSet = collections.abc.MutableSet
else:
    from collections import MutableSet

app = Flask(__name__, static_url_path="", static_folder="static1/")
cors = CORS(app, resources={"/*": {"origins": "*"}})
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
#postgres://dep_database_render_user:lEejAMNz4Lp312Fgj26l3ZWNwHTLRSyK@dpg-co0t6k7109ks73biiv0g-a.singapore-postgres.render.com/dep_database_render
db.init_app(app)

scheduler = BackgroundScheduler()
scheduler.start()


migrate = Migrate(app, db)
app.register_blueprint(router, url_prefix="/api")
admin = Admin(app)

# with app.app_context():
#     users = User.query.all()
#     for user in users:
#             user.last_notification_check = datetime.now()

#     # Commit changes to the database session
#     db.session.commit()
def sendReminders():
    with app.app_context():
        a = [j for j in LTCInfo.query.filter(
            LTCInfo.stageCurrent != 0 and LTCInfo.stageCurrent < 100).all()]
        f = filter(lambda j: (datetime.now() - j.lastForwardDate).days > 3, a)
        forms = [{'firstName': x.user.firstName, 'lastName': x.user.lastName, 'department': x.user.department,'delay': (
            datetime.now() - x.lastForwardDate).days, 'stageCurrent': x.stageCurrent, 'id': x.id} for x in f]        

        for form in forms:
            role = Role.query.filter(
                Role.stageCurrent == form['stageCurrent']).first()
            if form['stageCurrent']==1:
                emails = [user.emailId for user in User.query.filter(
                User.roleId == role.id , User.department == form['department'])]
            else:
                emails = [user.emailId for user in User.query.filter(
                    User.roleId == role.id)]
            for email in emails:
                form['email'] = email
                print(form)
                remindStakeholder(form)

def update_officiating_hod(email, is_officiating):
    with app.app_context():
        # Retrieve the user by email
        print(email)
        user = User.query.filter(User.emailId ==email).first()
        if user:
            user.isOfficiating = is_officiating
            db.session.commit()

def schedule_hod_dates(email, start_date, end_date):
    with app.app_context():
        # Schedule action for start date
        # print("reached scheduler")
        # print(datetime.now())
        # print(datetime.strptime(start_date, '%Y-%m-%d'))
        # print(datetime.strptime(end_date, '%Y-%m-%d'))
        run_time = datetime.strptime(start_date, '%Y-%m-%d')
        run_time1 = datetime.strptime(end_date, '%Y-%m-%d')
        scheduler.add_job(
            func=update_officiating_hod,
            args=(email, True),  # Set officiating_hod to True
            trigger=DateTrigger(run_date=run_time + timedelta(minutes=1)),
            id=f"start_date_{email}",
        )

        # Schedule action for end date
        scheduler.add_job(
            func=update_officiating_hod,
            args=(email, False),  # Set officiating_hod to False
            trigger=DateTrigger(run_date=run_time+ timedelta(minutes=2) ),
            id=f"end_date_{email}",
        )

@app.route('/officiatinghod', methods=['POST'])
def officiatinghod():
    data = json.loads(request.form['json'])
    email = data.get('Email')
    startdate = data.get('startdate')
    enddate = data.get('enddate')
    # print("reached off")
    schedule_hod_dates(email,startdate,enddate)

    return 'Scheduled', 200

# @app.route("/", defaults={'path': ''})
# @app.route("/<path:path>")
# def serve(path):
#     frontend_dir = os.path.join(os.path.dirname(__file__), '..', 'dep-frontend')
#     return send_from_directory(frontend_dir, 'index.html')


@app.route("/")
def fronend():
    print("hi")
    return send_from_directory("static1", "index.html")

@app.route("/home")
def home():
    return "You r home"


class UserView(ModelView):
    column_list = ('id', 'firstName', 'lastName', 'emailId', 'hometown', 'designation', 'payLevel', 'roleId', 'role', 'dateOfJoining', 'department', 'ltcInfos', 'signUrl')
    form_columns = ('firstName', 'lastName', 'emailId', 'hometown', 'designation', 'payLevel', 'role', 'dateOfJoining', 'department', 'ltcInfos', 'signUrl')
    form_overrides = {
        'signUrl': ImageUploadField
    }
    
    form_args = {
        'signUrl': {
            'label': 'Image',
            'base_path': os.path.join(os.path.dirname(__file__), 'uploads'),
            'url_relative_path': 'uploads'
        }
    }


class RoleView(ModelView):
    column_list = ('id', 'roleName', 'stageCurrent', 'nextStage', 'prevStage')
    form_columns = ('id', 'roleName', 'stageCurrent', 'nextStage', 'prevStage')

admin.add_view(UserView(User, db.session))
admin.add_view(RoleView(Role, db.session))
admin.add_view(ModelView(LTCInfo, db.session))
admin.add_view(ModelView(TAInfo, db.session))

scheduler.add_job(
    func=sendReminders,
    trigger=CronTrigger.from_crontab("0 0 * * *"),  # run at midnight every day
)
# run_time = datetime.now() + timedelta(minutes=3)
# scheduler.add_job(
#     func=sendReminders,
#     trigger=DateTrigger(run_date=run_time),  # Run immediately for testing
# )

# if (__name__ == "__main__"):
#     app.run(debug=True, port=5000)
export_app=app
