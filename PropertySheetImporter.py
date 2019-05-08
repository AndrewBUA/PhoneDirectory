# Import Data
'''

Property Sheet importer. Takes the data from
the property sheet and inputs it into the
directory

'''

import csv

class PropertySheetImporter():

    def __init__(self):
        self.propertyList = []
        self.propertyDictionary = {}

    def removeLeadAndTrailSpaces(self, token):
        cleanTokenList = token.split(" ")
        cleanToken = ""
        for token in cleanTokenList:
            if token != "":
                cleanToken += token + " "
        cleanToken = cleanToken[:-1] #remove trailing space
        return cleanToken

    def importFile(self, filename, region):
        with open(filename) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            regional = ""
            RVP = ""
            for row in csv_reader:
                if row[3].lower() == 'total units':
                    break
                elif 'rpm' in row[3].lower() or 'area' in row[3].lower():
                    regionalList = row[3].split("-")
                    regional = regionalList[0]
                    regional = self.removeLeadAndTrailSpaces(regional)
                elif 'regional vice president' in row[3].lower():
                    RVPList = row[3].split("-")
                    RVP = RVPList[-1]
                    RVP = self.removeLeadAndTrailSpaces(RVP)
                elif row[3] != '':
                    self.propertyDictionary["REGIONAL"] = regional
                    self.propertyDictionary["RVP"] = RVP
                    self.propertyDictionary["PROPERTYNAME"] = row[3]
                    self.propertyDictionary["REGION"] = region
                    self.propertyDictionary["TYPE"] = row[2]
                    self.propertyDictionary["UNITS"] = row[4]
                    self.propertyDictionary["MANAGERNAME"] = row[5]
                    self.propertyDictionary["ASSISTANTNAME"] = row[6]
                    self.propertyDictionary["STREETNAME"] = row[7]
                    self.propertyDictionary["CITY"] = row[8]
                    self.propertyDictionary["STATE"] = row[9]
                    self.propertyDictionary["ZIPCODE"] = row[10]
                    self.propertyDictionary["PHONENUMBER"] = row[11]
                    self.propertyDictionary["FAXNUMBER"] = row[12]
                    self.propertyDictionary["EMAIL"] = row[17]
                    self.propertyList.append(self.propertyDictionary)
                    self.propertyDictionary = {}
            csv_file.close()

    def properties(self):
        self.propertyList = sorted(self.propertyList, key=lambda k: k['PROPERTYNAME'])
        return self.propertyList


def main():

    eastSheet = PropertySheetImporter()
    eastSheet.importFile('Regional Prop List - East.csv', "east")
    for dic in eastSheet.properties():
        print(dic)


if __name__ == '__main__':
    main()
