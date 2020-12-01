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

def geeksForGeeksFormatCode(URL):
  try:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    title_elem = soup.find('div', class_='container')
    code = title_elem.find_all('div')
    text = ''
    for i in range(len(code)):
      formatted_code = code[i].get_text().encode('ascii', 'ignore').decode('ascii')
      if(i == 0):
        text = formatted_code
      else:
        try:
          indent = code[i].find('code', class_='undefined spaces')
          text += '\n' + indent.text + formatted_code
        except AttributeError:
          text += '\n' + formatted_code 
  except AttributeError:
    text = ''
  return text

def w3SchoolsFormatCode(URL):
  try:
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    title_elem = soup.find('div', class_='w3-example')
    elem = title_elem.find_all('div')
    if(elem == []):
      elem = title_elem.find_all('pre')
    text = str(elem[0]).replace('<br/>', '<br/>\n')
    soup = BeautifulSoup(text, 'html.parser')
    text = soup.text
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
    try:
      page = requests.get(URL)
      soup = BeautifulSoup(page.content, 'html.parser')
      results = soup.find_all('p')
      text = ''
      for i in results:
        text += i.text
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
  query = question + " site:docs.oracle.com OR site:w3schools.com OR site:geeksforgeeks.org OR site:docs.python.org OR site:stackoverflow.com" 

  # map the inputs to the function blocks
  options = {'www.geeksforgeeks.org' : getArticleTag,
            'stackoverflow.com' : stackOverflow,
             'docs.oracle.com' : oracle,
             'docs.python.org' : docsPython,
             #'towardsdatascience.com' : getArticleTag,
             'www.w3schools.com' : w3Schools,
  }
  context = ''
  url = ''
  try:
    for j in search(query, tld="co.in", num=1, stop=1, pause=2):
        #https://stackoverflow.com/questions/44021846/extract-domain-name-from-url-python
        ext =  tldextract.extract(j)
        url = j
        if ext.subdomain != '':
            context = options[ext.subdomain + '.' + ext.domain + '.' + ext.suffix](j)
        else:
            context = options[ext.domain + '.' + ext.suffix](j)
  except: 
    context = ''
    url = None

  return context, url

#Not currently in use. Potential future implementation
#Scrapes top 5 memes (past 24 hours) from ProgrammingHumor and randomly displays one of them
#Pictures of the 5 memes are stored in local directory
def reddit():
  #!pip install praw
  import praw,requests,re

  r = praw.Reddit(client_id="tIjKIK3zNnJnvQ",
                client_secret="8ke_e-1QjmJeD6ruV5iRSUKqC_M",
                password="csi4999",
                user_agent="Buddy Bot",
                username="BuddyBot4999")
  subreddit = r.subreddit('ProgrammerHumor')

  import urllib.request
  count = 0

  # Iterate through top submissions
  for submission in subreddit.hot(limit=None):

    # Get the link of the submission
    url = str(submission.url)

    # Check if the link is an image
    if url.endswith("jpg") or url.endswith("jpeg") or url.endswith("png"):

        urllib.request.urlretrieve(url, f"image{count}")
        count += 1

        # Stop once you have 10 images
        if count == 5:
            break

  from random import randint
  x = randint(0, 4)
  images = ['image0', 'image1', 'image2', 'image3', 'image4']

  import matplotlib.pyplot as plt
  img = plt.imread(images[x])
  imgplot = plt.imshow(img)
  plt.axis('off')
  plt.show()
