from apscheduler.schedulers.background import BackgroundScheduler
from .iot_puller import coba_update
from .email_report import html_email

def start():
    scheduler = BackgroundScheduler()
    # scheduler.add_job(coba_update, 'cron', minute='*/5')
    # scheduler.add_job(html_email, 'cron', minute='*/9')
    # scheduler.add_job(coba_update, 'cron', minute='*/10') # Job for gathering from Iot
    # scheduler.add_job(html_email, 'cron', minute='2', hour='0') # Job for send email report
    scheduler.start()