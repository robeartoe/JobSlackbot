# SlackbotCraigslist
## A bot that sends job listings from Indeed and Craigslist, to a database, and to your slack.
### Let's get a job!

**This only works on python3**

---

**Instructions:**
* Best to use a virtual env
  * pip install -r requirments.txt
* Get a slack Token
  * Instructions can be found [here](https://get.slack.help/hc/en-us/articles/215770388-Create-and-regenerate-API-tokens).
* Get a Indeed Developer Token
  * Can be found [here](https://www.indeed.com/publisher). Create a developer account and in the "Job Search API" tab, scroll down to find "Get Job API"
* Add onto config/private
  * Rename configExample to config
  * Put your slack & Indeed tokens here.
* Check settings.py
  * Check useIndeed and useCraiglist if you want to use services.
  * Change JobKeywords to whatever you are looking for.(For Indeed)
  * For Craigslist it's a bit different:
    * You have to check craigslist and find what categorys you think your future job will be.
      * For example: Customer Service in LA is: https://losangeles.craigslist.org/search/csr ; You put this in jobCategorys.
    * For what cities you want to choose from, you choose the city exactly from the website. For example: 'losangeles'
    * Finally for within that city, are different neighborhoods, for example 'newyork' has 'mnh','brk','que', and 'brx' for Manhattan, Brooklyn, Queens and Bronx.
* Check util.py
  * This one I appologize for, but for each city, for each function, you have to copy and paste, and change the if/elif/else statement.
  * Also check if you have the correct channel that you want to post to slack.
 * And that's it! Good luck finding a job or internship.
