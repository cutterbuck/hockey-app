from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
import pytz
from package.etl.etl import run_standings_auto_update


# def append_myself_to_contracts_csv():
#     import csv, os
#     new_row_dict = dict(player="Jake MacNaughton",team="NYR",salary=5000000,cap_hit=5000000)
#     file_str = os.getcwd() + '/package/data/contracts.csv'
#     with open(file_str, 'a', newline='') as f:
#         print("appending myself to contracts.csv")
#         writer = csv.DictWriter(f, fieldnames=new_row_dict.keys())
#         writer.writerow(new_row_dict)


def start_running_schedules():
    print("Starting schedules")
    now = datetime.now()
    sched = BackgroundScheduler(daemon=True)
    trigger = CronTrigger(year="*", month="*", day="*", hour="3", minute="0", second="0")
    sched.add_job(run_standings_auto_update, trigger=trigger, start_date=now, timezone=pytz.timezone("America/New_York"))
    # sched.add_job(append_myself_to_contracts_csv, 'interval', minutes=1, start_date=now, end_date=datetime(now.date().year, now.date().month, now.date().day, 15, 49, 1), timezone=pytz.timezone("America/New_York"))
    sched.start()