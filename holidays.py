import json
from datetime import datetime, date
import wednesday as wd
import calendar
import schedule

# Check JSON file for holiday match
def checkHolidayFromFile(bot, chatId):
    holidays = open('holidays.json', encoding='utf-8')
    data = json.load(holidays)
    today = wd.tlnTime()
    dayOfYear = wd.tlnTime().timetuple().tm_yday
    todayNoYear = today.strftime('%m-%d')

    for i in data['holidays']:
        if (todayNoYear == i["exact_date"]):
            print(i["exact_date"], i["holiday"])
            bot.send_message(chatId, "Сегодня " + i["holiday"] + "! \n" + i["text"])
            if (i["picture"] != None):
                bot.send_photo(chatId, photo=open("./holidays/" + i["picture"], "rb"))
        elif (dayOfYear==i["exact_year_day"]):
            print(i["exact_year_day"], i["holiday"])
            bot.send_message(chatId, "Сегодня " + i["holiday"] + "! \n" + i["text"])
            if (i["picture"] != None):
                bot.send_photo(chatId, photo=open("./holidays/" + i["picture"], "rb"))
        elif (i["specific_date"] != None and todayNoYear==getSysadminDay()):
            print(i["holiday"])
            bot.send_message(chatId, "Сегодня " + i["holiday"] + "! \n" + i["text"])
            if (i["picture"] != None):
                bot.send_photo(chatId, photo=open("./holidays/" + i["picture"], "rb"))

    print(today, "Holidays checked")

    holidays.close()

# Define a sysadmin day (last friday of July)
def getSysadminDay():
    year = datetime.now().year
    month = 7
    last_day = calendar.monthrange(year, month)[1]
    last_weekday = calendar.weekday(year, month, last_day)
    last_friday = last_day - ((7 - (4 - last_weekday)) % 7)
    sysAdminDayNoYear ="07-" + str(last_friday)

    return sysAdminDayNoYear

# Schedule an automatic Holiday message sending
# Timezones are not supported! Uses server time!
def scheduleHolidayMessage(bot, chatId, time):
    date = wd.tlnTime()
    schedule.every().day.at(time).do(checkHolidayFromFile, bot, chatId)
    print(date, "scheduleHolidayMessage is set to", time, "(server time)")
