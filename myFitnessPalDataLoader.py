from SQLConnect import SQLConnect
from datetime import datetime


def insertIntoDict(line, dictionary):
    data_type, date, value = line.strip().split(',')
    date, time = date.split()
    if date in dictionary.keys() and data_type != 'bodyMass':
        dictionary[date] = (float(dictionary[date]) + float(value))
    elif date in dictionary.keys() and data_type == 'bodyMass':
        dictionary[date] = (float(dictionary[date]) + float(value)) / 2
    else:
        dictionary[date] = float(value)
    return dictionary


def getData(filename):
    bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated, dietaryFatSaturated, \
        dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber, dietarySugar, dietaryEnergyConsumed, \
        dietaryProtein, dietaryVitaminC, dietaryCalcium, dietaryIron, dietaryPotassium = [
            dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(), dict(),
            dict(), dict(), dict()]
    types = {"BodyMass": bodyMass, "DietaryFatTotal": dietaryFatTotal,
             "DietaryFatPolyunsaturated": dietaryFatPolyunsaturated,
             "DietaryFatMonounsaturated": dietaryFatMonounsaturated,
             "DietaryFatSaturated": dietaryFatSaturated, "DietaryCholesterol": dietaryCholesterol,
             "DietarySodium": dietarySodium, "DietaryCarbohydrates": dietaryCarbohydrates, "DietaryFiber": dietaryFiber,
             "DietarySugar": dietarySugar, "DietaryEnergyConsumed": dietaryEnergyConsumed,
             "DietaryProtein": dietaryProtein, "DietaryVitaminC": dietaryVitaminC, "DietaryCalcium": dietaryCalcium,
             "DietaryIron": dietaryIron, "DietaryPotassium": dietaryPotassium}
    with open(filename) as file:
        for line in file:
            data_type = line.split(',')[0]
            if data_type in types.keys():
                types[data_type] = insertIntoDict(line, types[data_type])
    return [bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated, dietaryFatSaturated,
            dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber, dietarySugar, dietaryEnergyConsumed,
            dietaryProtein, dietaryVitaminC, dietaryCalcium, dietaryIron, dietaryPotassium]


def getAllDates(lstOfDict):
    dates = set()
    for dct in lstOfDict:
        dates = dates.union(set(dct.keys()))
    return dates


def getDayOfTheWeek(date):
    datetimeObject = datetime.strptime(date, '%Y-%m-%d')
    day = datetimeObject.weekday()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    return days[day]


def addDataToSQL(dates, bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated,
                 dietaryFatSaturated, dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber,
                 dietarySugar, dietaryEnergyConsumed, dietaryProtein, dietaryVitaminC, dietaryCalcium, dietaryIron,
                 dietaryPotassium):
    connector = SQLConnect()
    connector.useDatabase('health')
    connector.createTable('MyFitnessPal', ['date CHAR(10), bodyMass FLOAT, dietaryFatTotal FLOAT, '
                                           'dietaryFatPolyunsaturated FLOAT, dietaryFatMonounsaturated FLOAT, '
                                           'dietaryFatSaturated FLOAT, dietaryCholesterol FLOAT, dietarySodium '
                                           'FLOAT, dietaryCarbohydrates FLOAT, dietaryFiber FLOAT, dietarySugar '
                                           'FLOAT, dietaryEnergyConsumed FLOAT, dietaryProtein FLOAT, '
                                           'dietaryVitaminC FLOAT, dietaryCalcium FLOAT, dietaryIron FLOAT, '
                                           'dietaryPotassium FLOAT, dayOfTheWeek varchar(255)'])
    for date in dates:
        connector.insertIntoTable('MyFitnessPal', [date, bodyMass.get(date, 0.0), dietaryFatTotal.get(date, 0.0),
                                                   dietaryFatPolyunsaturated.get(date, 0.0),
                                                   dietaryFatMonounsaturated.get(date, 0.0),
                                                   dietaryFatSaturated.get(date, 0.0),
                                                   dietaryCholesterol.get(date, 0.0),
                                                   dietarySodium.get(date, 0.0),
                                                   dietaryCarbohydrates.get(date, 0.0),
                                                   dietaryFiber.get(date, 0.0), dietarySugar.get(date, 0.0),
                                                   dietaryEnergyConsumed.get(date, 0.0),
                                                   dietaryProtein.get(date, 0.0),
                                                   dietaryVitaminC.get(date, 0.0), dietaryCalcium.get(date, 0.0),
                                                   dietaryIron.get(date, 0.0), dietaryPotassium.get(date, 0.0),
                                                   getDayOfTheWeek(date)])
    connector.commit()


def main():
    bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated, dietaryFatSaturated, \
        dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber, dietarySugar, dietaryEnergyConsumed, \
        dietaryProtein, dietaryVitaminC, dietaryCalcium, dietaryIron, dietaryPotassium = getData(
            'data/myFitnessPal.csv')
    dates = getAllDates([bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated,
                        dietaryFatSaturated, dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber,
                        dietarySugar, dietaryEnergyConsumed, dietaryProtein, dietaryVitaminC, dietaryCalcium,
                        dietaryIron, dietaryPotassium])
    addDataToSQL(dates, bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated,
                 dietaryFatSaturated, dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber,
                 dietarySugar, dietaryEnergyConsumed, dietaryProtein, dietaryVitaminC, dietaryCalcium, dietaryIron,
                 dietaryPotassium)


if __name__ == "__main__":
    main()
