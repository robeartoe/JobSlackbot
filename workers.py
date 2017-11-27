from threading import Thread

class indeedWorker(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue
        self.RESULTS = []
    def run(self):
        while True:
            # Get parameters from tuple:
            keyword,searchcity = self.queue.get()
            # Perform Slack Post:
            from scrape import scrape_area_indeed
            self.RESULTS.extend(scrape_area_indeed(keyword=keyword,searchcity=searchcity))
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
            sc, city, result = self.queue.get()
            # Perform Slack Post:
            from util import postFromIndeed
            postFromIndeed(sc,city,result)
            # Update Queue:
            self.queue.task_done()
    def join(self):
        self.queue.join()

class slackPostWorkerCL(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get parameters from tuple:
            sc, city, listing = self.queue.get()
            # Perform Slack Post:
            from util import postFromCraiglist
            postFromCraiglist(sc=sc,city=city,listing=listing)
            # Update Queue:
            self.queue.task_done()
    def join(self):
        self.queue.join()

class craigslistWorker(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get parameters from tuple:
            area, city, jobC = self.queue.get()
            # Search Craigslist:
            from scrape import scrape_area_jobs
            self.RESULTS = scrape_area_jobs(area=area, searchcity=city, jobcategory=jobC)
            # Update Queue:
            self.queue.task_done()
    def join(self):
        self.queue.join()
        return self.RESULTS
