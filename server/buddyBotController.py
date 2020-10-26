import json, requests, re
from requests import get
from flask import Flask, jsonify, request
from flask_cors import CORS
from webScraper import webScraperFunc

app = Flask(__name__)
CORS(app)

@app.route('/buddy-bot/v1/health-check', methods=['GET'])
def health_check():
    return 'true'

@app.route('/buddy-bot/v1/response', methods=['POST'])
def response():
    question = request.json.get('question')
    response = webScraperFunc(question)
    # response = mock_response(question)
    return response

def mock_response(question):
    response = jsonify({'response': 'she my lil boo thang'})
    return response

if __name__ == '__main__':
    app.run()