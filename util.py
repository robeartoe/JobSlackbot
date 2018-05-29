"""
This function is to post results to slack.
"""
from models import craigslistModel,indeedModel,Listing
import settings

def postFromIndeed(listing,inRow):
    try:
        description = "{}|{}|{}|{}|<{}>".format(inRow.location, inRow.title, inRow.url,
                                        inRow.name, inRow.created)
        sc.api_call(
        "chat.postMessage", channel=inRow.slackChannel, text=description,
        username='pybot', icon_emoji=':briefcase:'
        )
    except Exception as inst:
        print(inst)
        print("ERROR Posting to Slack.")

def postFromCraiglist(listing,clRow):
    try:
        description = "{}|{}|{}|<{}>".format(listing.location, listing.title, listing.url, listing.created)
        sc.api_call(
        "chat.postMessage", channel=clRow.slackChannel, text=description,
        username='pybot', icon_emoji=':palm_tree:'
        )
    except Exception as inst:
        print(inst)
        print("ERROR Posting to Slack.")
