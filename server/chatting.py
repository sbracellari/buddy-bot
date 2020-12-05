from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import random

# This function initializes the conversational aspect
# of the chatbot using the chatterbot python package.
def initChat():
    bot = ChatBot(
    'BuddyBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='mysql+mysqldb://admin:dreamteam1234@buddybot.c2ao7w5qbjh5.us-east-2.rds.amazonaws.com:3306/chat_training',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': ['Make it make sense (ノಠ益ಠ)ノ彡┻━┻', 'Oof I don\'t quite understand', 'Sorry, I can\'t read'],
            'maximum_similarity_threshold': 0.90
        }
    ])

    return bot

# This function is used to select a default response 
# if the confidence level of the bot response is below the set amount.
def selectDefault():
    defaultList = ['Make it make sense (ノಠ益ಠ)ノ彡┻━┻', 'Oof I don\'t quite understand', 'Sorry, I can\'t read']
    ind = random.randint(0, len(defaultList) - 1)
    return defaultList[ind]

# This function takes the user input from the frontend and 
# returns a response from the chat training database or
# returns a default response if the bot confidence level is too low.
def botResponse(user_input):
    bot = initChat()
    bot_input = bot.get_response(user_input)
    if bot_input.confidence < 0.5:
        return selectDefault()
    else:
        return bot_input
