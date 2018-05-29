from threading import Thread

class indeedWorker(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue
        self.RESULTS = {}
    def run(self):
        while True:
            # Get parameters from tuple:
            keyword,searchcity,query = self.queue.get()
            # Perform Slack Post:
            from scrape import scrape_area_indeed
            self.RESULTS['result'] = (scrape_area_indeed(keyword=keyword,searchcity=searchcity))
            self.RESULTS['query'] = query
            # Update Queue:
            self.queue.task_done()
    def join(self):
        self.queue.join()
        return self.RESULTS

class slackPostWorkerIN(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
            # Get parameters from tuple:
            sc, listings, inRow = self.queue.get()
            # Perform Slack Post:
            from util import postFromIndeed
            postFromIndeed(sc,listings,inRow)
            # Update Queue:
            self.queue.task_done()
    def join(self):
        self.queue.join()
# --------------------------------------------------------#
# Craigslist:

class slackPostWorkerCL(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue
    def run(self):
        while True:
            # Get parameters from tuple:
            sc,listing,query = self.queue.get()
            # Perform Slack Post:
            from util import postFromCraiglist
            postFromCraiglist(sc=sc,listings=listing,clRow=query)
            # Update Queue:
            self.queue.task_done()
    def join(self):
        self.queue.join()

class craigslistWorker(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue
        self.RESULTS = {}
    def run(self):
        while True:
            # Get parameters from tuple:
            area, city, jobC,internship,query = self.queue.get()
            # Search Craigslist:
            from scrape import scrape_area_jobs
            self.RESULTS['result'] = scrape_area_jobs(area=area, searchcity=city, jobcategory=jobC,internship=internship)
            self.RESULTS['query'] = query
            # Update Queue:
            self.queue.task_done()
    def join(self):
        self.queue.join()
        return self.RESULTS
