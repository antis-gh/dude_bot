from datetime import datetime
import time
import schedule
from pytz import timezone
import wednesday as wd


# Check if today is any user's from the list birthday
# If yes returnes user's name from NAMES list
# If no returnes False
def isBirthday(BDAYS, NAMES):
    today = wd.tlnTime()
    todayNoYear = today.strftime('%m-%d')
    for i in range(len(BDAYS)):
        if(str(todayNoYear) == BDAYS[i]):
            print (today, "It's bday of ", NAMES[i])
            name = NAMES[i]
            return name
    print("No bdays today")
    return False

# Send happy bitrhday message and pic to chat
def sendBirthdayMessage(BDAYS, NAMES, bot, chatId):
    if (isBirthday(BDAYS, NAMES) != False):
        bot.send_message(chatId, "\U00002728 Сегодня день рождения " + isBirthday(BDAYS, NAMES) + "!\nПоздравляю, кожаный мешок!\U0001F942\n                                                Железяка")
        bot.send_photo(chatId, photo=open("./dudes/bday/bday.jpg", "rb"))

# Schedule an automatic Birthday message sending
# Timezones are not supported! Uses server time!
def scheduleBirthdayMessage(BDAYS, NAMES, bot, chatId, time):
    date = wd.tlnTime()
    schedule.every().day.at(time).do(sendBirthdayMessage, BDAYS, NAMES, bot, chatId)
    print(date, "scheduleBirthdayMessage is set to", time, "(server time)")

def printBdays(BDAYS, NAMES, bot, chatId):
    list="Our birthdays, my dude:\n"
    for i in range(len(BDAYS)):
        formatedName=formatName(NAMES[i])
        date=datetime.strptime(BDAYS[i], "%m-%d")
        formatDate=date.strftime("%b-%d")
        list += formatDate + " - " + formatedName+"\n"
    bot.send_message(chatId, list)
    print(wd.tlnTime(), "Bdlist was printed")

#Remove @ from usernames to not ping person in chat
def formatName(str):
    if (str[0] == "@"):
        str = str[1:]
        return str
    else:
        return str
