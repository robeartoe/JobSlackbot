from queue import Queue
from threading import Thread

class slackPostWorkerIN(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get parameters from tuple:

            # Perform Slack Post:

            # Update Queue:
            pass



class indeedWorker(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
            # Get parameters from tuple:

            # Perform Slack Post:

            # Update Queue:
            pass

class slackPostWorkerCL(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get parameters from tuple:
            sc, city, result = self.queue.get()
            # Perform Slack Post:
            from util import postFromCraiglist
            postFromCraiglist(sc=sc,city=city,listing=result)
            # Update Queue:
            self.queue.task_done()

class craigslistWorker(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue
        self.RESULTS = []

    def run(self):
        while True:
            # Get parameters from tuple:
            area, city, jobC = self.queue.get()
            # Search Craigslist:
            from scrape import scrape_area_jobs
            self.RESULTS.append(scrape_area_jobs(area=area, searchcity=city, jobcategory=jobC))
            # Update Queue:
            self.queue.task_done()
    def join(self):
        self.queue.join()
        return self.RESULTS

    def returnResults(self):
        return self.RESULTS
