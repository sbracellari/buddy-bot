import json, requests, re
import mysql.connector
from mysql.connector import errorcode
from requests import get
from flask import Flask, jsonify, request
from flask_cors import CORS
from webScraper import webScraperFunc
from model import initModel, computeAnswer
from chatting import initChat, botResponse

from webScraper import geeksForGeeksFormatCode
from webScraper import w3SchoolsFormatCode

params = initModel()

app = Flask(__name__)
CORS(app)
app_context = app.app_context()

def bot_response(question):
    context, url = webScraperFunc(question)
    answer = computeAnswer(question, f'''{context}''', params[0], params[1])

    response = 'Waddaya talkin\' bout?' if '[SEP]' in answer or answer is '' else answer
    return response

def chat_response(user_input):
    chat = str(botResponse(user_input))
    return chat

@app.route('/buddy-bot/v1/health-check', methods=['GET'])
def health_check():
    return 'true'

@app.route('/buddy-bot/v1/response', methods=['POST'])
def response():
    question = request.json.get('question')

    context, url = webScraperFunc(question)
    answer = computeAnswer(question, f'''{context}''', params[0], params[1])
    
    code = None
    #Get Formatted Code
    try:
        if(url.find('geeksforgeeks') != -1):
            if(geeksForGeeksFormatCode(url) != ''):
                code = geeksForGeeksFormatCode(url)
        elif(url.find('w3schools') != -1):
            if(w3SchoolsFormatCode(url) != ''):
                code = w3SchoolsFormatCode(url)
    except AttributeError:
        print("Error in formatting code", AttributeError)

    bad_answer = '[SEP]' in answer or question.lower() in answer.lower()
    bad_url = url == None or url == ''
    
    if bad_answer == True or bad_url == True:
        answer = ''
        url = None

    try:
        connection = mysql.connector.connect(user='admin', password='dreamteam1234', host='buddybot.c2ao7w5qbjh5.us-east-2.rds.amazonaws.com', database='buddybot')
    except mysql.connector.Error as err:
        print(err)

    cur = connection.cursor(dictionary=True)
    connection.autocommit = True

    cur.callproc('programmingQ', [question, answer, url])
      
    for result in cur.stored_results():
        row_ID = result.fetchone()[0]

    response = jsonify({
       'response': answer,
       'id': row_ID,
       'url': url,
       'code': code
    })

    return response

@app.route('/buddy-bot/v1/chat', methods=['POST'])
def chat():
    user_input = request.json.get('sentence')
    chat = str(botResponse(user_input))
    response = jsonify({ 'response': chat })
    return response
    return user_input

@app.route('/buddy-bot/v1/success', methods=['POST'])
def success():
    success= request.json.get('success')
    row_id = request.json.get('id')

    try:
        connection = mysql.connector.connect(user='admin', password='dreamteam1234', host='buddybot.c2ao7w5qbjh5.us-east-2.rds.amazonaws.com', database='buddybot')
    except mysql.connector.Error as err:
        print(err)

    cur = connection.cursor(dictionary=True)
    connection.autocommit = True

    cur.callproc('feedback', [row_id, success])
    return 'True'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
