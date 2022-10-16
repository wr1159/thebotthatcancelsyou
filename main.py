import os
import random
import telebot
from telebot.async_telebot import AsyncTeleBot
from telebot import types,util
from flask import Flask
from threading import Thread
from dbhelper import DBHelper
import time
from replit import db


'''
Goal: A bot that uses a sqlite db to have counters. 

Planned features: 
1. Cancel someone (Add counter to someone) 
1.1 To cancel someone we need a few people to cancel someone 
2. Get leaderboard (Fetch counters of everyone and sort)
2.1 : Format -> 
  Index. Name: Counter
  Index. Name: Counter

1.1 
person A cancels person S
timestamp T is stored
add 1 to temporary value V
person B cancels person S
check if timestamp is <5 minutes from timestamp T
if yes: add 1 to temporary value V -> update timestamp (refresh timing)
     If V > 30% of group member, counter of person S gets 1 added
if no: update timestamp -> temporary value V reset to 1
'''

API_KEY = os.getenv('API_KEY') 
TOKEN = os.getenv('TOKEN')
PORT = int(os.environ.get('PORT', 5000))

app = Flask('')

@app.route('/')

def home():
    return "I'm alive"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
  
keep_alive()
# bot = telebot.TeleBot(API_KEY)
bot = telebot.TeleBot(TOKEN)
# bot = AsyncTeleBot(API_KEY)

sent_poll = ""
target = ""
count = 0
@bot.message_handler(commands=['cancel'])
def cancel(message):
  global target
  global count
  global sent_poll
  target = message.text[message.entities[1].offset:]
  if target in db.keys():
    count = db[target]
  sent_poll = bot.send_poll(chat_id= message.chat.id,
    question= "do we cancel " + target,
    options= ("Yes", "No"),
    is_anonymous= False,
    open_period = 10)
  print(message.text[message.entities[1].offset:])
  print("Cancel " + str(message.entities[0]))  
  
@bot.poll_handler(func = None)
def poll_stop(poll):
  print(poll)
  # if(poll.is_closed):
  options = poll.options
  print(options[0].voter_count)
  print(options[1].voter_count)
  print(target)
  if(options[0].voter_count > options[1].voter_count):
    if(target not in db.keys()):
      db[target] = count
    else:
      db[target] = count + 1
  
  
  
@bot.message_handler(commands=['leaderboard'])
def leaderboard(message):
  print(message.chat.id)
  keys = db.keys()
  cancelled = list()
  for key in keys:
    cancelled.append(str(db[key]) + "  " + key)
  cancelled.sort()
  cancelled.reverse()
  output_message = ""
  for i in range(len(cancelled)):
    output_message += str(i+1) + ". "
    output_message += cancelled[i][2:] + ":  " + cancelled[i][:1] 
    output_message += "\n"
  if output_message == "":
    output_message = "leaderboard is empty as of now."
  bot.send_message(chat_id=message.chat.id, text= output_message)
  print("Leaderboard called")

# import asyncio
# asyncio.run(bot.polling())
bot.infinity_polling()

#code to model after
# @bot.message_handler(commands=['praiseyou'])
# def praiseyou(message):
#   markup = types.ForceReply(selective=False)
#   bot.reply_to(
#     message,
#     welcomemessage, reply_markup=markup
#   )
  
# @bot.message_handler(commands = ['deldeldel'])
# def delete_message(message):
#   if getattr(getattr(message, 'from_user'),'username') != 'thaddeusong':
#     bot.send_message(getattr(getattr(message,'chat'),'id'), 'Get a life CS nerd')
#   else:
#     items = db.get_items()
#     badcompliment = getattr(message, 'text').replace("/deldeldel ","")
#     if badcompliment in items:
#       bot.send_message(getattr(getattr(message, 'chat'), 'id'), "Bad compliment deleted")
#       db.delete_item(getattr(message, 'text').replace("/deldeldel ", ""))  
#     else:
#       bot.send_message(getattr(getattr(message,'chat'), 'id'), 'not in db')
      
# @bot.message_handler(regexp='(praisebot)')
# def handle_message(message):
#   try:
#     reply_content = getattr(getattr(message, 'reply_to_message'), 'text')
#   except AttributeError:
#     reply_content = ""
#   items = db.get_items()
#   if reply_content != praiseyoumessage:
#     bot.send_message(getattr(getattr(message, 'chat'), 'id'), "Reply to my previous message with my compliment!")
#   elif len(getattr(message,'text')) > 300:
#     bot.send_message(getattr(getattr(message, 'chat'), 'id'), "That's too long of a compliment!")
#   elif getattr(message, 'text') in items:
#     bot.send_message(getattr(getattr(message, 'chat'), 'id'),
#                        "I've heard that one.")
#   else:
#     bot.send_message(getattr(getattr(message, 'chat'), 'id'),
#                        "Thanks! I'll remember that one.")
#     db.add_item(getattr(message, 'text'))

# @bot.message_handler(commands=['praiseme'])
# def praiseme(message):
#   items = db.get_items()
#   name = getattr(getattr(message, 'from_user'), 'first_name')
#   compliment = random.choice(items)
#   compliment = compliment.replace("'praisebot'", name)
#   compliment = compliment.replace("/praisebot", name)
#   compliment = compliment.replace('praisebot', name)
#   compliment = compliment.replace('Praisebot', name)
#   bot.send_message(getattr(getattr(message, 'chat'), 'id'), compliment)


# @bot.message_handler(commands=['plan_c'])
# def erase_db(message):
#   if getattr(getattr(message, 'from_user'),'username') != 'thaddeusong':
#     bot.send_message(getattr(getattr(message,'chat'),'id'), 'Get a life CS nerd')
#   else:
#     bot.reply_to(message, "DESTRUCTION!!!!!")
#     items = db.get_items()
#     for item in items:
#       db.delete_item(item)
      
# @bot.message_handler(commands=['list_all'])
# def list_all(message):
#   if getattr(getattr(message, 'from_user'),'username') != 'thaddeusong':
#     bot.send_message(getattr(getattr(message,'chat'),'id'), 'Get a life CS nerd')
#   else: 
#     items = db.get_items()
#     compliments = "#:"
#     for item in items:
#       compliments = compliments + item + "\n#:"
#     splitted_compliments = util.split_string(compliments, 3000)
#     for text in splitted_compliments:
#       bot.reply_to(message, text)

# @bot.message_handler(commands=['list_recent'])
# def list_recent(message):
#   if getattr(getattr(message, 'from_user'),'username') != 'thaddeusong':
#     bot.send_message(getattr(getattr(message,'chat'),'id'), 'Get a life CS nerd')
#   else:
#     items = db.get_items()
#     compliments = "#:"
#     try:
#       number = int(getattr(message,'text').replace("/list_recent ", ""))
#     except:
#       number = 0
#     for i in range(0, len(items)):
#       if i > len(items) - number:
#         compliments = compliments + items[i] + "\n#:"
#     bot.reply_to(message, compliments)
      
  
# @bot.message_handler(commands=['prune_list'])
# def prune_list(message):
#   if getattr(getattr(message, 'from_user'),'username') != 'thaddeusong':
#     bot.send_message(getattr(getattr(message,'chat'),'id'), 'Get a life CS nerd')
#   items = db.get_items()
#   for item in items:
#     if len(item) > 300: 
#       db.delete_item(item)
# bot.polling()

# @bot.message_handler(commands=['tidy_list'])
# def tidy_list(message):
#   if getattr(getattr(message, 'from_user'),'username') != 'thaddeusong':
#     bot.send_message(getattr(getattr(message,'chat'),'id'), 'Get a life CS nerd')
#   else:
#     items = db.get_items()
#     for item in items:
#       item.replace("Praisebot", "praisebot")
#       item.replace("'praisebot'", "praisebot")
#       item.replace("/praisebot", "praisebot")