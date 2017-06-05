"""
The point of this file is to find the distance between two coordinates.
Now I'll do the function three times.
One to find the distance between a point of interst and a house.
Next is to find the distance between a point of interest and a job.
The final is to find the distance between a house and a job.

Of course this will have to be different taking into account WantJob
and WantHousing is True or False.

The next function is to post results to slack.
"""
from math import radians, cos, sin , asin, sqrt
import settings

def postFromIndeed(sc,result,city):
    # Simply copy and paste these statements to add more cities, or remove cities. Then change city accordingly.
    if city == "Los Angeles" or city == 'losangeles':
        description = "{}|{}|{}|{}|<{}>".format(result["formattedLocationFull"],result["jobtitle"],result["url"], result["company"], result["date"])
        sc.api_call(
            "chat.postMessage", channel = settings.slackLA, text = description,
            username = 'pybot' , icon_emoji = ':palm_tree:'
        )
    else:
        description = "{}|{}|{}|{}|<{}>".format(result["formattedLocationFull"],result["jobtitle"],result["url"], result["company"], result["date"])
        sc.api_call(
            "chat.postMessage", channel = settings.slackNY, text = description,
            username = 'pybot' , icon_emoji = ':statue_of_liberty:'
        )
def postFromCraiglist(sc,listing,city):
    # Simply copy and paste these statements to add more cities, or remove cities. Then change city accordingly.
    if city == "Los Angeles" or city == 'losangeles':
        description = "{}|{}|{}|<{}>".format(listing["where"],listing["name"],listing['url'],listing["datetime"])
        sc.api_call(
            "chat.postMessage", channel = settings.slackLA, text = description,
            username = 'pybot' , icon_emoji = ':palm_tree:'
        )
    else:
        description = "{}|{}|{}|<{}>".format(listing["where"],listing["name"],listing['url'],listing["datetime"])
        sc.api_call(
            "chat.postMessage", channel = settings.slackNY, text = description,
            username = 'pybot' , icon_emoji = ':statue_of_liberty:'
        )
