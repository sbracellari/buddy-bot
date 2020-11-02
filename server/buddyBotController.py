import json, requests, re
import mysql.connector
from mysql.connector import errorcode
from requests import get
from flask import Flask, jsonify, request
from flask_cors import CORS
from webScraper import webScraperFunc
from model import initModel, computeAnswer
from chatting import initChat, botResponse

try:
    connection = mysql.connector.connect(user='admin', password='dreamteam1234', host='buddybot.c2ao7w5qbjh5.us-east-2.rds.amazonaws.com', database='buddybot')
except mysql.connector.Error as err:
    print(err)

cur = connection.cursor(dictionary=True)

connection.autocommit = True

params = []

app = Flask(__name__)
CORS(app)

@app.route('/buddy-bot/v1/health-check', methods=['GET'])
def health_check():
    return 'true'

@app.route('/buddy-bot/v1/response', methods=['POST'])
def response():
    question = request.json.get('question')
    context, url = webScraperFunc(question)
    answer = computeAnswer(question, f'''{context}''', params[0], params[1])

    if '[SEP]' in answer:
        answer = ''

    cur.callproc('programmingQuestion', [question, answer])

    row_ID = None

    for result in cur.stored_results():
        row_ID = result.fetchone()
    
    response = jsonify(
        { 'response': answer },
        { 'id': row_ID }#,
        #{ 'url': url }
    )

    return response

@app.route('/buddy-bot/v1/chat', methods=['POST'])
def chat():
    user_input = request.json.get('sentence')
    chat = str(botResponse(user_input, chatbot[0], chatbot[1]))
    response = jsonify({ 'response': chat })
    return response

@app.route('/buddy-bot/v1/success', methods=['POST'])
def success():
    success= request.json.get('success')
    row_id = request.json.get('id')

    cur.callproc('feedback', [row_id, success])
    return True

if __name__ == '__main__':
    params = initModel()
    chatbot = initChat()
    app.run()
