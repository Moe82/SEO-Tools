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
    def __init__(self, first_name, last_name, email, organization, domain, confidance_score, domain_authority, type="personal"):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.organization = organization
        self.domain = domain 
        self.domain_authority = domain_authority
        self.confidance_score = confidance_score
        self.type = type
    
    def get_contact_dict(self):
        return {"Cofidance score": self.confidance_score, "First Name": self.first_name, "Last Name": self.last_name,"email": self.email, "email type": self.type,"organization": self.organization,"domain": self.domain, "Domain Authority": self.domain_authority}


def get_contact_information(domain, HUNTER_API_KEY, domain_authority):
    try:
        print("Calling Hunter API to get contact information...")
        uClient = urllib.request.urlopen("https://api.hunter.io/v2/domain-search?domain="+domain+"&api_key=" + HUNTER_API_KEY)
        json = loads(uClient.read())    
        uClient.close()
        for email in json.get('data').get('emails'):
            contact = ContactInformation(email.get('first_name'), email.get('last_name'), email.get('value'), json.get('data').get('organization'), json.get('data').get('domain'), email.get('confidence'), domain_authority, email.get('type'))
            if email.get('type') == 'personal':
                if email.get('last_name') != None:
                    utils.append_dict_to_csv_file("personal_contact.csv", contact.get_contact_dict())
                    print(email.get('first_name') + " " + email.get('last_name') + " added to personal_contact.csv")
                else:
                    utils.append_dict_to_csv_file("personal_contact_extra.csv", contact.get_contact_dict())
                    print("Contact added to personal_contact_extra.csv")
            elif email.get('type') != 'personal':
                utils.append_dict_to_csv_file("nonpersonal_contact.csv", contact.get_contact_dict())
                print("Contact added to nonpersonal_contact.csv")
    except Exception as e:
        print("Issue accessing Hunter API (" + str(e) + ")\nTerminating webmaster.py")
        exit()

def get_domain_authority(domain, MOZ_ACCESS_ID, MOZ_SECRET_KEY):    
    try:
        print("Calling Moz API to get DA score...")
        time.sleep(10)
        expires = int(time.time() + 100)
        string_to_sign = MOZ_ACCESS_ID + "\n" + str(expires)
        binary_signature = base64.b64encode(hmac.new(MOZ_SECRET_KEY.encode(), string_to_sign.encode(), hashlib.sha1).digest())
        url_safe_signature = urllib.parse.quote_plus(binary_signature.decode('utf-8'))
        cols = "68719476736"
        request_url = "http://lsapi.seomoz.com/linkscape/url-metrics/?Cols="+cols+"&AccessID="+MOZ_ACCESS_ID+"&Expires="+str(expires)+"&Signature="+url_safe_signature
        batched_domains = [domain]
        json_encoded = dumps(batched_domains)
        binary_data = json_encoded.encode('utf-8') 
        req = urllib.request.Request(url=request_url, data=binary_data)
        f = urllib.request.urlopen(req)
        domain_authority_string = ((f.read().decode('utf-8')))
        if len(domain_authority_string) == 12:
            domain_authority = domain_authority_string[8:10]
        elif len(domain_authority_string) == 13:
            domain_authority = domain_authority_string[8:11]
        elif len(domain_authority_string) == 11:
            domain_authority = domain_authority_string[8]
        return (domain_authority)
    except Exception as e:
        print("Issue accessing Moz API (" + str(e) + ")")
        return -1

def url_to_domain(url):
        if (url[8:11] == 'www'):
            domain = url.replace('https://www.', '').split('/', 1)[0]
        else:
            domain = url.replace('https://', '').split('/', 1)[0]
        return domain

def urls_to_domains(urls):
    domains = []
    for url in urls:
        domains.append(url_to_domain(url))
    return domains

def google(keyword):      
    print("\nGetting Google search results for keyword: " + keyword)
    return list(search(keyword, tld='com', num=100, stop=100, pause=2))

if __name__ == "__main__":
    try:
        credentials = utils.parse_file("credentials.csv")
        MOZ_ACCESS_ID, MOZ_SECRET_KEY, HUNTER_API_KEY = credentials['MOZ_ACCESS_ID'], credentials['MOZ_SECRET_KEY'], credentials['HUNTER_API_KEY']
    except:
        MOZ_ACCESS_ID = input("\nPlease enter your Moz API Access ID: ")
        MOZ_SECRET_KEY = input("Please enter your Moz API secret key: ")
        HUNTER_API_KEY = input("Please enter your Hunter API key: ")
    keywords = utils.parse_file("keywords.txt")
    for keyword in keywords:
        domains = urls_to_domains(google(keyword))
        for domain in domains:
            if utils.search_file("history.txt", domain) == False:
                print("\nDomain: " + domain)
                domain_authority = int(get_domain_authority(domain, MOZ_ACCESS_ID, MOZ_SECRET_KEY))
                print("DA score: " + str(domain_authority))
                if domain_authority < MAX_DA:
                    get_contact_information(domain,HUNTER_API_KEY, domain_authority)
                else:
                    print("Domain authority score is too high. Skipping.")
                utils.append_string_to_textfile("history.txt", domain)
                print("________________________________")
        time.sleep(randint(5,10))
