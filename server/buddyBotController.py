import json, requests, re
from requests import get
from flask import Flask, jsonify, request
from flask_cors import CORS
from webScraper import webScraperFunc
from model import initModel, computeAnswer

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

if __name__ == '__main__':
    params = initModel()
    app.run()