# scheduler.py
import os
import time

import schedule


def cleanup_worksdata_job():
    os.system('python manage.py cleanup_worksdata')

# Schedule the job to run daily at midnight
schedule.every().day.at('00.00').do(cleanup_worksdata_job)

while True:
    schedule.run_pending()
    time.sleep(1)
