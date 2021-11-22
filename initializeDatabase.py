from SQLConnect import SQLConnect
import hydrateDataLoader


def main():
    connector = SQLConnect()
    connector.createDatabase('Health')
    hydrateDataLoader.main()
    connector.commit()


if __name__=='__main__':
    main()