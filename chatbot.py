
#import necessary libraries
from flask import Flask, render_template, request
from datetime import datetime
#from chatterbot import ChatBot
#from chatterbot.trainers import ListTrainer
import os
import io
import random
import string # to process standard python strings
import warnings
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')
import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('popular', quiet=True) # for downloading packages

# uncomment the following only the first time
# nltk.download('punkt')
# nltk.download('wordnet')

#Reading in the corpus
with open('chatbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read()
#TOkenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words

# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


# Keyword Matching
GREETING_INPUTS = ["hello", "hi", "greetings", "sup", "whats up", "hey", "heyy", "heyyy", "hello there", "how are you", "how r u", "namaste", "good morning", "good afternoon", "good evening", "yo", "kaisanba"]
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me", "It's nice to meet you.", "It's a pleasure to meet you.", "It's great seeing you. I hope you're doing well."]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    # for word in sentence:
    if sentence.lower() in GREETING_INPUTS:
        return random.choice(GREETING_RESPONSES)
    else:
        return None


# Generating response
def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I did not understand this."
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response



        
#GUI starts
app = Flask(__name__)

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/home', methods=['POST'])
def feedback():
    experience=request.form['experience']
    comments = request.form['Comments']
    name = request.form['name1']
    email = request.form['email']

    #storing the feedback with timestamp
    dateTimeObj = datetime.now()

    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")

    f = open("feedback.txt", "a")
    if(experience=='good'):
    	flag ='1'
    elif(experience=='average'):
    	flag='2'
    else:
    	flag='3'
    f.write(timestampStr +","+ "experience: " + experience +"," + flag +"," + "Comments: " + comments +"," + "name: " + name +"," + "email: " + email +"\n")
    f.close()
    return render_template('index.html')







@app.route('/process',methods=['POST'])
def process():
    leave = ['bye', 'good bye', 'see ya', 'see you later', 'take care', 'cheerio']
    user_input=request.form['user_input']
    user_response=user_input.lower()
    if(user_response not in leave):
        if(user_response=='thanks' or user_response=='thank you'):
                # flag=False
            bot_response = "You are welcome..."
            # print(bot_response)
        else:
            if(greeting(user_response)!= None):
                bot_response = greeting(user_response)
                # print(bot_response)
            else:
                bot_response = response(user_response)
                #print(bot_response)
                sent_tokens.remove(user_response)
    else:
        bot_response = random.choice(leave)
        # print(bot_response)

    # bot_response=response(user_response)
    bot_response=str(bot_response)
    # print(bot_response)
    # print("USER: " + user_response)
    # print("SFIT: "+bot_response)

    #storing the chats with timestamp
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")

    f = open("chats_storage.txt", "a")
    
    if(bot_response=='I am sorry! I did not understand this.'):
    	flag1='0'
    else:
    	flag1='1'
   
    f.write(timestampStr +","+ "USER: " + user_response +","+ "SFIT: "+ bot_response +","+ flag1 +"\n")

    # timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
    #print(t_count)
     
    f.close()


    # bot_response = "flask try karra hu hojaa fatafat..."
    return render_template('index.html', user_input=user_response, bot_response=bot_response)

if __name__=='__main__':
    app.run(debug=True, port = 5001)


