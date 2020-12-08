import json, requests, re
import mysql.connector
from mysql.connector import errorcode
from requests import get
from flask import Flask, jsonify, request
from flask_cors import CORS

#Imports functions from other server files
from webScraper import webScraperFunc
from model import initModel, computeAnswer
from chatting import initChat, botResponse
from webScraper import geeksForGeeksFormatCode
from webScraper import w3SchoolsFormatCode

#Initiates the BERT model upon run of file
params = initModel()

app = Flask(__name__)
CORS(app)
app_context = app.app_context()

#The functions below are called by the Discord Bot in bot.py
#bot_response takes a question as input, runs it through the scraper
#to get context, and runs the context and question through BERT to recieve an answer.
def bot_response(question):
    context, url = webScraperFunc(question)
    answer = computeAnswer(question, f'''{context}''', params[0], params[1])

    bad_answer = '[SEP]' in answer or question.lower() in answer.lower() or answer is ''

    #If there is no answer recieved from BERT, it responds with 'Waddaya talkin' about?'
    response = 'Waddaya talkin\' bout?' if bad_answer else answer
    return response

#chat_response takes a user input and runs it through chatterbot, which then returns a 
#response from chatterbot. 
def chat_response(user_input):
    chat = str(botResponse(user_input))
    return chat


@app.route('/buddy-bot/v1/health-check', methods=['GET'])
def health_check():
    return 'true'

#This approute is called when the website sends a programming question from a user. 
@app.route('/buddy-bot/v1/response', methods=['POST'])
#The response function recieves a programming question as input from the user,
#runs it through the web scraper and BERT to get and answer, and also checks for
#possible code snippets, and returns them to the website as a JSON object. 
def response():
    #Recieves the question request from the site
    question = request.json.get('question')

    #Runs the question through the webscraper and recieves context ana a url.
    context, url = webScraperFunc(question)

    #Runs the question and context through BERT to recieve an answer.
    answer = computeAnswer(question, f'''{context}''', params[0], params[1])
    
    #Get Formatted Code (only works for responses from geeksforgeeks and w3schools)
    code = None
    try:
        if(url.find('geeksforgeeks') != -1):
            if(geeksForGeeksFormatCode(url) != ''):
                code = geeksForGeeksFormatCode(url)
        elif(url.find('w3schools') != -1):
            if(w3SchoolsFormatCode(url) != ''):
                code = w3SchoolsFormatCode(url)
    except AttributeError:
        print("Error in formatting code", AttributeError)

    #Checks to make sure there is an answer and a URL to be returned
    #If not, then the URL or answer will be deemed "bad"
    #If either is bad, the answer = '' and url = None
    bad_answer = '[SEP]' in answer or question.lower() in answer.lower()
    bad_url = url == None or url == ''
    
    if bad_answer == True or bad_url == True:
        answer = ''
        url = None

    #This initializes the connection to the database and is called every time a user 
    #asks a question to prevent any timeout 
    try:
        connection = mysql.connector.connect(user='admin', password='dreamteam1234', host='buddybot.c2ao7w5qbjh5.us-east-2.rds.amazonaws.com', database='buddybot')
    except mysql.connector.Error as err:
        print(err)

    cur = connection.cursor(dictionary=True)
    connection.autocommit = True

    #Inserts the question, answer, and url into the database for future training.
    cur.callproc('programmingQ', [question, answer, url])
      
    #Gets the most recent row id in case the user wants to provide feedback.   
    for result in cur.stored_results():
        row_ID = result.fetchone()[0]

    #Sends the response, id, url, and code back to the site to be used accordingly. 
    response = jsonify({
       'response': answer,
       'id': row_ID,
       'url': url,
       'code': code
    })

    return response

#This approute is called when the website sends a chat from a user. 
@app.route('/buddy-bot/v1/chat', methods=['POST'])
#This function recieves a chat from the website that was input by a user, runs it through
#chatterbot and sends the user a response. 
def chat():
    #recieves the chat from the site
    user_input = request.json.get('sentence')

    #casts the response from chatterbot to a String to send it back to the user
    chat = str(botResponse(user_input))
    response = jsonify({ 'response': chat })

    return response

#This approute is called when the website sends feedback from a user for a programming question. 
@app.route('/buddy-bot/v1/success', methods=['POST'])
#This function recievies a row id and a success variable from the site due to feedback from the user. 
def success():
    #Success is a boolean veriable, 0 for not helpful, 1 for helpful. 
    success= request.json.get('success')
    #Row id tells us what row in the database to add the feedback
    row_id = request.json.get('id')

    #This initializes the connection to the database and is called every time a user 
    #provides feedback to prevent any timeout 
    try:
        connection = mysql.connector.connect(user='admin', password='dreamteam1234', host='buddybot.c2ao7w5qbjh5.us-east-2.rds.amazonaws.com', database='buddybot')
    except mysql.connector.Error as err:
        print(err)

    cur = connection.cursor(dictionary=True)
    connection.autocommit = True

    #Alters the row of the question answer pair to reflect the user's feedback
    cur.callproc('feedback', [row_id, success])

    return 'True'

#If not run through a web server like NGINX, this runs on the host's private ip through port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0')
