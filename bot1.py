import nltk
import os
import time
import sys
sys.path.insert(0, os.getcwd())
import Chatbot
sys.path.insert(0, os.getcwd())
import art
from slackclient import SlackClient
from newspaper import Article
import re, string
import MySQLdb
import pyttsx3
# starterbot's ID as an environment variable
BOT_ID = 'U7RHG06GL'
location = 'https://en.wikipedia.org/wiki/Machine_learning'
# constants
AT_BOT = "<@" + BOT_ID + ">"
EXAMPLE_COMMAND = "do"

# instantiate Slack & Twilio clients
slack_client = SlackClient('xoxb-263594006564-FGqddMF8t08x8N7Oq4i57vs1')

def answer_question ( answer , channel ) :
    response = answer
    response = response.replace( '0' , '' )
    response = response.replace( '1' , '' )
    response = response.replace( '2' , '' )
    response = response.replace( '3' , '' )
    response = response.replace( '4' , '' )
    response = response.replace( '5' , '' )
    response = response.replace( '6' , '' )
    response = response.replace( '7' , '' )
    response = response.replace( '8' , '' )
    response = response.replace( '9' , '' )
    slack_client.api_call ("chat.postMessage" , channel = channel , text = response , as_user = True )

def retrain ( where  ):
    data = art.train ( where )
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize ( data )
    le = len ( sentences )
    for i in range ( 0 , le ):
         sentences [ i ] = re.sub(r'([^\s\w]|_)+', '', sentences [ i ] )
    return sentences

def parse_slack_output( slack_rtm_output , sentences  ):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if 'text' in output and 'channel' in output :
                answer = Chatbot.return_answer ( sentences , output ['text' ]  )
                new_location = None
                if 'bot_id' not in output :
                    if re.search("(?P<url>https?://[^\s]+)", output [ 'text' ] ) is not None :
                         new_location = re.search("(?P<url>https?://[^\s]+)", output [ 'text' ] ) .group ( "url" )
                         new_location = new_location .replace ('>' , '' )
                channel = output [ 'channel' ]
                if answer is not None  :
                    if 'bot_id' not in output :
                        if new_location is not None :
                           answer = "I'm taking you to the new location . Continue by asking the questions you desire for the next topic :) !"
                        answer_question ( answer , channel )
                        cur.execute("""INSERT INTO raspunsuri VALUES (%s,%s)""",( answer , output [ 'text' ] ))
                        db.commit()
                        engine = pyttsx3.init() ;
                        engine.say( answer ) ;
                        engine.runAndWait() ;
                        return answer , output [ 'channel' ] , new_location
                return answer , output ['channel' ] , new_location
    return None , None , None

if __name__ == "__main__":
    db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="Darius",         # your username
                     passwd="grigore",  # your password
                     db="educational_website" )
    cur = db.cursor()
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        sentences = retrain ( location )
        while True :
            answer , channel , new_location = parse_slack_output( slack_client.rtm_read() , sentences )
            if new_location is not None :
                location = new_location
                sentences = retrain ( location )
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
