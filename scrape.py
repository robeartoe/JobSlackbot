import time
from workers import craigslistWorker, indeedWorker, slackPostWorker
# from multiprocessing import pool
# from functools import partial

from indeed.EZIndeed import EZIndeed, JobListing

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker

from craigslist import CraigslistJobs
from slackclient import SlackClient
from config.private import token, SLACK_TOKEN
from util import postFromIndeed,postFromCraiglist
from settings import JobKeywords,cities,jobCategorys,want_internship,Craigslistcities,areas,useIndeed,useCraigslist,resultNumber


engine = create_engine('sqlite:///listings.db', echo=False)

Base = declarative_base()

class Listing(Base):
    """
    Hold all types of data on listing.
    """
    __tablename__ = 'listings'

    id = Column(Integer , primary_key = True)
    link = Column(String, unique = True) #'url' for both Indeed and Craigslist
    created = Column(String) #'date' for Indeed and 'datetime' for Craigslist
    name = Column(String,nullable = True) #'company' Name Only for Indeed
    title = Column(String) # 'jobtitle' for Indeed and and 'name' forCraigslist
    location = Column(String) #'formattedLocation', and 'where' for craigslist
    city = Column(String) #Los Angeles or New York
    JobKeyOrID = Column(String, unique=True) #'jobkey' for Indeed and 'id' for Craigslist

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def scrape_area_indeed(keyword,searchcity):
    #Can use JobKey to see whether or not it's in the database
    RESULTS = []
    api = EZIndeed(token)
    json_results = api.search(keyword=keyword, location = searchcity, full = True)

    for result in json_results['results']:
        listing = session.query(Listing).filter_by(JobKeyOrID = result["jobkey"]).first()
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
            session.add(listing)
            session.commit()
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
        listing = session.query(Listing).filter_by(JobKeyOrID=result["id"]).first()
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
            session.add(listing)
            session.commit()
            RESULTS.append(result)
    return RESULTS

#This function will start the scraper. And post to slack.
def do_scrape():
    #Create a slack client
    sc = SlackClient(SLACK_TOKEN)
    allIndeedResults = {}
    allCraigslistResults = {}
    #Get all the results from craigslist
    #This will iterate through areas, in settings.
    jobQueue = Queue()
    slackQueue = Queue()

    for i in range(2):
        worker = slackPostWorker(jobQueue)
        worker.daemon = True
        worker.start()


    for i in range(2):
        t = Thread(target=postFromCraiglist,args=(sc,result,city,))
        t.start()

    # THIS IS CRAIGSLIST:
    #For loop for cities, and for loop for the areas in said cities
    if useCraigslist:
        for city in Craigslistcities:
            allCraigslistResults[city] = []

            for area in areas[city]:
                for jobcategory in jobCategorys:
                    # Threading:
                    jobQueue.put((area,city,jobcategory))
                    # allCraigslistResults[city].append(scrape_area_jobs(area,city,jobcategory))



            testString = "Found: {} results for this city: {} ".format(len(allCraigslistResults[city]),city)
            print (testString)

            # Threading Post Results?
            for result in allIndeedResults[city]:
                postFromIndeed(sc,result,city)

    jobQueue = Queue()
    slackQueue = Queue()

    for i in range(2):
        t = Thread(target=scrape_area_jobs(area,city,jobcategory,))
        t.start()
    for i in range(2):
        t = Thread(target=postFromCraiglist,args=(sc,result,city,))
        t.start()

    # THIS IS INDEED:
    if useIndeed:
        for city in cities:
            allIndeedResults[city] = []

            for keyword in JobKeywords:
                # Threading?
                allIndeedResults[city] += scrape_area_indeed(keyword,city)


            testString = "Found: {} results for this city: {} ".format(len(allIndeedResults[city]),city)
            print(testString)

            # Threading Post Results?

            for result in allIndeedResults[city]:
                postFromIndeed(sc,result,city)
