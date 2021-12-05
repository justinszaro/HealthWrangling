from SQLConnect import SQLConnect
from datetime import datetime


def insertIntoDict(line, dct):
    data_type, date, value = line.split(',')
    date, time = date.split()
    if date in dct.keys():
        dct[date] = (float(dct[date]) + float(value)) / 2
    else:
        dct[date] = float(value)
    return dct


def getData(filename):
    bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned = [dict(), dict(), dict(), dict(),
                                                                                   dict()]
    types = {"BodyMassIndex": bodyMassIndex, "BodyMass": bodyMass, "BodyFatPercentage": bodyFatPercentage,
             'LeanBodyMass': leanBodyMass, 'BasalEnergyBurned': basalEnergyBurned}
    with open(filename) as in_file:
        for line in in_file:
            data_type = line.strip().split(',')[0]
            if data_type in types.keys():
                types[data_type] = insertIntoDict(line, types[data_type])
    return bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned


def getAllDates(bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned):
    dates = set()
    return dates.union(bodyMassIndex.keys(), bodyMass.keys(), bodyFatPercentage.keys(), leanBodyMass.keys(),
                       basalEnergyBurned.keys())


def getDayOfTheWeek(date):
    datetimeObject = datetime.strptime(date, '%Y-%m-%d')
    day = datetimeObject.weekday()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days[day]


def addDataToSQL(dates, bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned):
    connector = SQLConnect()
    connector.useDatabase('health')
    connector.createTable('Fitindex', ['date DATE', 'bodyMassIndex FLOAT', 'bodyMass FLOAT', 'bodyFatPercentage FLOAT',
                                       'leanBodyMass FLOAT', 'basalEnergyBurned FLOAT', 'dayOfTheWeek varchar(255)'])
    for date in dates:
        connector.insertIntoTable('Fitindex', [date, bodyMassIndex.get(date, 0.0), bodyMass.get(date, 0.0),
                                               bodyFatPercentage.get(date, 0.0), leanBodyMass.get(date, 0.0),
                                               basalEnergyBurned.get(date, 0.0), getDayOfTheWeek(date)])
    connector.commit()


def main():
    bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned = getData('data/fitindex.csv')
    dates = getAllDates(bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned)
    addDataToSQL(dates, bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned)


if __name__ == '__main__':
    main()
