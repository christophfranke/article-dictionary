import schedule
import sys
import time
from datetime import datetime
import statistics
import dictionary
import articles
import user


# statistics.jobs()
# user.jobs()
# articles.repair()
# dictionary.jobs()
schedule.every(1).hours.do(statistics.jobs)
schedule.every(1).seconds.do(dictionary.jobs)
schedule.every(1).minutes.do(articles.jobs)

schedule.every(0.7).hours.do(dictionary.repair)
schedule.every(1.1).hours.do(articles.repair)
schedule.every(5.3).hours.do(user.repair)

print("Scheduler is running")

while True:
    schedule.run_pending()
    time.sleep(1)
    sys.stdout.flush()
