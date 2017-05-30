#In here all settings, all variables can be configured here.
from indeed.indeed import IndeedApi
from config.private import token

slackLA = "#losangeles"
slackNY = "#newyork"

#Indeed Api:
useIndeed = False
api = IndeedApi(token)
JobKeywords = ["Python Internship","Web Developer Internship","Django Internship"]
cities = ['Los Angeles', 'New York']

#Craigslist Api:
useCraigslist = True
jobCategorys = ['sof', 'jjj']
want_internship = True
Craigslistcities = ['losangeles','newyork']
areas = {'losangeles': ['lac'] , 'newyork': ['mnh','brk','que','brx']}

SLEEP_INTERVAL = 60 * 60 #60 minutes. Change the first number to adjust minutes. Or second... I'm not the boss of you.
