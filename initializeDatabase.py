from SQLConnect import SQLConnect
import hydrateDataLoader
import fitindexDataLoader
import myFitnessPalDataLoader
import appleWatchDataLoader
import calendarDataLoader


def main():
    connector = SQLConnect()
    connector.createDatabase('health')
    hydrateDataLoader.main()
    fitindexDataLoader.main()
    myFitnessPalDataLoader.main()
    appleWatchDataLoader.main()
    calendarDataLoader.main()
    connector.commit()


if __name__ == '__main__':
    main()
