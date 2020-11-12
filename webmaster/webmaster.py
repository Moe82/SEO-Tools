import data_utils as utils
from googlesearch import search
from random import randint
import time
import hmac
import base64
from json import loads, dumps
import hashlib
import urllib

MAX_DA = 70

class ContactInformation:
	def __init__(self, firstName, lastName, email, organization, domain, confidanceScore, domainAuthority, type="Personal"):
		self.firstName = firstName
		self.lastName = lastName
		self.email = email
		self.organization = organization
		self.domain = domain 
		self.domainAuthority = domainAuthority
		self.confidanceScore = confidanceScore;
		self.type = type;
	
	def getContactDict(self):
		return {"Cofidance score": self.confidanceScore,"First Name": self.firstName,"Last Name": self.lastName,"email": self.email, "email type": self.type,"organization": self.organization,"domain": self.domain, "Domain Authority": self.domainAuthority}


def getContactInformation(domain, HUNTER_API_KEY, domainAuthority):
	print("Calling Hunter API to get contact information..")
	uClient = urllib.request.urlopen("https://api.hunter.io/v2/domain-search?domain="+domain+"&api_key=" + HUNTER_API_KEY)
	json = loads(uClient.read())	
	uClient.close()
	for email in json.get('data').get('emails'):
		contact = ContactInformation(email.get('first_name'), email.get('last_name'),email.get('value'), json.get('data').get('organization'), json.get('data').get('domain'), email.get('confidence'), domainAuthority, email.get('type'))
		if email.get('type') == 'personal':
			if email.get('last_name') != None:
				utils.appendDictToFile("personal_contact.csv", contact.getContactDict())
				print(email.get('first_name') + " " + email.get('last_name') + " added to personal_contact.csv")
			else:
				utils.appendDictToFile("personal_contact_extra.csv", contact.getContactDict())
				print("Contact added to personal_contact_extra.csv")
		elif email.get('type') != 'personal':
			utils.appendDictToFile("nonpersonal_contact.csv", contact.getContactDict())
			print("Contact added to nonpersonal_contact.csv")

def getDomainAuthority(domain, accessID, secretKey):	
	try:
		print("Calling Moz API to get DA score..")
		time.sleep(randint(5,10))
		expires = int(time.time() + 100)
		stringToSign = accessID+"\n"+str(expires)
		binarySignature = base64.b64encode(hmac.new(secretKey.encode(), stringToSign.encode(), hashlib.sha1).digest())
		urlSafeSignature = urllib.parse.quote_plus(binarySignature.decode('utf-8'))
		cols = "68719476736"
		requestUrl = "http://lsapi.seomoz.com/linkscape/url-metrics/?Cols="+cols+"&AccessID="+accessID+"&Expires="+str(expires)+"&Signature="+urlSafeSignature
		batchedDomains =[domain]
		jsonencoded = dumps(batchedDomains)
		binary_data = jsonencoded.encode('utf-8') 
		req = urllib.request.Request(url=requestUrl, data=binary_data)
		f = urllib.request.urlopen(req)
		domainAuthority_string = ((f.read().decode('utf-8')))
		if len(domainAuthority_string) == 12:
			domainAuthority = domainAuthority_string[8:10]
		elif len(domainAuthority_string) == 13:
			domainAuthority = domainAuthority_string[8:11]
		elif len(domainAuthority_string) == 11:
			domainAuthority = domainAuthority_string[8]
		return (domainAuthority)
	except:
		print("Issue accessing Moz API")
		return -1

def urlToDomain(url):
		if (url[8:11] == 'www'):
			domain = url.replace('https://www.', '').split('/', 1)[0]
		else:
			domain = url.replace('https://', '').split('/', 1)[0]
		return domain

def urlsToDomains(urls):
	domains = []
	for url in urls:
		domains.append(urlToDomain(url))
	return domains

def google(keyword):	  
	print("\nGetting Google search results for keyword: " + keyword)
	return list(search(keyword, tld='com', num=100, stop=100, pause=2))

if __name__ == "__main__":
	try:
		credentials = utils.parseFile("credentials.csv")
		MOZ_ACCESS_ID, MOZ_SECRET_KEY, HUNTER_API_KEY = credentials['MOZ_ACCESS_ID'], credentials['MOZ_SECRET_KEY'], credentials['HUNTER_API_KEY']
	except:
		MOZ_ACCESS_ID = input("Please enter your Moz API Access ID: ")
		MOZ_SECRET_KEY = input("Please enter your Moz API secret key: ")
		HUNTER_API_KEY = input("Please enter your Hunter API key: ")
	
	keywords = utils.parseFile("keywords.txt")
	for keyword in keywords:
		domains = urlsToDomains(google(keyword))
		for domain in domains:
			if utils.searchFile("history.txt", domain) == False:
				print("\nDomain: " + domain)
				domainAuthority = int(getDomainAuthority(domain, MOZ_ACCESS_ID, MOZ_SECRET_KEY))
				print("domainAuthority: " + str(domainAuthority))
				if domainAuthority < MAX_DA:
					getContactInformation(domain,HUNTER_API_KEY, domainAuthority)
				else:
					print("Domain authority score is too high. Skipping.")
				utils.appendStringToFile("history.txt", domain)
				print("________________________________")
		time.sleep(randint(5,10))