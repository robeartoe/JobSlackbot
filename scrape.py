from Queue import Queue

from indeed.EZIndeed import EZIndeed
from workers import craigslistWorker, indeedWorker, slackPostWorkerCL, slackPostWorkerIN
from craigslist import CraigslistJobs
from slackclient import SlackClient
from settings import JobKeywords,cities,jobCategorys,want_internship,Craigslistcities,areas,useIndeed,useCraigslist,resultNumber,slackToken,indeedToken

from main import db
from models import Listing

def scrape_area_indeed(keyword,searchcity):
    #Can use JobKey to see whether or not it's in the database
    RESULTS = []
    api = EZIndeed(indeedToken)
    json_results = api.search(keyword=keyword,limit =1, location = searchcity, full = True)

    for result in json_results['results']:
        listing = Listing.query.filter_by(JobKeyOrID = result["jobkey"]).first()
        #If the listing already exist. Don't add it again.
        if listing is None:
        #If it does not exist. Get in more detail with it.
            #Create Listing Object:
            listing = Listing(
                link = result["url"],
                created = result["date"],
                name = result["company"],
                title = result['jobtitle'],
                location = result["formattedLocationFull"],
                JobKeyOrID = result["jobkey"],
                city = searchcity
            )
            #Save Session:
            try:
                db.session.add(listing)
                db.session.commit()
                db.session.close()
            except Exception as inst:
                print(inst)
                print("Error DB")
            RESULTS.append(result)
    return RESULTS

def scrape_area_jobs(area,searchcity,jobcategory):
    cl_j = CraigslistJobs(site = searchcity, area = area, category = jobcategory,
                            filters={'is_internship': want_internship})
    genJ = cl_j.get_results(sort_by = 'newest', geotagged = True, limit = resultNumber)
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
                JobKeyOrID = result['id']
            )
            #Save Session:
            try:
                db.session.add(listing)
                db.session.commit()
                db.session.close()
            except Exception as inst:
                print(inst)
                print("Error DB")
            RESULTS.append(result)
    return RESULTS

#This function will start the scraper. And post to slack.
def do_scrape():
    #Create a slack client
    sc = SlackClient(slackToken)
    allIndeedResults = {}
    allCraigslistResults = {}
    #Get all the results from craigslist
    #This will iterate through areas, in settings.
    Jobthreads = []
    slackThreads = []


    # THIS IS CRAIGSLIST:
    #For loop for cities, and for loop for the areas in said cities
    if useCraigslist:
        jobQueue = Queue()
        slackQueue = Queue()
        for i in range(4):
            worker = craigslistWorker(jobQueue)
            Jobthreads.append(worker)
            worker.daemon = True
            worker.start()
            slackWorker = slackPostWorkerCL(slackQueue)
            slackThreads.append(slackWorker)
            slackWorker.daemon = True
            slackWorker.start()

        for city in Craigslistcities:
            allCraigslistResults[city] = []
            for area in areas[city]:
                for jobcategory in jobCategorys:
                    jobQueue.put((area,city,jobcategory))

            for worker in Jobthreads:
                threadResults = worker.join()
                for result in threadResults:
                    allCraigslistResults[city].append(result)
                    slackQueue.put((sc,city,result))
            for worker in slackThreads:
                worker.join()
            Jobthreads *= 0
            slackThreads *= 0

            foundString = "Found: {} results for : {} ".format(len(allCraigslistResults[city]),city)
            print(foundString)

    # THIS IS INDEED:
    if useIndeed:
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

        for city in cities:
            allIndeedResults[city] = []
            for keyword in JobKeywords:
                jobQueue.put((keyword,city))
            for worker in Jobthreads:
                threadResults = worker.join()
                for result in threadResults:
                    allIndeedResults[city].append(result)
                    slackQueue.put((sc,city,result))
            Jobthreads *= 0
            for worker in slackThreads:
                worker.join()

            testString = "Found: {} results for : {} ".format(len(allIndeedResults[city]),city)
            print(testString)
