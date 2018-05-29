# TODO: Edit Scrape.py
from Queue import Queue

from indeed.EZIndeed import EZIndeed
from workers import craigslistWorker, indeedWorker, slackPostWorkerCL, slackPostWorkerIN
from craigslist import CraigslistJobs
from slackclient import SlackClient
from settings import JobKeywords,cities,jobCategorys,want_internship,Craigslistcities,areas,useIndeed,useCraigslist,resultNumber,slackToken,indeedToken

from main import db
from models import Listing,Settings,indeedModel,craigslistModel

def scrape_area_indeed(keyword,searchcity):
    #Can use JobKey to see whether or not it's in the database
    RESULTS = []
    api = EZIndeed(indeedToken)
    EZIndeedResults = api.search(keyword=keyword,limit = 3, location = searchcity)

    for result in EZIndeedResults:
        listing = Listing.query.filter_by(JobKeyOrID = result.jobkey).first()
        #If the listing already exist. Don't add it again.
        if listing is None:
        #If it does not exist. Get in more detail with it.
            #Create Listing Object:
            listing = Listing(
                link = result.url,
                created = result.date,
                name = result.company,
                title = result.jobtitle,
                location = result.date,
                JobKeyOrID = result.jobkey,
                city = searchcity,
                InorCl = "IN"
            )
            #Save Session:
            try:
                RESULTS.append(listing)
                db.session.add(listing)
                db.session.commit()
            except Exception as inst:
                print(inst)
                print("Error DB")
                db.session.rollback()
    return RESULTS

def scrape_area_jobs(area,searchcity,jobcategory,internship):
    cl_j = CraigslistJobs(site = searchcity, area = area, category = jobcategory,
                            filters={'is_internship': internship})
    genJ = cl_j.get_results(sort_by = 'newest', geotagged = True, limit = 2)
    RESULTS = []
    while True:
        try:
            result = next(genJ)
        except StopIteration:
            break
        except Exception:
            continue
        listing = Listing.query.filter_by(JobKeyOrID = result["id"]).first()
        if listing is None:
            # Create Listing Object:
            listing = Listing(
                link = result["url"],
                created = result["datetime"],
                name = result["name"],
                location = result["where"],
                city = searchcity,
                JobKeyOrID = result['id'],
                InorCl = "CL"
            )
            #Save Session:
            try:
                RESULTS.append(listing)
                db.session.add(listing)
                db.session.commit()
            except Exception as inst:
                print(inst)
                print("Error DB")
                db.session.rollback()
    return RESULTS

#This function will start the scraper. And post to slack.
def do_scrape():
    #Create a slack client
    sc = SlackClient(slackToken)

    settings = Settings.query.get(1)

    Jobthreads = []
    slackThreads = []

    # THIS IS CRAIGSLIST:
    if settings.craigslist:
        numResults = 0
        jobQueue = Queue()
        slackQueue = Queue()
        resultQueue = Queue()
        for i in range(4):
            worker = craigslistWorker(jobQueue)
            Jobthreads.append(worker)
            worker.daemon = True
            worker.start()

            slackWorker = slackPostWorkerCL(slackQueue)
            slackThreads.append(slackWorker)
            slackWorker.daemon = True
            slackWorker.start()

        clQueries = craigslistModel.query.all()
        for query in clQueries:
            jobQueue.put((query.area,query.city,query.category,query.internship,query))
        for worker in Jobthreads:
            results = worker.join()
            if results:
                slackQueue.put((sc,results['result'],results['query']))
                foundString = "Found: {} results for : {} ".format(len(results['result']),results['query'].city)
                print(foundString)
        for worker in slackThreads:
            worker.join()

        Jobthreads *= 0
        slackThreads *= 0

    # THIS IS INDEED:
    if settings.indeed:
        jobQueue = Queue()
        slackQueue = Queue()
        for i in range(4):
            worker = indeedWorker(jobQueue)
            Jobthreads.append(worker)
            worker.daemon = True
            worker.start()

            worker = slackPostWorkerIN(slackQueue)
            slackThreads.append(worker)
            worker.daemon = True
            worker.start()

        inQueries = indeedModel.query.all()
        for query in inQueries:
            jobQueue.put((query.keyword,query.city,query))

        for worker in Jobthreads:
            results = worker.join()
            if results:
                slackQueue.put((sc,results['result'],results['query']))
                testString = "Found: {} results for : {} ".format(len(results['result']),results['query'].city)
                print(testString)
        for worker in slackThreads:
            worker.join()
    db.session.close()
