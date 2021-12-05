from SQLConnect import SQLConnect
from datetime import datetime


def insertIntoDict(date, value, dictionary):
    if date in dictionary.keys():
        dictionary[date] = str((float(dictionary[date]) + float(value)).__round__())
    else:
        dictionary[date] = str(value)
    return dictionary


def addTotalToDictionary(line, dictionary):
    data_type, date, value = line.split(',')
    date, time = date.split()
    if date in dictionary.keys():
        dictionary[date].append(float(value))
    else:
        dictionary[date] = [float(value)]
    return dictionary


def addToDictionary(line, dictionary):
    data_type, date, value = line.split(',')
    date, time = date.split()
    dictionary = insertIntoDict(date, float(value), dictionary)
    return dictionary


def getData(filename):
    heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned = [dict(), dict(), dict(),
                                                                                           dict(), dict()]
    with open(filename) as file:
        for line in file:
            data_type = line.split(',')[0]
            if data_type == "HeartRate":
                heartRate = addTotalToDictionary(line, heartRate)
            elif data_type == "StepCount":
                stepCount = addToDictionary(line, stepCount)
            elif data_type == "DistanceWalkingRunning":
                distanceWalkingRunning = addTotalToDictionary(line, distanceWalkingRunning)
            elif data_type == "BasalEnergyBurned":
                basalEnergyBurned = addToDictionary(line, basalEnergyBurned)
            elif data_type == "ActiveEnergyBurned":
                activeEnergyBurned = addToDictionary(line, activeEnergyBurned)
    return [heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned]


def getAllDates(heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned):
    dates = set()
    return dates.union(heartRate.keys(), stepCount.keys(), distanceWalkingRunning.keys(), basalEnergyBurned.keys(),
                       activeEnergyBurned.keys())


def getDayOfTheWeek(date):
    date = date.split()[0]
    if date == '9999:01:01':
        return "None"
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


def quotes(string):
    return '"' + string + '"'


def getAverage(heartRate, date):
    avg = sum(heartRate.get(date, [0])) / len(heartRate.get(date, [1]))
    return str(avg)


def addDataToSQL(dates, heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned):
    connector = SQLConnect()
    connector.useDatabase('health')
    connector.createTable('AppleWatch', ['date DATE', 'averageHeartRate FLOAT', 'stepCount FLOAT',
                                         'distanceWalkingRunning FLOAT', 'basalEnergyBurned FLOAT',
                                         'activeEnergyBurned FLOAT', 'dayOfTheWeek varchar(255)'])
    for date in dates:
        connector.insertIntoTable('AppleWatch',
                                  [date, getAverage(heartRate, date), stepCount.get(date, '0.0'),
                                   str(sum(distanceWalkingRunning.get(date, [0.0]))),
                                   basalEnergyBurned.get(date, '0.0'),
                                   activeEnergyBurned.get(date, '0.0'), getDayOfTheWeek(date)])
    connector.commit()


def main():
    heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned = getData('data/appleWatch.csv')
    dates = getAllDates(heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned)
    addDataToSQL(dates, heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned)


if __name__ == "__main__":
    main()
