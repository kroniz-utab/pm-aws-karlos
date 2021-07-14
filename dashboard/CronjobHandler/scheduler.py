from apscheduler.schedulers.background import BackgroundScheduler
from .iot_puller import coba_update
from .email_test import html_email
from .full_job import testing

job_defaults = {
    'coalesce': False,
    'max_instances': 3
}

def start():
    scheduler = BackgroundScheduler(job_defaults=job_defaults)
    # scheduler.add_job(coba_update, 'cron', minute='*/5')
    # scheduler.add_job(html_email, 'cron', minute='*/2')
    # scheduler.add_job(coba_update, 'cron', minute='2-52/10') # Job for gathering from Iot
    # scheduler.add_job(html_email, 'cron', minute='53', hour='23') # Job for send email report
    scheduler.add_job(testing, 'cron', minute='*/1')
    scheduler.start()
