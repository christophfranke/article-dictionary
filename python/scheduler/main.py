from apscheduler.schedulers.blocking import BlockingScheduler
import time
import sys
import os

import statistics
import dictionary
import articles
import cluster
import user
import database


def run(debug=False):
    # make an initial export
    if not debug:
        # wait until the database is up
        time.sleep(5)
        database.export()
    else:
        time.sleep(2)

    # dictionary.reset_clusters()
    # dictionary.add_missing_words()
    # dictionary.reset_word_frequency()
    # cluster.update_aggregate_attributes()

    # statistics.jobs()
    # user.jobs()
    # articles.jobs()
    # dictionary.jobs()

    # statistics.repair()
    # user.repair()
    # articles.repair()
    # dictionary.repair()

    # Initialize the scheduler
    scheduler = BlockingScheduler()

    # Schedule your tasks with more readable intervals
    scheduler.add_job(statistics.jobs, 'interval', hours=1, id='statistics_jobs')
    scheduler.add_job(dictionary.jobs, 'interval', seconds=1, id='dictionary_jobs')
    scheduler.add_job(dictionary.lazy_jobs, 'interval', minutes=1, id='dictionary_lazy_jobs')
    scheduler.add_job(cluster.jobs, 'interval', seconds=30, id='cluster_jobs')
    scheduler.add_job(articles.jobs, 'interval', seconds=15, id='articles_jobs')
    scheduler.add_job(database.jobs, 'interval', hours=12, id='database_jobs')

    scheduler.add_job(dictionary.repair, 'interval', hours=2.7, id='dictionary_repair')
    scheduler.add_job(articles.repair, 'interval', hours=3.1, id='articles_repair')
    scheduler.add_job(user.repair, 'interval', hours=5.3, id='user_repair')

    # Start the scheduler
    try:
        print(f"Scheduler is running (Debug={debug})")
        scheduler.start()
    except KeyboardInterrupt:
        # Handle the shutdown gracefully
        print("Shutting down...")
        scheduler.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    debug = os.getenv('DEBUG', False)
    run(debug)
