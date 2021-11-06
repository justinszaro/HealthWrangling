def openFiles():
    myFitnessPal = open('myFitnessPal.txt', 'w')
    hidrate = open('hidrate.txt', 'w')
    fitindex = open('fitindex.txt', 'w')
    iPhone = open('iPhone.txt', 'w')
    appleWatch = open('appleWatch.txt', 'w')
    return [myFitnessPal, hidrate, fitindex, iPhone, appleWatch]


def getSourceName(line):
    beginning_index = line.index(' ', 17)
    first_quote = line.index('"', beginning_index)
    second_quote = line.index('"', first_quote + 1)
    return line[first_quote + 1:second_quote]


def addLineToFiles(sourceName, line, files):
    myFitnessPal, hidrate, fitindex, iPhone, appleWatch = files
    if sourceName == 'Justin’s Apple\xa0Watch':
        appleWatch.write(line)
    elif sourceName == 'Hidrate':
        hidrate.write(line)
    elif sourceName == 'FITINDEX':
        fitindex.write(line)
    elif sourceName == 'Justin’s iPhone':
        iPhone.write(line)
    elif sourceName == 'Justin’s Apple\xa0Watch':
        appleWatch.write(line)
    elif sourceName == 'MyFitnessPal':
        myFitnessPal.write(line)


def closeFiles(files):
    for file in files:
        file.close()


def main():
    files = openFiles()
    with open('apple_health_export/export.xml') as in_file:
        for line in in_file:
            if line.find('sourceName=') != -1:
                sourceName = getSourceName(line)
                addLineToFiles(sourceName, line, files)
    closeFiles(files)


main()