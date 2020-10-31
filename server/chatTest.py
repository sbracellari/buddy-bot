from chatting import initChat, botResponse

chatbot = initChat()

print(type(str(botResponse('Hello', chatbot[0], chatbot[1]))))

