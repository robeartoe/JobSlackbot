import requests

class EZIndeed(object):
    """docstring for EZIndeed."""
    def __init__(self, publisherID):
        self.publisherID = publisherID
        self.baseURL = "http://api.indeed.com/ads/"
        self.searchResults = None

    def search(self,keyword=None,limit = None,location = 'US',countryCode = 'us',full = False): #By DEFAULT location and countryCode is us. BUT it can be changed. Take note!
        if limit is None:
            limit = 5
        SearchURL = self.baseURL + "apisearch"
        dataSet = {'q':keyword,'l':location,'co':countryCode,'format':'json','v':'2','publisher':self.publisherID ,'limit': limit}
        r = requests.get(SearchURL,params = dataSet)
        data = r.json()
        self.searchResults = data
        if full == True:
            return data
        jobs = []
        for result in range(len(data['results'])):
            job = JobListing(data['results'][result])
            jobs.append(job)
        return jobs

    def jobDetails(self,job):
        jobkey = job.jobkey
        JobDetailURL = self.baseURL + "apigetjobs"
        r = requests.get(JobDetailURL,params={'publisher':self.publisherID,'jobkeys':jobkey,'v':'2','format':'json'})
        data = r.json()
        data = data['results'][0]
        jobDetail = JobListing(data)
        return jobDetail

    def __repr__(self):
        return '<EZIndeed Object>'
    def __str__(self):
        return self.searchResults

class JobListing(object):
    def __init__(self,job):
        self.result = job
        self.jobkey = job['jobkey']
        self.jobtitle = job['jobtitle']
        self.company = job['company']
        self.snippet = job['snippet']
        self.RelativeTime = job['formattedRelativeTime']
        self.date = job['date']
        self.city = job['city']
        self.url = job['url']

    def __repr__(self):
        return '<JobListing Object>'
    def __str__(self):
        return str(self.result)
