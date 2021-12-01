from SQLConnect import SQLConnect


def getDateAndValue(line):
    components = line.split()
    return [components[7].split('=')[1].strip('"'), components[-1][7:len(components[-1])-2].strip('"')]


def insertIntoDict(line, dict):
    date, value = getDateAndValue(line)
    if date in dict.keys():
        dict[date] = str(((float(dict[date]) + float(value)) / 2))
    else:
        dict[date] = str(value)
    return dict


def getDataType(line):
    return line.split()[0][30:].strip('"')


def getData(filename):
    bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned = [dict(), dict(), dict(), dict(), dict()]
    with open(filename) as in_file:
        for line in in_file:
            data_type = getDataType(line)
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
    return dates.union(bodyMassIndex.keys(), bodyMass.keys(), bodyFatPercentage.keys(), leanBodyMass.keys(), basalEnergyBurned.keys())


def addDataToSQL(dates, bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned):
    connector = SQLConnect()
    connector.useDatabase('health')
    connector.create_table('Fitindex', ['date DATE', 'bodyMassIndex FLOAT', 'bodyMass FLOAT', 'bodyFatPercentage FLOAT',
                                        'leanBodyMass FLOAT', 'basalEnergyBurned FLOAT'])
    for date in dates:
        connector.insert_into_table('fitindex', [date, bodyMassIndex.get(date, '0.0'), bodyMass.get(date, '0.0'),
                                                 bodyFatPercentage.get(date, '0.0'), leanBodyMass.get(date, '0.0'),
                                                 basalEnergyBurned.get(date, '0.0')])
    connector.commit()


def main():
    bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned = getData('fitindex.txt')
    dates = getAllDates(bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned)
    addDataToSQL(dates, bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned)


if __name__=='__main__':
    main()