import schedule
import sys
import time
from datetime import datetime
from statistics import create_statistics

print("Scheduler Running")

schedule.every(12).hours.do(create_statistics)
# schedule.every(5).seconds.do(create_statistics)

create_statistics()
while True:
    schedule.run_pending()
    time.sleep(1)
    sys.stdout.flush()
