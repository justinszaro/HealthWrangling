import SQLConnect

def getDateAndValue(line):
    components = line.split()
    return [components[7].split('=')[1].strip('"'), components[-1][7:len(components[-1])-2].strip('"')]


def insertIntoDict(date, value, dict):
    if date in dict.keys():
        dict[date] = (dict[date] + value / 2).__round__()
    else:
        dict[date] = value
    return dict


def addToDictionary(line, dictionary):
    date, value = getDateAndValue(line)
    dictionary = insertIntoDict(date, float(value), dictionary)
    return dictionary


def getDataType(line):
    return line.split()[0][30:].strip('"')


def getData(filename):
    bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned = [dict(), dict(), dict(), dict(), dict()]
    with open(filename) as in_file:
        for line in in_file:
            data_type = getDataType(line)
            if data_type == "BodyMassIndex":
                bodyMassIndex = addToDictionary(line, bodyMassIndex)
            elif data_type == "BodyMass":
                bodyMass = addToDictionary(line, bodyMass)
            elif data_type == "BodyFatPercentage":
                bodyFatPercentage = addToDictionary(line, bodyFatPercentage)
            elif data_type == 'LeanBodyMass':
                leanBodyMass = addToDictionary(line, leanBodyMass)
            elif data_type == 'BasalEnergyBurned':
                basalEnergyBurned = addToDictionary(line, basalEnergyBurned)
    return [bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned]


def getAllDates(bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned):
    dates = set()
    return dates.union(bodyMassIndex.keys(), bodyMass.keys(), bodyFatPercentage.keys(), leanBodyMass.keys(), basalEnergyBurned.keys())


def addDataToSQL(dates, bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned):
    pass


def main():
    bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned = getData('fitindex.txt')
    dates = getAllDates(bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned)
    addDataToSQL(dates, bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned)
if __name__=='__main__':
    main()