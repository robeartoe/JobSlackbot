"""
This function is to post results to slack.
"""
from models import craigslistModel,indeedModel,Listing
import settings

def postFromIndeed(sc,listings,inRow):
    for listing in listings:
        try:
            description = "{}|{}|{}|{}|<{}>".format(listing.location, listing.title, listing.url,
                                            listing.name, listing.created)
            sc.api_call(
            "chat.postMessage", channel=inRow.slackChannel, text=description,
            username='pybot', icon_emoji=inRow.icon
            )
        except Exception as inst:
            print(inst)
            print("ERROR Posting to Slack.")

def postFromCraiglist(sc,listings,clRow):
    for listing in listings:
        try:
            description = "{}|{}|{}|<{}>".format(listing.location, listing.title, listing.url, listing.created)
            sc.api_call(
            "chat.postMessage", channel=clRow.slackChannel, text=description,
            username='pybot', icon_emoji=clRow.icon
            )
        except Exception as inst:
            print(inst)
            print("ERROR Posting to Slack.")
