#This python script is only used to initialize the buddybot service if it is hosted 
#on a web server like NGINX. 
from buddyBotController import app

if __name__ == "__main__":
    app.run()
