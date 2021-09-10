import telebot
from telebot import types
import datetime
from datetime import datetime
import time
import os
import random
import schedule
import pytz
from pytz import timezone
from time import sleep

chatId = ""
TOKEN = os.environ["TOKEN"] # Set a system env var with a token
bot = telebot.TeleBot(TOKEN)

# Dates and timezones
serverDate = datetime.now()
tlnTZ = timezone('Europe/Tallinn')
tlnCurrentTime = serverDate.astimezone(tlnTZ)

# Set a system env vars for userlist ant birthday list
# NAMES var value should be array format
# Example: ["Name1", "Name2", "Name3", "Name4"]
NAMES = os.environ["NAMES"]
# BDAYS var value should be array format, same lenght as NAMES arr, dates in %m-%d
# BDAYS[0] = NAMES[0] user Birthday etc.
# Example: ["11-03", "12-23", "09-10", "03-03"]
BDAYS = os.environ["BDAYS"]

BOT_INTERVAL = 3
BOT_TIMEOUT = 30

def botactions(bot):
    # Main func to start the bot, read "/dude" key
    # Runs schedule for automatic Wednesday Frog pic sendout: scheduleWednesdayFrog
    # Runs schedule for keening connection alive: connectionPing
    @bot.message_handler(commands=["dude"])
    def starter(message):
        chatId = message.chat.id
        print(chatId)
        bot.send_message(chatId, "Dude!")
        scheduleWednesdayFrog(chatId)
        connectionPing(message)
        sendBirthdayMessage(chatId)
        scheduleBirthdayMessage(chatId)
        while True:
            schedule.run_pending()
            time.sleep(1)

    # Read "/wednesday" key, send a response with a Frog pic
    @bot.message_handler(commands=["wednesday"])
    def sendWednesdayFrog(message):
        chatId = message.chat.id
        sendFrog(chatId)

    # Read "dude_help"
    @bot.message_handler(commands=["dude_help"])
    def open_coub(message):
        chatId = message.chat.id
        bot.send_message(chatId, "Here's what I can do, dude:")
        bot.send_message(chatId, "/wednesday - Send a frog if it's Wednesday;\n/bdlist - List our birthdays;\nAlso:\n- Sending a Frog picture every Wednesday at 10AM;\n- Sending a b-day messages at 10-10AM")

    # Start or Rrestart bot and delete a call message
    # Bot should have chat admin rights to use the delete functin
    @bot.message_handler(commands=["dude_restart"])
    def deleteMsgAndRestart(message):
        chatId = message.chat.id
        messageId = message.message_id
        bot.delete_message(chatId, messageId)

        scheduleWednesdayFrog(chatId)
        connectionPing(message)
        print(tlnCurrentTime, "I've restarted")
        while True:
            schedule.run_pending()
            time.sleep(1)

    @bot.message_handler(commands=["bdlist"])
    def bdList(message):
        chatId = message.chat.id
        list="Our birthdays:\n"
        for i in range(len(TBDAYS)):
            formatedName=formatName(TNAMES[i])
            date=datetime.strptime(TBDAYS[i], "%m-%d")
            formatDate=date.strftime("%b-%d")
            list += formatDate + " - " + formatedName+"\n"
        bot.send_message(chatId, list)

# Send a random Frog pic
def sendFrog(chatId):
    if(isWednesday() == True):
        bot.send_photo(chatId, photo=open(getRangomPic("./dudes"), "rb"))
    else:
        bot.send_message(chatId, "It's NOT Wednesday, dude! Stop it!")
        bot.send_photo(chatId, photo=open(getRangomPic("./not"), "rb"))

# Check if it's Wednesday today (Tallinn timezone)
# Output: True/False
def isWednesday():
    day = tlnCurrentTime.isoweekday()
    print (day)

    if (day==3):
        return True
    return False

# Schedule an automatic Wednesday Frog pic send
def scheduleWednesdayFrog(chatId):
    schedule.every().wednesday.at("10:00").do(sendFrog, chatId)

# Choose a random pic from dir
# Input: path to dir
# Output: path to a ramdom pic in dir
def getRangomPic(path):
    files = os.listdir(path)
    d = random.choice(files)

    return path+"/"+d

# Ping every 10 min to keep API connection alive
def connectionPing(msg):
    schedule.every(10).minutes.do(setChatId, msg)

# Pointless function for Ping bot
def setChatId(message):
    chatId = message.chat.id
    dt = datetime.now()
    print(dt," Ping (chatId Updated)")

# Check if today is any user's from the list birthday
# If yes returnes user's name from NAMES list
# If no returnes False
def isBirthday():
    today = tlnCurrentTime.date()
    todayNoYear = today.strftime('%m-%d')
    for i in range(len(TBDAYS)):
        print(TBDAYS[i])
        if(str(todayNoYear) == TBDAYS[i]):
            print ("It's bday of ", TNAMES[i])
            name = TNAMES[i]
            return name
    return False

# Send happy bitrhday message and pic
def sendBirthdayMessage(chatId):
    if (isBirthday() != False):
        bot.send_message(chatId, "Сегодня день рождения " + isBirthday() + "!\nПоздравляю, кожаный человек!")
        bot.send_photo(chatId, photo=open(".\\dudes\\bday\\bday.jpg", "rb"))

def scheduleBirthdayMessage(chatId):
    schedule.every().day.at("10:10").do(sendBirthdayMessage, chatId)

#Remove @ from usernames to not ping person in chat
def formatName(str):
    if (str[0] == "@"):
        str = str[1:]
        return str
    else:
        return str

###################################
# Keep connection alive solution from https://gist.github.com/David-Lor/37e0ae02cd7fb1cd01085b2de553dde4
def bot_polling():
    #global bot #Keep the bot object as global variable if needed
    print("Starting bot polling now")
    while True:
        try:
            print("New bot instance started")
            bot = telebot.TeleBot(TOKEN)
            botactions(bot)
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
        except Exception as ex: #Error in polling
            print("Bot polling failed, restarting in {}sec. Error:\n{}".format(BOT_TIMEOUT, ex))
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else: #Clean exit
            bot.stop_polling()
            print("Bot polling loop finished")
            break #End loop

bot_polling()
