import SQLConnect


def getDateAndValue(line):
    components = line.split('" ')
    return [components[6].split('=')[-1].strip('"'), components[-1].split('"')[1]]


def insertIntoDict(date, value, dictionary):
    if date in dictionary.keys():
        dictionary[date] = (dictionary[date] + value / 2).__round__()
    else:
        dictionary[date] = value
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


def addDataToSQL(dates, heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned):
    pass


def main():
    heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned = getData('appleWatch.txt')
    dates = getAllDates(heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned)
    addDataToSQL(dates, heartRate, stepCount, distanceWalkingRunning, basalEnergyBurned, activeEnergyBurned)


if __name__ == "__main__":
    main()
