def convertToFlOz(value):
    return float(value) * 0.033814


def insertIntoDict(dictionary, date, value):
    if dictionary.get(date, None) is None:
        dictionary[date] = value
    else:
        dictionary[date] += value
    dictionary[date] = dictionary[date].__round__(2)
    return dictionary


def getData(filename):
    hydrateData = dict()
    with open(filename) as in_file:
        for line in in_file:
            components = line.split()
            date = components[7][11:]
            value = components[13][6:].strip('"/>')
            hydrateData = insertIntoDict(hydrateData, date, convertToFlOz(value))
    return hydrateData


def main():
    hydrateData = getData('data/hidrate.txt')


if __name__ == '__main__':
    main()
