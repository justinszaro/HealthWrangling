from SQLConnect import SQLConnect
import hidrateDataLoader
import fitindexDataLoader
import myFitnessPalDataLoader
import appleWatchDataLoader
import hydrationLocation


def main():
    connector = SQLConnect()
    connector.createDatabase('health')
    hidrateDataLoader.main()
    fitindexDataLoader.main()
    myFitnessPalDataLoader.main()
    appleWatchDataLoader.main()
    hydrationLocation.main()
    connector.commit()


if __name__ == '__main__':
    main()
