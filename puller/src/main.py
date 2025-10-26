import time
import logging
from datetime import datetime

from config import config
from TLE_pulling import main

def job():
    main()

def get_current_hour():
    return datetime.now().hour

while True:
    try:
        current_hour = (get_current_hour() + 3) % 24 # +3 hours because of utc difference
        if current_hour == 7:
            logging.info(f"I woke up, time to pull: {datetime.now().time()} (3 hours difference)")
            job()
            logging.info(f"I did my job, it's time to sleep again, time: {datetime.now().time()} (3 hours difference)")
        else:
            logging.info(f"Going to sleep again... time: {datetime.now().time()} (3 hours difference)")
        
        time.sleep(int(config["sleeping_time_in_seconds"]))
    except Exception as e:
        logging.error(f"Error while running script: {e}")