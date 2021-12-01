from SQLConnect import SQLConnect
import hydrateDataLoader
import fitindexDataLoader
import myFitnessPalDataLoader
import appleWatchDataLoader


def main():
    connector = SQLConnect()
    connector.createDatabase('health')
    hydrateDataLoader.main()
    fitindexDataLoader.main()
    myFitnessPalDataLoader.main()
    appleWatchDataLoader.main()
    connector.commit()


if __name__ == '__main__':
    main()
