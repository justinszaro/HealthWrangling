from SQLConnect import SQLConnect
from datetime import datetime


def convertToFlOz(value):
    return float(value) * 0.033814


def insertIntoDict(dictionary, date, value):
    if dictionary.get(date, None) is None:
        dictionary[date] = value.__round__(2)
    else:
        dictionary[date] = (dictionary[date] + value).__round__(2)
    return dictionary


def getData(filename):
    hydrateData = dict()
    with open(filename) as in_file:
        for line in in_file:
            components = line.split()
            date = components[7][11:]
            value = components[13][6:].strip('"/>')
            hydrateData = insertIntoDict(hydrateData, date, convertToFlOz(value))
    return hydrateData


def getDayOfTheWeek(date):
    datetimeobject = datetime.strptime(date, '%Y-%m-%d')
    day = datetimeobject.weekday()

    if day == 0:
        return 'Monday'
    elif day == 1:
        return 'Tuesday'
    elif day == 2:
        return 'Wednesday'
    elif day == 3:
        return 'Thursday'
    elif day == 4:
        return 'Friday'
    elif day == 5:
        return 'Saturday'
    elif day == 6:
        return 'Sunday'


def toSQL(data):
    connector = SQLConnect()
    connector.useDatabase('health')
    connector.create_table('Hidrate', ['date CHAR(10), amount FLOAT, dayOfTheWeek varchar(255)'])
    for key in data.keys():
        connector.insert_into_table('Hidrate', [key, str(data[key]), getDayOfTheWeek(key)])
    connector.commit()


def main():
    hydrateData = getData('hidrate.txt')
    toSQL(hydrateData)


if __name__ == '__main__':
    main()
