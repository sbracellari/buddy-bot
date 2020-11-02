import json, requests, re
from requests import get
from flask import Flask, jsonify, request
from flask_cors import CORS
from webScraper import webScraperFunc
from model import initModel, computeAnswer
from chatting import initChat, botResponse

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
    response = jsonify(
        { 'response': answer }#,
        #{ 'url': url }
    )

    return response

@app.route('/buddy-bot/v1/chat', methods=['POST'])
def chat():
    user_input = request.json.get('sentence')
    chat = str(botResponse(user_input, chatbot[0], chatbot[1]))
    response = jsonify({ 'response': chat })
    return response

if __name__ == '__main__':
    params = initModel()
    chatbot = initChat()
    app.run()