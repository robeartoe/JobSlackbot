from queue import Queue
from threading import Thread
from scrape import scrape_area_jobs , scrape_area_indeed

class slackPostWorker(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get parameters from tuple:

            # Perform Slack Post:

            # Update Queue:

class indeedWorker(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
            # Get parameters from tuple:

            # Perform Slack Post:

            # Update Queue:

class craigslistWorker(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue
        
        # Make a RESULTS list here.
        # Then when it's time to join. Join them here.
        # At scrape.py, make allCraigslistResults[ciyt] = RESULTS (The results here.)

    def run(self):
        while True:
            # Get parameters from tuple:
            area, city, jobC = self.queue.get()
            # Search Craigslist:
            scrape_area_jobs(area=area, searchcity=city, jobcategory=jobC)
            # Update Queue:
            self.queue.task_done()
