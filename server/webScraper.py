#Call the webScraperFunc() function and pass the user's question as a parameter
#Will return the context from GeeksforGeeks for the user's question
import requests
from bs4 import BeautifulSoup
from flask import jsonify
import tldextract

def stackOverflow(URL):
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, 'html.parser')
  results = soup.find(id='answers')
  title_elem = results.find('div', class_='s-prose js-post-body')

  possible_links = title_elem.find_all('p')
  for link in possible_links:
    return link.get_text()

def getArticleTag(URL):
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, 'html.parser')
  results = soup.find('article')
  return results.get_text()

def docsPython(URL):
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, 'html.parser')
  results = soup.find("div", class_ = "section")
  return results.get_text()

def w3Schools(URL):
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, 'html.parser')
  results = soup.find(id='main')
  return results.get_text()
  

def webScraperFunc(question):
  try: 
      from googlesearch import search 
  except ImportError:  
      print("No module named 'google' found")

  # to search
  query = question + " site:geeksforgeeks.org" #OR site:stackoverflow.com OR site:docs.oracle.com OR site:towardsdatascience.com OR site:w3schools.com" 

  # map the inputs to the function blocks
  options = {'www.geeksforgeeks.org' : getArticleTag,
            'stackoverflow.com' : stackOverflow,
             'docs.oracle.com' : getArticleTag,
             'docs.python.org' : docsPython,
             'towardsdatascience.com' : getArticleTag,
             'www.w3schools.com' : w3Schools,
  }
  for j in search(query, tld="co.in", num=1, stop=1, pause=2):
    #https://stackoverflow.com/questions/44021846/extract-domain-name-from-url-python
    ext =  tldextract.extract(j)
    if ext.subdomain != '':
      return options[ext.subdomain + '.' + ext.domain + '.' + ext.suffix](j)
    
    return options[ext.domain + '.' + ext.suffix](j)
