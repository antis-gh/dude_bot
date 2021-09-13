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
import wednesday as wd
import birthday as bd

TOKEN = os.environ["TOKEN"] # Set a system env var with a token
bot = telebot.TeleBot(TOKEN)

# Dates and timezones
serverDate = datetime.now()
tlnTZ = timezone('Europe/Tallinn')
tlnCurrentTime = serverDate.astimezone(tlnTZ)

# Scheduled times
# Timezones are not supported! Server time is used! (UTC)
bdMessageTime = "11:55"
frogMessageTime = "11:57"

# Set a system env vars for userlist and birthday list
# NAMES_HEROKU var value should be in string format (no spaces)
# Example: Name1,Name2,Name3,Name4
NAMES_HEROKU = os.environ["NAMES"]
# BDAYS_HEROKU var value should be in string format (no spaces), same amount names as amount of names, dates in %m-%d
# Example: 11-03,12-23,09-10,03-03
BDAYS_HEROKU = os.environ["BDAYS"]
# For local testing hardcoded values:
# BDAYS_HEROKU = "02-12,09-11,06-03,09-13,08-20"
# NAMES_HEROKU = "Name1,Name2,Name3,Name4,Name5"

# As Heroku can't store arrays in env vars, workaround to convert NAMES_HEROKU and BDAYS_HEROKU strings to arrays:
NAMES = NAMES_HEROKU.split(",")
BDAYS = BDAYS_HEROKU.split(",")

# Timers for polling restart
BOT_INTERVAL = 3
BOT_TIMEOUT = 30

# Handler wrapper to restart polling on crash
def botactions(bot):
    # Main func to start the bot, read "/dude" key
    # Runs schedule for automatic Wednesday Frog pic sendout: scheduleWednesdayFrog
    # Runs schedule for automatic Brithday message Frog pic sendout: scheduleBirthdayMessage
    # Runs schedule for keening connection alive: connectionPing
    @bot.message_handler(commands=["dude"])
    def starter(message):
        chatId = message.chat.id
        print(tlnCurrentTime,chatId)
        bot.send_message(chatId, "Dude!")

        setSchedules(chatId, message)

    # Read "/wednesday" key, send a response with a Frog pic
    @bot.message_handler(commands=["wednesday"])
    def sendWednesdayFrog(message):
        chatId = message.chat.id
        wd.sendFrog(tlnCurrentTime, bot, chatId)

    # Read "/dude_help" key
    @bot.message_handler(commands=["dude_help"])
    def open_coub(message):
        chatId = message.chat.id
        bot.send_message(chatId, "Here's what I can do, dude:")
        bot.send_message(chatId, "/wednesday - Send a frog if it's Wednesday;\n/bdlist - List of dude's birthdays;\nAlso:\n- Sending a Frog picture every Wednesday at 10AM;\n- Sending a b-day messages at 10-10AM")

    # Start or Rrestart bot and delete a call message
    # Bot should have chat admin rights to use the delete functin
    @bot.message_handler(commands=["dude_restart"])
    def deleteMsgAndRestart(message):
        chatId = message.chat.id
        messageId = message.message_id
        bot.delete_message(chatId, messageId)
        bot.send_message(chatId, "Сорян, я рестартанулся")
        print("Restarted with /dude_resrtart")
        setSchedules(chatId, message)

    # Send user's birthday list
    @bot.message_handler(commands=["bdlist"])
    def bdList(message):
        chatId = message.chat.id
        print(tlnCurrentTime, "Bdlist was called")
        list="Our birthdays, my dude:\n"
        for i in range(len(BDAYS)):
            formatedName=bd.formatName(NAMES[i])
            date=datetime.strptime(BDAYS[i], "%m-%d")
            formatDate=date.strftime("%b-%d")
            list += formatDate + " - " + formatedName+"\n"
        bot.send_message(chatId, list)

# Schedule ping every 10 min to keep Heroku Dyno alive
def connectionPing(msg):
    schedule.every(10).minutes.do(setChatId, msg)

# Pointless function for Ping
def setChatId(message):
    chatId = message.chat.id
    print(tlnCurrentTime,"Ping (chatId Updated)", chatId)

# Schedules caller function
def setSchedules(chatId, message):

    chatTitle = bot.get_chat(chatId).title
    wd.scheduleWednesdayFrog(updateTlnTime(tlnCurrentTime), bot, chatId, frogMessageTime)
    bd.scheduleBirthdayMessage(updateTlnTime(tlnCurrentTime), BDAYS, NAMES, bot, chatId, bdMessageTime)
    connectionPing(message)
    print(updateTlnTime(tlnCurrentTime), "Schedule is set for", chatTitle, chatId)
    while True:
        schedule.run_pending()
        time.sleep(1)

def updateTlnTime(time):
    time=serverDate.astimezone(tlnTZ)
    return time

###################################
# Keep connection alive solution from https://gist.github.com/David-Lor/37e0ae02cd7fb1cd01085b2de553dde4
def bot_polling():
    print(tlnCurrentTime,"Starting bot polling now")
    while True:
        try:
            print(tlnCurrentTime,"New bot instance started")
            bot = telebot.TeleBot(TOKEN)
            botactions(bot)
            bot.polling(none_stop=True, interval=BOT_INTERVAL, timeout=BOT_TIMEOUT)
        except Exception as ex: #Error in polling
            print(tlnCurrentTime,"Bot polling failed, restarting in {}sec. Error:\n{}".format(BOT_TIMEOUT, ex))
            bot.stop_polling()
            sleep(BOT_TIMEOUT)
        else: #Clean exit
            bot.stop_polling()
            print(tlnCurrentTime,"Bot polling loop finished")
            break #End loop

bot_polling()
