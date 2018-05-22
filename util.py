"""
This function is to post results to slack.
"""
import settings

# TODO: Convert so it'll read from DB.

def postFromIndeed(sc, city, listing):
    # Simply copy and paste these statements to add more cities, or remove cities. Then change city accordingly.
    if city == "Los Angeles" or city == 'losangeles':
        try:
            description = "{}|{}|{}|{}|<{}>".format(listing["formattedLocationFull"], listing["jobtitle"], listing["url"],
                                                listing["company"], listing["date"])
            sc.api_call(
            "chat.postMessage", channel=settings.slackLA, text=description,
            username='pybot', icon_emoji=':palm_tree:'
            )
        except Exception as inst:
            print(inst)
            print("ERROR Posting to Slack.")

    else:
        description = "{}|{}|{}|{}|<{}>".format(listing["formattedLocationFull"], listing["jobtitle"], listing["url"],
                                                listing["company"], listing["date"])
        sc.api_call(
            "chat.postMessage", channel=settings.slackNY, text=description,
            username='pybot', icon_emoji=':statue_of_liberty:'
        )


def postFromCraiglist(sc, city, listing):
    # Simply copy and paste these statements to add more cities, or remove cities. Then change city accordingly.
    # print("postFromCraiglist was called: sc:{},city:{},listing:{}".format(sc,city,listing))
    if city == "Los Angeles" or city == 'losangeles':
        try:
            description = "{}|{}|{}|<{}>".format(listing["where"], listing["name"], listing['url'], listing["datetime"])
            sc.api_call(
            "chat.postMessage", channel=settings.slackLA, text=description,
            username='pybot', icon_emoji=':palm_tree:'
            )
        except Exception as inst:
            print(inst)
            print("ERROR Posting to Slack.")
    else:
        description = "{}|{}|{}|<{}>".format(listing["where"], listing["name"], listing['url'], listing["datetime"])
        sc.api_call(
            "chat.postMessage", channel=settings.slackNY, text=description,
            username='pybot', icon_emoji=':statue_of_liberty:'
        )
