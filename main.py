#---------------------------------------------------------------------------------------------#
# To-Do: Change from sleeping with a time interval, and instead quit upon completion. That way, I could have it run at timed intervals.
#---------------------------------------------------------------------------------------------#
from scrape import do_scrape
import time
import traceback
import sys
from settings import SLEEP_INTERVAL

if __name__ == "__main__":
    while True:
            print("{} : Starting scrape cycle".format(time.ctime()))
            try:
                do_scrape()
            except KeyboardInterrupt:
                print("Exiting...")
                sys.exit(1)
            except Exception as exc:
                print("Error with scraping".format(time.ctime()))
                traceback.print_exc()
            else:
                    print("{}: Finished scraping with no issues".format(time.ctime()))
            time.sleep(SLEEP_INTERVAL)
