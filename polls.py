from dateutil.rrule import rrule, WEEKLY, FR, SA
from datetime import datetime
import wednesday as wd

# Replace weekday 5 and 6 numbers to text names
def weekDayName(weekDay):
    if (weekDay == 5):
        return ("Friday")
    elif (weekDay == 6):
        return ("Saturday")

# Get 4 nearest Friday and Sataurdays (total 8 dates) dates + weekday names
def getWeekends():
    list = ""
    for date in rrule(WEEKLY, byweekday=(FR,SA), count=8):
        weekDay  = date.isoweekday()
        formatDate = date.strftime("%d-%b")
        list += formatDate + ", " + weekDayName(weekDay)+";"
    return list

# Change getWeekends() function output to array format
def weekendListToArray(list):
    return getWeekends().split(";")

# Create a poll with Friday and Saturday dates as an options + today and never options
def createPoll(bot, chatId):
    list=weekendListToArray(getWeekends())
    today = "Сегодня!"
    never = "Нет, этом году уже виделись"
    bot.send_poll(chatId, "Когда пьём?", options=[today, list[0], list[1], list[2], list[3], list[4], list[5], list[6], list[7], never], allows_multiple_answers=True, is_anonymous=False)
    print(wd.tlnTime(), "Poll created")
