from SQLConnect import SQLConnect


def getDateAndValue(line):
    components = line.split()
    componentsForDate = line.split('startDate="')
    return [componentsForDate[1].split()[0], components[-1].split('"')[1]]


def insertIntoDict(date, value, dictionary):
    if date in dictionary.keys():
        dictionary[date] = str(((float(dictionary[date]) + float(value)) / 2).__round__())
    else:
        dictionary[date] = str(value)
    return dictionary


def addToDictionary(line, dictionary):
    date, value = getDateAndValue(line)
    dictionary = insertIntoDict(date, float(value), dictionary)
    return dictionary


def getDataType(line):
    return line.split()[0][30:].strip('"')


def getData(filename):
    heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned = [dict(), dict(), dict(), dict(), dict()]
    with open(filename) as file:
        for line in file:
            data_type = getDataType(line)
            if data_type == "HeartRate":
                heartRate = addToDictionary(line, heartRate)
            elif data_type == "StepCount":
                stepCount = addToDictionary(line, stepCount)
            elif data_type == "DistanceWalkingRunning":
                distanceWalkingRunning = addToDictionary(line, distanceWalkingRunning)
            elif data_type == "BasalEnergyBurned":
                basalEnergyBurned = addToDictionary(line, basalEnergyBurned)
            elif data_type == "ActiveEnergyBurned":
                activeEnergyBurned = addToDictionary(line, activeEnergyBurned)
    return [heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned]


def getAllDates(heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned):
    dates = set()
    return dates.union(heartRate.keys(), stepCount.keys(), distanceWalkingRunning.keys(), basalEnergyBurned.keys(), activeEnergyBurned.keys())


def quotes(string):
    return '"' + string + '"'


def addDataToSQL(dates, heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned):
    connector = SQLConnect()
    connector.useDatabase('health')
    connector.create_table('applewatch', ['date DATE', 'heartRate FLOAT', 'stepCount FLOAT', 'distanceWalkingRunning FLOAT',
                                        'basalEnergyBurned FLOAT', 'activeEnergyBurned FLOAT'])
    for date in dates:
        connector.insert_into_table('applewatch',
                                    [date, heartRate.get(date, '0.0'), stepCount.get(date, '0.0'),
                                     distanceWalkingRunning.get(date, '0.0'), basalEnergyBurned.get(date, '0.0'),
                                     activeEnergyBurned.get(date, '0.0')])
    connector.commit()


def main():
    heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned = getData('appleWatch.txt')
    dates = getAllDates(heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned)
    addDataToSQL(dates, heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned)


if __name__ == "__main__":
    main()
