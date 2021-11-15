import unittest

import fitindexDataLoader


def getTestStrings():
    test_string = 'type="HKQuantityTypeIdentifierBodyMassIndex" sourceName="FITINDEX" sourceVersion="1" ' \
                  'unit="count" creationDate="2020-01-18 13:36:20 -0400" startDate="2019-01-22 07:42:28 -0400" ' \
                  'endDate="2019-01-22 07:42:28 -0400" value="26.8"/>'
    test_string1 = 'type="HKQuantityTypeIdentifierBodyFatPercentage" sourceName="FITINDEX" sourceVersion="2" ' \
                   'unit="%" creationDate="2021-07-10 04:32:01 -0400" startDate="2021-07-10 04:32:01 -0400" ' \
                   'endDate="2021-07-10 04:32:01 -0400" value="0.1507"/>'
    return test_string, test_string1


class MyTestCase(unittest.TestCase):

    def testGetDataType(self):
        test_string, test_string1 = getTestStrings()
        self.assertEqual('BodyMassIndex', fitindexDataLoader.getDataType(test_string))
        self.assertEqual('BodyFatPercentage', fitindexDataLoader.getDataType(test_string1))

    def testGetDateAndValue(self):
        test_string, test_string1 = getTestStrings()
        self.assertEqual(['2019-01-22', '26.8'], fitindexDataLoader.getDateAndValue(test_string))
        self.assertEqual(['2021-07-10', '0.1507'], fitindexDataLoader.getDateAndValue(test_string1))

    def testCollectedAllDates(self):
        dates = set()
        with open('../fitindex.txt') as in_file:
            for line in in_file:
                components = line.split()
                date = components[7].split('=')[1].strip('"')
                dates.add(date)
        bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned = fitindexDataLoader.getData('../fitindex.txt')
        self.assertEquals(len(dates), len(fitindexDataLoader.getAllDates(bodyMassIndex, bodyMass, bodyFatPercentage, leanBodyMass, basalEnergyBurned)))





if __name__ == '__main__':
    unittest.main()
