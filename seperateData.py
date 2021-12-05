def openFiles():
    myFitnessPal = open('data/myFitnessPal.csv', 'w')
    hidrate = open('data/hidrate.csv', 'w')
    fitindex = open('data/fitindex.csv', 'w')
    appleWatch = open('data/appleWatch.csv', 'w')
    return [myFitnessPal, hidrate, fitindex, appleWatch]


def getSourceName(line):
    beginning_index = line.index(' ', 17)
    first_quote = line.index('"', beginning_index)
    second_quote = line.index('"', first_quote + 1)
    return line[first_quote + 1:second_quote]


def writeLine(line, file):
    components = line.split()
    label = components[0][30:len(components[0]) - 1]
    start_datetime = components[-4][9:] + ' ' + components[-3]
    value = components[-1][7:].strip('"/>')
    file.write(','.join([label, start_datetime, value]) + '\n')


def addLineToFiles(sourceName, line, files):
    myFitnessPal, hidrate, fitindex, appleWatch = files
    if sourceName == 'Justin’s Apple\xa0Watch':
        writeLine(line, appleWatch)
    elif sourceName == 'Hidrate':
        writeLine(line, hidrate)
    elif sourceName == 'FITINDEX':
        writeLine(line, fitindex)
    elif sourceName == 'MyFitnessPal':
        writeLine(line, myFitnessPal)


def closeFiles(files):
    for file in files:
        file.close()


def main():
    files = openFiles()
    with open('data/export.xml') as in_file:
        for line in in_file:
            if line.find('sourceName=') != -1:
                sourceName = getSourceName(line)
                addLineToFiles(sourceName, line[9:], files)
    closeFiles(files)


main()
