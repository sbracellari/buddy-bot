#Call the webScraper() function and pass the user's question as a parameter
#Will return the context from GeeksforGeeks for the user's question
import requests
from bs4 import BeautifulSoup
import tldextract

def stackOverflow(URL):
  try:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='answers')
    title_elem = results.find('div', class_='s-prose js-post-body')
    possible_links = title_elem.find_all('p')
    for link in possible_links:
      text = link.get_text().encode('ascii', 'ignore').decode('ascii')
  except AttributeError:
    text = ''
  return text

def getArticleTag(URL):
  try:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('article')
    text = results.get_text().encode('ascii', 'ignore').decode('ascii')
  except AttributeError:
    text = ''
  return text

def docsPython(URL):
  try:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find("div", class_ = "section")
    text = results.get_text().encode('ascii', 'ignore').decode('ascii')
  except AttributeError:
    text = ''
  return text

def w3Schools(URL):
  try:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='main')
    text = results.get_text().encode('ascii', 'ignore').decode('ascii')
  except AttributeError:
    text = ''
  return text

def oracle(URL):
  try:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find('body')
    text = results.get_text().encode('ascii', 'ignore').decode('ascii')
  except AttributeError:
    text = ''
  return text

def webScraperFunc(question):
  try: 
      from googlesearch import search 
  except ImportError:  
      print("No module named 'google' found")

  # to search
  query = question + " site:docs.oracle.com OR site:geeksforgeeks.org OR site:w3schools.com OR site:geeksforgeeks.org OR site:towardsdatascience.com OR site:docs.python.org" 

  # map the inputs to the function blocks
  options = {'www.geeksforgeeks.org' : getArticleTag,
            'stackoverflow.com' : stackOverflow,
             'docs.oracle.com' : oracle,
             'docs.python.org' : docsPython,
             'towardsdatascience.com' : getArticleTag,
             'www.w3schools.com' : w3Schools,
  }
  context = ''
  url = ''
  for j in search(query, tld="co.in", num=1, stop=1, pause=2):
    #https://stackoverflow.com/questions/44021846/extract-domain-name-from-url-python
    ext =  tldextract.extract(j)
    url = j
    if ext.subdomain != '':
      context = options[ext.subdomain + '.' + ext.domain + '.' + ext.suffix](j)
    else:
      context = options[ext.domain + '.' + ext.suffix](j)

  return context, url