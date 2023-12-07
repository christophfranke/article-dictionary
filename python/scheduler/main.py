import schedule
import sys
import time
from datetime import datetime
from statistics import create_statistics
from repair import repair

# wait a minute
time.sleep(60)
print("Scheduler Running")

create_statistics()
schedule.every(2).hours.do(create_statistics)
schedule.every(60).seconds.do(repair)

while True:
    schedule.run_pending()
    time.sleep(1)
    sys.stdout.flush()
