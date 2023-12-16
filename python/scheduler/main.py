import schedule
import sys
import time
from datetime import datetime
import statistics
import dictionary
import articles
import user

# wait until the database is up
time.sleep(5)

# dictionary.reset_clusters()
# dictionary.add_missing_words()
# dictionary.reset_word_frequency()

# statistics.jobs()
# user.jobs()
# articles.jobs()
# dictionary.jobs()

# statistics.repair()
# user.repair()
# articles.repair()
# dictionary.repair()

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
