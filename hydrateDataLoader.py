from SQLConnect import SQLConnect
from datetime import datetime


def convertToFlOz(value):
    return (float(value) * 0.033814).__round__(2)


def toOutputFile(outfile, line):
    data_type, date, value = line.strip().split(',')
    outfile.write(','.join([date, str(convertToFlOz(value))]) + '\n')


def insertIntoDict(dictionary, date, value):
    if dictionary.get(date, None) is None:
        dictionary[date] = value.__round__(2)
    else:
        dictionary[date] = (dictionary[date] + value).__round__(2)
    return dictionary


def getData(filename):
    hidrateData = dict()
    outfile = open('data/HydrateDataPoints.csv', 'w')
    with open(filename) as in_file:
        for line in in_file:
            data_type, dateTime, value = line.strip().split(',')
            hidrateData = insertIntoDict(hidrateData, dateTime, convertToFlOz(value))
            toOutputFile(outfile, line)
    outfile.close()
    return hidrateData


def getDayOfTheWeek(date):
    datetimeobject = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
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


def getHydrationCategory(date):
    return "TBD"


def toSQL(data):
    connector = SQLConnect()
    connector.useDatabase('health')
    connector.create_table('Hidrate', ['date DATETIME, amount FLOAT, dayOfTheWeek varchar(255), hydrationCategory '
                                       'varchar(255)'])
    for key in data.keys():
        connector.insert_into_table('Hidrate', [key, str(data[key]), getDayOfTheWeek(key), getHydrationCategory(key)])
    connector.commit()


def main():
    hydrateData = getData('data/hidrate.csv')
    toSQL(hydrateData)


if __name__ == '__main__':
    main()
