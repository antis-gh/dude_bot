from datetime import datetime
import time
import os
import random
import schedule

# Check if it's Wednesday today (according to passed timezone date)
# Output: True/False
def isWednesday(date):
    day = date.isoweekday()
    print (date, "weekday:", day)

    if (day==3):
        return True
    return False

# Send a random Frog pic if it's a Wednesday
def sendFrog(date, bot, chatId):
    if(isWednesday(date) == True):
        bot.send_photo(chatId, photo=open(getRangomPic("./dudes"), "rb"))
    else:
        bot.send_message(chatId, "It's NOT Wednesday, dude! Stop it!")
        bot.send_photo(chatId, photo=open(getRangomPic("./not"), "rb"))

# Schedule an automatic Wednesday Frog pic sending
# Timezones are not supported! Uses server time! (UTC)
def scheduleWednesdayFrog(date, bot, chatId, time):
    #schedule.every().wednesday.at(time).do(sendFrog, date, bot, chatId)
    schedule.every().monday.at(time).do(sendFrog, date, bot, chatId)
    print(date, "scheduleWednesdayFrog is set to", time, "(server time)")

# Choose a random pic from dir
# Input: path to dir
# Output: path to a ramdom pic in dir
def getRangomPic(path):
    files = os.listdir(path)
    randomPic = random.choice(files)

    return path+"/"+randomPic
