from SQLConnect import SQLConnect
import hydrateDataLoader
import fitindexDataLoader


def main():
    connector = SQLConnect()
    connector.createDatabase('Health')
    hydrateDataLoader.main()
    fitindexDataLoader.main()
    connector.commit()


if __name__=='__main__':
    main()