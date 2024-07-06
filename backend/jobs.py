from datetime import date, timedelta
from flask import current_app, render_template
from flask_mail import Message, Mail
from website import create_app
from website.models import User, LastLogin, Bookings
from celery import Celery
from celery.schedules import crontab

celery = Celery(
    'jobs',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery.task
def send_daily_emails():
    app = create_app() 
    with app.app_context(): 
        users_to_notify = get_users_to_notify()
        with app.test_request_context(): 
            for user in users_to_notify:
                send_email_to_user(user.email)

def get_users_to_notify():
    today = date.today()
    users_last_login = User.query.outerjoin(LastLogin, User.id == LastLogin.user_id).filter((LastLogin.lastlogin < today) | (LastLogin.lastlogin == None)).all()
    return users_last_login

def send_email_to_user(email):
    sender = '201aashish@gmail.com'
    subject = 'Where are you? LogIn to TICKETIFY!'
    html_body = render_template("daily.html")
    msg = Message(subject=subject, sender=sender, recipients=[email], html=html_body)

    with current_app.app_context():
        mail = Mail(current_app)
        mail.send(msg)
    return 'Email Sent Successfully'

def monthly_report_mailer(user, bookings):
    sender = '201aashish@gmail.com'
    subject = 'Your Monthly Entertainment Report - Ticketify Reg.'
    if bookings == None:
        html_body = render_template("no_bookings.html")
        msg = Message(subject=subject, sender=sender, recipients=[user.email], html=html_body)
        with current_app.app_context():
            mail = Mail(current_app)
            mail.send(msg)
        return 'Email Sent Successfully'
    html_body = render_template('monthly.html',user=user, bookings = bookings)
    msg = Message(subject=subject, sender=sender, recipients=[user.email], html=html_body)
    with current_app.app_context():
        mail = Mail(current_app)
        mail.send(msg)
    return 'Email Sent Successfully'


@celery.task
def monthly_mail_sender():
    app = create_app() 
    with app.app_context(): 
        users = User.query.filter_by(role='user').all()
        with app.test_request_context(): 
            for user in users:
                bookings = get_user_monthly_bookings(user)
                monthly_report_mailer(user, bookings)

def get_user_monthly_bookings(user):
    today = date.today()
    last_month = today - timedelta(days=30)
    bookings = Bookings.query.filter_by(user_id=user.id).filter(Bookings.date_time >= last_month).all()
    return bookings


celery.conf.beat_schedule = {
    'send-daily-emails': {
        'task': 'jobs.send_daily_emails', 
        'schedule': crontab(hour=8, minute=24),
    },
    'send-monthly-emails': {
        'task': 'jobs.monthly_mail_sender', 
        'schedule': crontab(day_of_month=1, hour=10, minute=0),
    },
}
