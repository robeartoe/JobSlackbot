#---------------------------------------------------------------------------------------------#
#Searches through craigslist for python internships in LA and LA areas
#And also a slackbot to send to my slackchat ... which I need to make.

#To include: Add indeed.com; Add apartment; Add NY, Seattle, and SF;
#Add distance from apartment and job (and possibly transit?).

#---------------------------------------------------------------------------------------------#
from scrape import do_scrape
import time
import traceback
import sys
from settings import SLEEP_INTERVAL
# Let's make this simple. Two cities. NYC AND LA. Search Jobs. Post on Slack. GG EZ.

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
"""
for x in jobCategorys:
    cLJobsDowntownLA = CraigslistJobs(site='losangeles' , category = x, filters={'is_internship': want_internship, })
    results = cLJobsDowntownLA.get_results(sort_by ='newest', geotagged = True , limit = 10)
    print("The current category is ")
    print (x)
    for result in results:
        print(result)
"""
