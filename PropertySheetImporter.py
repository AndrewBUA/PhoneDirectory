# PropertySheetImporter.py
import csv


class PropertySheetImporter():

    def __init__(self):
        self.propertyList = []

    def removeLeadAndTrailSpaces(self, token):
        """Cleans up whitespace from a string token."""
        return " ".join(token.split())

    def importFile(self, filename, region):
        """Imports property data from a given CSV file and region."""
        try:
            with open(filename, encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")
                regional = ""
                RVP = ""
                for row in csv_reader:
                    # Skip empty rows or rows that don't have enough columns
                    if not row or len(row) < 18:
                        continue
                    if row[3].lower() == 'total units':
                        break
                    elif 'rpm' in row[3].lower() or 'area' in row[3].lower():
                        regionalList = row[3].split("-")
                        regional = self.removeLeadAndTrailSpaces(regionalList[0])
                    elif 'regional vice president' in row[3].lower():
                        RVPList = row[3].split("-")
                        RVP = self.removeLeadAndTrailSpaces(RVPList[-1])
                    elif row[3] != '':
                        propertyDictionary = {}
                        propertyDictionary["REGIONAL"] = regional
                        propertyDictionary["RVP"] = RVP
                        propertyDictionary["PROPERTYNAME"] = row[3]
                        propertyDictionary["REGION"] = region
                        propertyDictionary["TYPE"] = row[2]
                        propertyDictionary["UNITS"] = row[4]
                        propertyDictionary["MANAGERNAME"] = row[5]
                        propertyDictionary["ASSISTANTNAME"] = row[6]
                        propertyDictionary["STREETNAME"] = row[7]
                        propertyDictionary["CITY"] = row[8]
                        propertyDictionary["STATE"] = row[9]
                        propertyDictionary["ZIPCODE"] = row[10]
                        propertyDictionary["PHONENUMBER"] = row[11]
                        propertyDictionary["FAXNUMBER"] = row[12]
                        propertyDictionary["EMAIL"] = row[17]
                        self.propertyList.append(propertyDictionary)
        except FileNotFoundError:
            print(f"Error: The file '{filename}' was not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def properties(self):
        """Returns the final list of properties, sorted by name."""
        return sorted(self.propertyList, key=lambda k: k['PROPERTYNAME'])