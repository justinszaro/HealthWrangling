from SQLConnect import SQLConnect
from datetime import datetime


def getDateAndValue(line):
    components = line.split()
    return [components[7].split('=')[1].strip('"'), components[-1][7:len(components[-1]) - 2].strip('"')]


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
    bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated, dietaryFatSaturated, dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber, dietarySugar, dietaryEnergyConsumed, dietaryProtein, dietaryVitaminC, dietaryCalcium, dietaryIron, dietaryPotassium = [dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict()]
    with open(filename) as file:
        for line in file:
            data_type = getDataType(line)
            if data_type == "BodyMass":
                bodyMass = addToDictionary(line, bodyMass)
            elif data_type == "DietaryFatTotal":
                dietaryFatTotal = addToDictionary(line, dietaryFatTotal)
            elif data_type == "DietaryFatPolyunsaturated":
                dietaryFatPolyunsaturated = addToDictionary(line, dietaryFatPolyunsaturated)
            elif data_type == "DietaryFatMonounsaturated":
                dietaryFatMonounsaturated = addToDictionary(line, dietaryFatMonounsaturated)
            elif data_type == "DietaryFatSaturated":
                dietaryFatSaturated = addToDictionary(line, dietaryFatSaturated)
            elif data_type == "DietaryCholesterol":
                dietaryCholesterol = addToDictionary(line, dietaryCholesterol)
            elif data_type == "DietarySodium":
                dietarySodium = addToDictionary(line, dietarySodium)
            elif data_type == "DietaryCarbohydrates":
                dietaryCarbohydrates = addToDictionary(line, dietaryCarbohydrates)
            elif data_type == "DietaryFiber":
                dietaryFiber = addToDictionary(line, dietaryFiber)
            elif data_type == "DietarySugar":
                dietarySugar = addToDictionary(line, dietarySugar)
            elif data_type == "DietaryEnergyConsumed":
                dietaryEnergyConsumed = addToDictionary(line, dietaryEnergyConsumed)
            elif data_type == "DietaryProtein":
                dietaryProtein = addToDictionary(line, dietaryProtein)
            elif data_type == "DietaryVitaminC":
                dietaryVitaminC = addToDictionary(line, dietaryVitaminC)
            elif data_type == "DietaryCalcium":
                dietaryCalcium = addToDictionary(line, dietaryCalcium)
            elif data_type == "DietaryIron":
                dietaryIron = addToDictionary(line, dietaryIron)
            elif data_type == "DietaryPotassium":
                dietaryPotassium = addToDictionary(line, dietaryPotassium)
    return [bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated, dietaryFatSaturated, dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber, dietarySugar, dietaryEnergyConsumed, dietaryProtein, dietaryVitaminC, dietaryCalcium, dietaryIron, dietaryPotassium]


def getAllDates(bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated, dietaryFatSaturated, dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber, dietarySugar, dietaryEnergyConsumed, dietaryProtein, dietaryVitaminC, dietaryCalcium, dietaryIron, dietaryPotassium):
    dates = set()
    return dates.union(bodyMass.keys(), dietaryFatTotal.keys(), dietaryFatPolyunsaturated.keys(), dietaryFatMonounsaturated.keys(), dietaryFatSaturated.keys(), dietaryCholesterol.keys(), dietarySodium.keys(), dietaryCarbohydrates.keys(), dietaryFiber.keys(), dietarySugar.keys(), dietaryEnergyConsumed.keys(), dietaryProtein.keys(), dietaryVitaminC.keys(), dietaryCalcium.keys(), dietaryIron.keys(), dietaryPotassium.keys())


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


def addDataToSQL(dates, bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated, dietaryFatSaturated, dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber, dietarySugar, dietaryEnergyConsumed, dietaryProtein, dietaryVitaminC, dietaryCalcium, dietaryIron, dietaryPotassium):
    connector = SQLConnect()
    connector.useDatabase('health')
    connector.create_table('MyFitnessPal', ['date CHAR(10), bodyMass FLOAT, dietaryFatTotal FLOAT, '
                                            'dietaryFatPolyunsaturated FLOAT, dietaryFatMonounsaturated FLOAT, '
                                            'dietaryFatSaturated FLOAT, dietaryCholesterol FLOAT, dietarySodium '
                                            'FLOAT, dietaryCarbohydrates FLOAT, dietaryFiber FLOAT, dietarySugar '
                                            'FLOAT, dietaryEnergyConsumed FLOAT, dietaryProtein FLOAT, '
                                            'dietaryVitaminC FLOAT, dietaryCalcium FLOAT, dietaryIron FLOAT, '
                                            'dietaryPotassium FLOAT, dayOfTheWeek varchar(255)'])
    for date in dates:
        connector.insert_into_table('MyFitnessPal', [date, bodyMass.get(date, '0.0'), dietaryFatTotal.get(date, '0.0'),
                                                     dietaryFatPolyunsaturated.get(date, '0.0'),
                                                     dietaryFatMonounsaturated.get(date, '0.0'),
                                                     dietaryFatSaturated.get(date, '0.0'),
                                                     dietaryCholesterol.get(date, '0.0'),
                                                     dietarySodium.get(date, '0.0'),
                                                     dietaryCarbohydrates.get(date, '0.0'),
                                                     dietaryFiber.get(date, '0.0'), dietarySugar.get(date, '0.0'),
                                                     dietaryEnergyConsumed.get(date, '0.0'),
                                                     dietaryProtein.get(date, '0.0'),
                                                     dietaryVitaminC.get(date, '0.0'), dietaryCalcium.get(date, '0.0'),
                                                     dietaryIron.get(date, '0.0'), dietaryPotassium.get(date, '0.0'),
                                                     getDayOfTheWeek(date)])
    connector.commit()


def main():
    bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated, dietaryFatSaturated, dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber, dietarySugar, dietaryEnergyConsumed, dietaryProtein, dietaryVitaminC, dietaryCalcium, dietaryIron, dietaryPotassium = getData('myFitnessPal.txt')
    dates = getAllDates(bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated, dietaryFatSaturated, dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber, dietarySugar, dietaryEnergyConsumed, dietaryProtein, dietaryVitaminC, dietaryCalcium, dietaryIron, dietaryPotassium)
    addDataToSQL(dates, bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated, dietaryFatSaturated, dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber, dietarySugar, dietaryEnergyConsumed, dietaryProtein, dietaryVitaminC, dietaryCalcium, dietaryIron, dietaryPotassium)


if __name__ == "__main__":
    main()
