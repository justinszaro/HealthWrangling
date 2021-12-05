from SQLConnect import SQLConnect
from datetime import datetime
import calendarDataLoader as cd


def convertToFlOz(value):
    return float(value) * 0.033814


def insertIntoDict(dictionary, date, value):
    if dictionary.get(date, None) is None:
        dictionary[date] = value
    else:
        dictionary[date] = dictionary[date] + value
    return dictionary


def getData(filename):
    hidrateData = dict()
    with open(filename) as in_file:
        for line in in_file:
            data_type, dateTime, value = line.strip().split(',')
            hidrateData = insertIntoDict(hidrateData, dateTime, convertToFlOz(value))
    return hidrateData


def getDayOfTheWeek(date):
    if len(str(date)) > 19:
        date = str(date)[:-6]
    datetimeObject = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    day = datetimeObject.weekday()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days[day]


def isWithinDate(date, activity):
    return activity[2].date() < date.date() < activity[4][0].date()


def isWithinTime(date, activity):
    return activity[2].time() < date.time() < activity[3].time()


def isOnDay(date, activity):
    return cd.getDayOfTheWeek(date) in activity[1]


def occursOnce(activity):
    return '9999-01-01 00:00:00+00:00' == activity[-1][0]


def getHidrationCategory(date, calendarData):
    date = datetime.fromisoformat(date)
    for activity in calendarData:
        if occursOnce(activity) and activity[2].replace(tzinfo=None) < date < activity[3].replace(tzinfo=None):
            return activity[0]
        elif occursOnce(activity):
            pass
        elif isWithinDate(date, activity) and isWithinTime(date, activity) and isOnDay(date, activity):
            return activity[0]
    return 'None'


def toSQL(data, calendarData):
    connector = SQLConnect()
    connector.useDatabase('health')
    connector.createTable('Hidrate', ['date DATETIME, amount FLOAT, dayOfTheWeek varchar(255), hidrationCategory '
                                      'varchar(255)'])
    for key in data.keys():
        connector.insertIntoTable('Hidrate',
                                  [key, data[key], getDayOfTheWeek(key), getHidrationCategory(key, calendarData)])
    connector.commit()


def main(calendarData):
    hidrateData = getData('data/hidrate.csv')
    toSQL(hidrateData, calendarData)


if __name__ == '__main__':
    main(cd.main())
