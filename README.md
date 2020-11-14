# SEO-Tools
A collection of SEO automation tools that I wrote in Python. 

## Webmaster
The second script in my Python SEO automation pipeline. Transforms a list of niche related keywords into list of email addresses (along with the first name, last name, and domain authority) of webmasters within a niche.

The script is fairly simple and merely ties 3 different API's together, but the output is quite significant. With enough keywords (and time), it can generate thousands of high quality email addresses for webmasters within a specific niche. Collecting this information manually would be nearly impossible.

The output (a .csv file) can be fed directly into your favorite email marketing software and the keywords can simply be those that your site ranks for. 

### Requirements
- Python 3
- [Google Library](https://pypi.org/project/google/) (Note: package has no association with Google, LLC)
- Free [Moz](https://moz.com/products/api/keys) API Key
- Free [Hunter.io](https://hunter.io/api) API

### Instructions
1) Clone this repository and install the Google library. 
 ```console
 git clone https://github.com/Moe82/SEO-Tools.git
 pip install google
 ```
2) Open up keywords.txt (located inside the data directory) and populate it with keywords related to your niche. Each keyword should go on a separate line. Tip: you can download a very large file of keywords that you rank for on [search.google.com](https://search.google.com/search-console/about)
3) Run the script.

 ```console 
 python3 webmaster.py
 ```
4) When prompted, enter your Moz API access ID and key and your Hunter.io API Key. Alternatively, you can have the script load your credentials automatically. To do so, paste the text below into a .csv file, save it as credentials.csv, and place it inside the data directory. If a file called credentials.csv is already present inside the data directory, delete the old one and insert the new one that you created. 
```console
MOZ_ACCESS_ID,<your Moz access ID>
MOZ_SECRET_KEY,<your Moz secret key>
HUNTER_API_KEY,<your Moz access ID>
```
As the script runs, the 3 CSV below will be updated as information is collected. Each row in a table represents a contact and each contact includes a first name, last name, email address and its confidence score (as determined by the Hunter.io API), organization, domain, and domain authority. Note that if information for any of these fields is not found, the corresponding cell will be empty.

* personal_contact.csv - Email address that are flagged as "personal" and have an associated first name and last name. This is what you want to use for your outreach. 
* personal_contact_extra.csv - Email address that are flagged as "personal" but don't have an accociated first name and last name. You can use this list as well, but I find that starting an email with "Dear first_name last_name," greatly increases response rate. 
* nonpersonal_contact.csv - All other email addresses (that are not flagged as personal). 
* history.txt - Contains the domain address for sites that have already been scrapped. This file essentially allows you to terminate the script at any point and resume where you left off when you run it again. 

By default, sites with a domain authority score greater than 70 are ignored as such sites generally aren't good targets for backlink accusation. This value can be changed in line 11 of webmaster.py.

### Common HTTP response errors

* HTTP Error 429 - Too many calls to API. Either upgrade free trial account or make a new one.
* HTTP error 401 - Incorrect api credentials. Check that you have entered them in correctly and try again.