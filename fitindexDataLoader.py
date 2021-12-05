from SQLConnect import SQLConnect
from datetime import datetime


def insertIntoDict(line, dict):
    data_type, date, value = line.split(',')
    date, time = date.split()
    if date in dict.keys():
        dict[date] = str(((float(dict[date]) + float(value)) / 2).__round__(2))
    else:
        dict[date] = str(float(value).__round__(2))
    return dict


def getData(filename):
    bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned = [dict(), dict(), dict(), dict(),
                                                                                   dict()]
    with open(filename) as in_file:
        for line in in_file:
            data_type = line.strip().split(',')[0]
            if data_type == "BodyMassIndex":
                bodyMassIndex = insertIntoDict(line, bodyMassIndex)
            elif data_type == "BodyMass":
                bodyMass = insertIntoDict(line, bodyMass)
            elif data_type == "BodyFatPercentage":
                bodyFatPercentage = insertIntoDict(line, bodyFatPercentage)
            elif data_type == 'LeanBodyMass':
                leanBodyMass = insertIntoDict(line, leanBodyMass)
            elif data_type == 'BasalEnergyBurned':
                basalEnergyBurned = insertIntoDict(line, basalEnergyBurned)
    return [bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned]


def getAllDates(bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned):
    dates = set()
    return dates.union(bodyMassIndex.keys(), bodyMass.keys(), bodyFatPercentage.keys(), leanBodyMass.keys(),
                       basalEnergyBurned.keys())


def getDayOfTheWeek(date):
    datetimeObject = datetime.strptime(date, '%Y-%m-%d')
    day = datetimeObject.weekday()

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


def addDataToSQL(dates, bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned):
    connector = SQLConnect()
    connector.useDatabase('health')
    connector.createTable('Fitindex', ['date DATE', 'bodyMassIndex FLOAT', 'bodyMass FLOAT', 'bodyFatPercentage FLOAT',
                                       'leanBodyMass FLOAT', 'basalEnergyBurned FLOAT', 'dayOfTheWeek varchar(255)'])
    for date in dates:
        connector.insertIntoTable('Fitindex', [date, bodyMassIndex.get(date, '0.0'), bodyMass.get(date, '0.0'),
                                               bodyFatPercentage.get(date, '0.0'), leanBodyMass.get(date, '0.0'),
                                               basalEnergyBurned.get(date, '0.0'), getDayOfTheWeek(date)])
    connector.commit()


def main():
    bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned = getData('data/fitindex.csv')
    dates = getAllDates(bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned)
    addDataToSQL(dates, bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned)


if __name__ == '__main__':
    main()
