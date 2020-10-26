#Call the webScraperFunc() function and pass the user's question as a parameter
#Will return the context from GeeksforGeeks for the user's question
import requests
from bs4 import BeautifulSoup
from flask import jsonify

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
  results = soup.find(id='module-array')
  return results.get_text()

def w3Schools(URL):
  page = requests.get(URL)
  soup = BeautifulSoup(page.content, 'html.parser')
  results = soup.find(id='main')
  return results.get_text()
  

def webScraperFunc(question):
  response = jsonify({'response': 'use margin : auto'})
  return response
  # try: 
  #     from googlesearch import search 
  # except ImportError:  
  #     print("No module named 'google' found") 
  # site = "geeksforgeeks.org"

  # # to search
  # query = question + " site:" + site 

  # # map the inputs to the function blocks
  # options = {'geeksforgeeks.org' : getArticleTag,
  #           'stackoverflow.com' : stackOverflow,
  #            'docs.oracle.com' : getArticleTag,
  #            'docs.python.org' : docsPython,
  #            'towardsdatascience.com' : getArticleTag,
  #            'w3schools.com' : w3Schools,
  # }
  
  # for j in search(query, tld="co.in", num=1, stop=1, pause=2): 
  #     return options[site](j)
