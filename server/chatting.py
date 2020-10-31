from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from chatterbot.trainers import ChatterBotCorpusTrainer
import random


def initChat():
    default_response = 'Make it make sense (ノಠ益ಠ)ノ彡┻━┻'
    bot = ChatBot(
    'BuddyBot',
    storage_adapter='chatterbot.storage.SQLStorageAdapter',
    database_uri='mysql+mysqldb://admin:dreamteam1234@buddybot.c2ao7w5qbjh5.us-east-2.rds.amazonaws.com:3306/test',
    logic_adapters=[
        {
            'import_path': 'chatterbot.logic.BestMatch',
            'default_response': ['Make it make sense (ノಠ益ಠ)ノ彡┻━┻', 'Oof I don\'t quite understand'],
            'maximum_similarity_threshold': 0.90
        }
    ])

    trainer = ChatterBotCorpusTrainer(bot)
    trainer2 = ListTrainer(bot)

    trainer.train(
        "chatterbot.corpus.english.greetings",
        "chatterbot.corpus.english.conversations",
        "chatterbot.corpus.english.botprofile",
        "chatterbot.corpus.english.ai"
    )

    trainer2.train([
        'Hey',
        'Hello',
        'How\'s it going?',
        'It\'s going great!'
    ])

    return bot, default_response

def selectDefault():
    defaultList = ['Make it make sense (ノಠ益ಠ)ノ彡┻━┻', 'Oof I don\'t quite understand']
    ind = random.randint(0, len(defaultList) - 1)
    return defaultList[ind]

def botResponse(user_input, bot, default_response):
    bot_input = bot.get_response(user_input)
    if bot_input.confidence < 0.5:
        return selectDefault()
    else:
        return bot_input