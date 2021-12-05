from icalendar import Calendar
from SQLConnect import SQLConnect
import os
from datetime import datetime


def insertIntoSQL(data):
    connector = SQLConnect()
    connector.useDatabase('health')
    connector.createTable('Calendar', ['summary VARCHAR(255)', 'days VARCHAR(255)', 'start_time DATETIME',
                                       'end_time DATETIME', 'end_date DATETIME'])
    for event in data:
        if str(event[2]).find(' ') == -1:
            event[2] = str(event[2]) + ' 00:00:00-00:00'
        if str(event[3]).find(' ') == -1:
            event[3] = '9999-01-01 00:00:00+00:00'
        connector.insertIntoTable('Calendar', [event[0], ','.join(event[1]), str(event[2])[:-6], str(event[3])[:-6],
                                               str(event[4][0])[0:-6]])
    connector.commit()


def getDayOfTheWeek(date):
    if len(str(date)) > 19:
        date = str(date)[:-6]
    datetimeObject = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
    day = datetimeObject.weekday()
    days = ['MO', 'TU', 'WE', 'TR', 'FR', 'SA', 'SU']
    return days[day]


def getData(files):
    data = []
    for file in files:
        with open('data/icsFiles/' + file) as infile:
            for component in Calendar.from_ical(infile.read()).walk('vevent'):
                summary = component.get('SUMMARY', "None")
                start_time = component.get('DTSTART').dt
                end_time = component.get('DTEND').dt
                if component.get('RRULE', None) is None:
                    continue
                days = component.get('RRULE').get('BYDAY', [getDayOfTheWeek(start_time)])
                end_date = component.get('RRULE').get('UNTIL', ["9999-01-01 00:00:00+00:00"])
                data.append([str(summary), days, start_time, end_time, end_date])
    return data


def get_filenames(folder):
    filenames = list()
    for root, dirs, files in os.walk(folder):
        filenames = [file for file in files if file.endswith('.ics')]
    return filenames


def main():
    files = get_filenames('data/icsFiles')
    data = getData(files)
    insertIntoSQL(data)
    return data


if __name__ == '__main__':
    main()
