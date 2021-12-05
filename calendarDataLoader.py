from icalendar import Calendar
from SQLConnect import SQLConnect
import os
from datetime import datetime

def insertIntoSQL(data):
    connector = SQLConnect()
    connector.useDatabase('health')
    connector.query('Drop table if exists Calendar')
    connector.create_table('Calendar',['summary VARCHAR(255)', 'days VARCHAR(255)', 'start_time DATETIME',
                                       'end_time DATETIME', 'end_date DATETIME'])
    for event in data:
        if str(event[2]).find(' ') == -1:
            event[2] = str(event[2]) + ' 00:00:00-00:00'
        if str(event[3]).find(' ') == -1:
            event[3] = '9999-01-01 00:00:00+00:00'
        connector.insert_into_table('Calendar', [event[0], ','.join(event[1]), str(event[2])[:-6], str(event[3])[:-6], str(event[4][0])[0:-6]])
    connector.commit()


def getDayOfTheWeek(date):
    if len(str(date)) > 19:
        date = str(date)[:-6]
    datetimeobject = datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S')
    day = datetimeobject.weekday()

    if day == 0:
        return 'MO'
    elif day == 1:
        return 'TU'
    elif day == 2:
        return 'WE'
    elif day == 3:
        return 'TH'
    elif day == 4:
        return 'FR'
    elif day == 5:
        return 'SA'
    elif day == 6:
        return 'SU'


def getData(files):
    data = []
    for file in files:
        with open('data/icsFiles/' + file) as infile:
            for component in Calendar.from_ical(infile.read()).walk('vevent'):
                summary = component.get('SUMMARY', "None")
                start_time = component.get('DTSTART', ["9999-01-01 00:00:00"]).dt
                end_time = component.get('DTEND', "'9999-01-01 00:00:00'").dt
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


if __name__=='__main__':
    main()