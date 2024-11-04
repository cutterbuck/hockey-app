from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
from package.etl.etl import get_standings



def print_hello_world():
    print('Hello world! Time is', datetime.now())

def start_running_schedules():
    now = datetime.now()
    sched = BackgroundScheduler(daemon=True)
    trigger = CronTrigger(year="*", month="*", day="*", hour="11", minute="0", second="0")
    sched.add_job(get_standings, trigger=trigger, start_date=now, timezone=pytz.timezone("America/New_York"))
    # sched.add_job(print_hello_world, 'interval', minutes=1, start_date=now, end_date=datetime(now.date().year, now.date().month, now.date().day, 23, 59), timezone=pytz.timezone("America/New_York"))
    sched.start()
