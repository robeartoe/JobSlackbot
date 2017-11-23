from scrape import do_scrape
import time
import traceback
import sys
from settings import SLEEP_INTERVAL

if __name__ == "__main__":
    starttime = time.time()
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
            print("{} Amount of time it took to complete.".format(time.time() - starttime))
