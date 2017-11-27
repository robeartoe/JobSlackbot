#In here all settings, all variables can be configured here.
from indeed.indeed import IndeedApi
from config.private import token

slackLA = "#losangeles"
slackNY = "#newyork"

#Indeed Api:-----------------------------------------------------------------------------------------------------
useIndeed = True
JobKeywords = ["Python Internship","Web Developer Internship","python intern","web developer intern","Computer Science Internship"]
cities = ['Los Angeles']
# Cities: cities = ['Los Angeles', 'New York']

#Craigslist Api:-------------------------------------------------------------------------------------------------
useCraigslist = True
jobCategorys = ['sof', 'jjj']
want_internship = True
resultNumber = 1 #Be careful with this, don't bring back too many results.
Craigslistcities = ['losangeles']
# Craigslistcities = ['losangeles','newyork']

areas = {'losangeles': ['lac']}
# areas = {'losangeles': ['lac'] , 'newyork': ['mnh','brk','que','brx']}

SLEEP_INTERVAL = 180 * 60 #Three hour Interval
#60 minutes. Change the first number to adjust minutes.
