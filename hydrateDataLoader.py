from SQLConnect import SQLConnect


def convertToFlOz(value):
    return (float(value) * 0.033814).__round__(2)


def toOutputFile(outfile, line):
    components = line.split()
    date = components[7][11:]
    time = components[8]
    value = components[13][6:].strip('"/>')
    outfile.write(','.join([date, time, str(convertToFlOz(value))]) + '\n')


def insertIntoDict(dictionary, date, value):
    if dictionary.get(date, None) is None:
        dictionary[date] = value.__round__(2)
    else:
        dictionary[date] = (dictionary[date] + value).__round__(2)
    return dictionary


def getData(filename):
    hydrateData = dict()
    outfile = open('data/HydrateDataPoints.csv', 'w')
    with open(filename) as in_file:
        for line in in_file:
            components = line.split()
            date = components[7][11:]
            value = components[13][6:].strip('"/>')
            hydrateData = insertIntoDict(hydrateData, date, convertToFlOz(value))
            toOutputFile(outfile, line)
    outfile.close()
    return hydrateData


def toSQL(data):
    connector = SQLConnect()
    connector.useDatabase('health')
    connector.create_table('Hidrate', ['date CHAR(10), amount FLOAT'])
    for key in data.keys():
        connector.insert_into_table('Hidrate', [key, str(data[key])])
    connector.commit()


def main():
    hydrateData = getData('data/hidrate.txt')
    toSQL(hydrateData)


if __name__ == '__main__':
    main()
