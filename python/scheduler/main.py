import schedule
import sys
import time
from datetime import datetime
from statistics import create_statistics
from dictionary import do_jobs

# wait a minute
time.sleep(60)
print("Scheduler Running")

create_statistics()
schedule.every(2).hours.do(create_statistics)
schedule.every(5).seconds.do(do_jobs)

while True:
    schedule.run_pending()
    time.sleep(1)
    sys.stdout.flush()
