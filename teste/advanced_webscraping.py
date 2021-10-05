import requests
from bs4 import BeautifulSoup
# GET
content = requests.get('https://www.imdb.com/find?q=mark&s=nm&exact=true&ref_=fn_al_nm_ex')

doc = BeautifulSoup(content.text, 'html.parser')

# Grab all the titles
name_tags = doc.find_all(class_='result_text')

# Let's print the firs 5
for name in name_tags:
    print(name.a.string)


# POST EXAMPLE
data = {
    'lastName': 'Kelly',
    'firstName': 'John',
    'boardCode': '9',
    'licenseNumber': '',
    'licenseType': '250',
    'registryNumber': '',
    }

url = 'https://search.dca.ca.gov/results'

response = requests.post(url, data=data)
doc = BeautifulSoup(response.text, 'html.parser')

# Grabbing all the name tags
name_tags = doc.find_all('h3')

for name in name_tags:
    print(name.text)

# Module 02 - Cookies and Login
# Session Cookie - It's a piece of text that a website stores with the browser.
# Used to store unique identifier. Can track browsing session, called "session cookies"
# After login browser starts to behave differently for you.

# CSRF Tokens
# Cross Site Request Forgeries - Security vulnerabilities in web applications
# Since they are common, most websites employ tools to block them
# Random string in every form once form is submitted, it is sent back to the website to be verified
# Random string is called: CSRF




