import schedule
import sys
import time
from datetime import datetime
from statistics import create_statistics
from repair import repair_word

# wait a minute
# time.sleep(60)
print("Scheduler Running")

# create_statistics()
schedule.every(12).hours.do(create_statistics)
schedule.every(2).seconds.do(repair_word)

while True:
    schedule.run_pending()
    time.sleep(1)
    sys.stdout.flush()
