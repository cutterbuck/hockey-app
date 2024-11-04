from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
from package.etl.etl import run_standings_auto_update



def print_hello_message():
    print("Hello world!")

def start_running_schedules():
    print("Starting schedules")
    now = datetime.now()
    sched = BackgroundScheduler(daemon=True)
    trigger = CronTrigger(year="*", month="*", day="*", hour="19", minute="20", second="0")
    sched.add_job(print_hello_message, trigger=trigger, start_date=now, timezone=pytz.timezone("America/New_York"))
    sched.start()