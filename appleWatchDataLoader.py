from SQLConnect import SQLConnect
from datetime import datetime


def addToDictionary(line, dictionary):
    data_type, date, value = line.split(',')
    date, time = date.split()
    if date in dictionary.keys():
        dictionary[date].append(float(value))
    else:
        dictionary[date] = [float(value)]
    return dictionary


def getData(filename):
    heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned = [dict(), dict(), dict(),
                                                                                           dict(), dict()]
    types = {"HeartRate": heartRate, "StepCount": stepCount, "DistanceWalkingRunning": distanceWalkingRunning,
             "BasalEnergyBurned": basalEnergyBurned, "ActiveEnergyBurned": activeEnergyBurned}
    with open(filename) as file:
        for line in file:
            data_type = line.split(',')[0]
            if data_type in types.keys():
                types[data_type] = addToDictionary(line, types[data_type])
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
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days[day]


def getAverage(lst):
    return sum(lst) / len(lst)


def addDataToSQL(dates, heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned):
    connector = SQLConnect()
    connector.useDatabase('health')
    connector.createTable('AppleWatch', ['date DATE', 'averageHeartRate FLOAT', 'stepCount FLOAT',
                                         'distanceWalkingRunning FLOAT', 'basalEnergyBurned FLOAT',
                                         'activeEnergyBurned FLOAT', 'dayOfTheWeek varchar(255)'])
    for date in dates:
        connector.insertIntoTable('AppleWatch',
                                  [date, getAverage(heartRate.get(date, [0])), sum(stepCount.get(date, [0.0])),
                                   sum(distanceWalkingRunning.get(date, [0.0])),
                                   sum(basalEnergyBurned.get(date, [0.0])),
                                   sum(activeEnergyBurned.get(date, [0.0])), getDayOfTheWeek(date)])
    connector.commit()


def main():
    heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned = getData('data/appleWatch.csv')
    dates = getAllDates(heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned)
    addDataToSQL(dates, heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned)


if __name__ == "__main__":
    main()
