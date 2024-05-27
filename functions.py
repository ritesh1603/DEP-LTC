from models import User, LTCInfo,TAInfo, db, Notification, Receipt, Role
from flask import request
import uuid, mimetypes, json, os
from helper import remindStakeholder
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger
from datetime import datetime
# from app import app
# scheduler = BackgroundScheduler()
# scheduler.start()

def checkEmail(emailId):
    foundUser = User.query.filter(User.emailId == emailId).first()
    return foundUser

def createNewLTCApplication(userInfo, formInfo):
    formInfo['userId'] = userInfo.id
    info = LTCInfo(formInfo)
    for file in request.files.getlist('file'):
        fileName = uuid.uuid4().hex + mimetypes.guess_extension(file.mimetype)
        base_path = os.path.join(os.path.dirname(__file__), 'receipts')
        filePath = f"{base_path}/{fileName}"
        info.receipts.append(Receipt(filePath))
        print(file.save(filePath))

    db.session.add(info)
    db.session.commit()
    print("JSON LTCINFO", info.json())
    return info

def approvedltclist(userInfo):
    # Assuming User and LtcInfo are the correct model names
    all_ltc_infos =  LTCInfo.query.all()
    user = User.query.filter(User.id == userInfo.id).first()
    live_ltc = filter(lambda ltc: ltc.stageCurrent != 0 
                                  and ltc.stageCurrent <= 101 
                                  and ltc.stageCurrent > user.roleId,
                      all_ltc_infos)
    return list(live_ltc)

def approvedtalist(userInfo):
    # Assuming User and LtcInfo are the correct model names
    all_ta_infos = TAInfo.query.all()
    user = User.query.filter(User.id == userInfo.id).first()
    live_ta = filter(lambda ta: ta.stageCurrent != 0 
                                  and ta.stageCurrent <= 101 
                                  and ta.stageCurrent > user.roleId,
                      all_ta_infos)
    return list(live_ta)

def listLiveApplications(userInfo):
    liveLtc = filter(lambda ltc: ltc.stageCurrent <= 100, User.query.filter(User.id==userInfo.id).first().ltcInfos)
    return list(liveLtc)

def listDoneLTCApplications(userInfo):
    liveLtc = filter(lambda ltc: ltc.stageCurrent == 100, User.query.filter(User.id==userInfo.id).first().ltcInfos)
    return list(liveLtc)

def listLiveTAApplications(userInfo):
    # add Stage current here
    liveTa = filter(lambda ta: ta.stageCurrent <= 100, User.query.filter(User.id==userInfo.id).first().taInfos)
    return list(liveTa)


def addNotification(userId, message):
    user = User.query.filter(User.id == userId).first()
    user.notifications.append(Notification(message))
    db.session.commit()

# def update_officiating_hod(email, is_officiating):
#     # Retrieve the user by email
#     print(email)
#     user = User.query.filter_by(email=email).first()
#     if user:
#         user.isOfficiating = is_officiating
#         db.session.commit()

# def schedule_hod_dates(email, start_date, end_date):
#     # Schedule action for start date
#     print("reached scheduler")
#     print(datetime.now())
#     print(datetime.strptime(start_date, '%Y-%m-%d'))
#     print(datetime.strptime(end_date, '%Y-%m-%d'))
#     scheduler.add_job(
#         func=update_officiating_hod,
#         args=(email, True),  # Set officiating_hod to True
#         trigger=DateTrigger(start_date),
#         id=f"start_date_{email}",
#     )

#     # Schedule action for end date
#     scheduler.add_job(
#         func=update_officiating_hod,
#         args=(email, False),  # Set officiating_hod to False
#         trigger=DateTrigger(end_date),
#         id=f"end_date_{email}",
#     )
# def sendReminders():
#     with app.app_context():
#         a = [j for j in LTCInfo.query.filter(
#             LTCInfo.stageCurrent != 0 and LTCInfo.stageCurrent < 100).all()]
#         # f = filter(lambda j: (datetime.now() - j.lastForwardDate).days > 3, a)
#         print("reached reminders")
#         f = filter(lambda j: (datetime.now() - j.lastForwardDate).total_seconds() > 120, a)
#         forms = [{'firstName': x.user.firstName, 'lastName': x.user.lastName, 'delay': (
#             datetime.now() - x.lastForwardDate).days, 'stageCurrent': x.stageCurrent, 'id': x.id} for x in f]

#         for form in forms:
#             role = Role.query.filter(
#                 Role.stageCurrent == form['stageCurrent']).first()
#             emails = [user.emailId for user in User.query.filter(
#                 User.roleId == role.id)]
#             for email in emails:
#                 form['email'] = email
#                 print(form)
#                 remindStakeholder(form)
