import SQLConnect


def getDateAndValue(line):
    components = line.split()
    return [components[7].split('=')[1].strip('"'), components[-1][7:len(components[-1]) - 2].strip('"')]


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


def addDataToSQL(dates, bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated, dietaryFatSaturated, dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber, dietarySugar, dietaryEnergyConsumed, dietaryProtein, dietaryVitaminC, dietaryCalcium, dietaryIron, dietaryPotassium):
    pass


def main():
    bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated, dietaryFatSaturated, dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber, dietarySugar, dietaryEnergyConsumed, dietaryProtein, dietaryVitaminC, dietaryCalcium, dietaryIron, dietaryPotassium = getData('myFitnessPal.txt')
    dates = getAllDates(bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated, dietaryFatSaturated, dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber, dietarySugar, dietaryEnergyConsumed, dietaryProtein, dietaryVitaminC, dietaryCalcium, dietaryIron, dietaryPotassium)
    addDataToSQL(dates, bodyMass, dietaryFatTotal, dietaryFatPolyunsaturated, dietaryFatMonounsaturated, dietaryFatSaturated, dietaryCholesterol, dietarySodium, dietaryCarbohydrates, dietaryFiber, dietarySugar, dietaryEnergyConsumed, dietaryProtein, dietaryVitaminC, dietaryCalcium, dietaryIron, dietaryPotassium)


if __name__ == "__main__":
    main()
