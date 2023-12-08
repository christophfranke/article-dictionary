import schedule
import sys
import time
from datetime import datetime
import statistics
import dictionary
import articles

# wait a minute
# time.sleep(60)
print("Scheduler Running")

# create_statistics()
schedule.every(2).hours.do(statistics.jobs)
schedule.every(10).seconds.do(dictionary.jobs)
schedule.every(60).seconds.do(articles.jobs)

while True:
    schedule.run_pending()
    time.sleep(1)
    sys.stdout.flush()
