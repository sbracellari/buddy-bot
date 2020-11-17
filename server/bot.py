import os
import discord
from dotenv import load_dotenv
from buddyBotController import bot_response, app_context, chat_response

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord. What\'s good?')

@client.event
async def on_message(message):
    if message.author == client.user or not message.content.startswith("!bb"):
        return

    if message.content.startswith("!bb"):
        with app_context:
            response = bot_response(message.content[3:])
        await message.channel.send(response)
    elif message.content.startswith("!cb"):
        with app_context:
            response = chat_response(message.content[3:])
        await message.channel.send(response)

client.run(TOKEN)
