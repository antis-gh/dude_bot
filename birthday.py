from datetime import datetime
import time
import schedule

# Check if today is any user's from the list birthday
# If yes returnes user's name from NAMES list
# If no returnes False
def isBirthday(date, BDAYS, NAMES):
    today = date.date()
    todayNoYear = today.strftime('%m-%d')
    for i in range(len(BDAYS)):
        if(str(todayNoYear) == BDAYS[i]):
            print (date, "It's bday of ", NAMES[i])
            name = NAMES[i]
            return name
    return False

# Send happy bitrhday message and pic
def sendBirthdayMessage(date, BDAYS, NAMES, bot, chatId):
    if (isBirthday(date, BDAYS, NAMES) != False):
        bot.send_message(chatId, "\U00002728 Сегодня день рождения " + isBirthday(date, BDAYS, NAMES) + "!\nПоздравляю, кожаный мешок!\U0001F942\n                                                Железяка")
        bot.send_photo(chatId, photo=open("./dudes/bday/bday.jpg", "rb"))

# Schedule an automatic Birthday message sending
# Timezones are not supported! Uses server time!
def scheduleBirthdayMessage(date, BDAYS, NAMES, bot, chatId, time):
    schedule.every().day.at(time).do(sendBirthdayMessage, date, BDAYS, NAMES, bot, chatId)
    print(date, "scheduleBirthdayMessage is set to", time, "(server time)")

#Remove @ from usernames to not ping person in chat
def formatName(str):
    if (str[0] == "@"):
        str = str[1:]
        return str
    else:
        return str
