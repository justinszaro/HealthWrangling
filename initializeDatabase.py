from SQLConnect import SQLConnect
import hidrateDataLoader
import fitindexDataLoader
import myFitnessPalDataLoader
import appleWatchDataLoader
import calendarDataLoader


def main():
    connector = SQLConnect()
    connector.createDatabase('health')
    calendarData = calendarDataLoader.main()
    hidrateDataLoader.main(calendarData)
    fitindexDataLoader.main()
    myFitnessPalDataLoader.main()
    appleWatchDataLoader.main()
    connector.commit()


if __name__ == '__main__':
    main()
