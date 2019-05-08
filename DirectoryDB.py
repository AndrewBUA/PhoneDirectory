import sqlite3

from PropertySheetImporter import PropertySheetImporter


class Database():

    def __init__(self):
        self.connection = sqlite3.connect("GatewayMGTDB.db")
        self.cursor = self.connection.cursor()

    def createTable(self):
        self.table = """CREATE TABLE IF NOT EXISTS GatewayMGTDB(PROPERTYNAME VARCHAR(100) PRIMARY KEY,
                        REGIONAL VARCHAR(100),
                        MAANAGERNAME VARCHAR(100),
                        ASSISTANTNAME VARCHAR(100),
                        REGION VARCHAR(100),
                        STREETNAME VARCHAR(100),
                        CITY VARCHAR(100),
                        STATE VARCHAR(100),
                        ZIPCODE VARCHAR(100),
                        PHONENUMBER VARCHAR(100),
                        FAXNUMBER VARCHAR(100),
                        RVP VARCHAR(100),
                        EMAIL VARCHAR(100))"""
        self.cursor.execute(self.table)
        self.connection.commit()
        return


    def checkDuplicate(self, PropInfo):
        #PropInfo is a list
        query = "SELECT count(*) FROM GatewayMGTDB WHERE PROPERTYNAME = ?"
        self.cursor.execute(query, (PropInfo["PROPERTYNAME"],))
        data = self.cursor.fetchone()[0]
        if data >= 1:
            return True
        return False

    def insertRecord(self, PropInfo):
        #PropInfo is a list
        if(self.checkDuplicate(PropInfo) == False):
            sql = """ INSERT INTO GatewayMGTDB (PROPERTYNAME, REGIONAL, MAANAGERNAME, ASSISTANTNAME, STREETNAME, CITY, STATE,
            ZIPCODE, PHONENUMBER, FAXNUMBER, EMAIL, REGION, RVP) VALUES ( ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(sql, (PropInfo['PROPERTYNAME'], PropInfo['REGIONAL'], PropInfo['MANAGERNAME'], PropInfo['ASSISTANTNAME'],
                                      PropInfo['STREETNAME'], PropInfo['CITY'], PropInfo['STATE'], PropInfo['ZIPCODE'], PropInfo['PHONENUMBER'],
                                      PropInfo['FAXNUMBER'], PropInfo['EMAIL'], PropInfo['REGION'], PropInfo['RVP']))
            self.connection.commit()
        return

    def allRecords(self):
        query = "SELECT * FROM GatewayMGTDB"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def closeConnection(self):
        self.connection.close()
        return

    def updateRecord(self, propertyName, columnName, update):
        query = "UPDATE GatewayMGTDB SET {} = ? WHERE PROPERTYNAME = ?".format(columnName)
        self.cursor.execute(query, (update, propertyName,))
        self.connection.commit()
        return


    def deleteRecord(self, propertyName):
        self.cursor.execute("DELETE FROM GatewayMGTDB WHERE PROPERTYNAME = ?", (propertyName,))
        self.connection.commit()
        return

    def selectRecord(self, propertyName, columnName):
        #Returns the record that matches the propertyName
        propertyName = "%" + propertyName + "%"
        record = self.cursor.execute("SELECT {} FROM GatewayMGTDB WHERE PROPERTYNAME LIKE ?".format(columnName), (propertyName,))
        self.connection.commit()
        return record.fetchone()

    def selectRecords(self, propertyName, columnName):
        #Returns the record that matches the propertyName
        propertyName = "%" + propertyName + "%"
        record = self.cursor.execute("SELECT {} FROM GatewayMGTDB WHERE PROPERTYNAME LIKE ?".format(columnName), (propertyName,))
        self.connection.commit()
        return record.fetchall()

    def convertTupleToDict(self, tuple):
        PropInfo = {}
        PropInfo['PROPERTYNAME'] = tuple[0].replace("'", "")
        PropInfo['REGIONAL']= tuple[1].replace("'", "")
        PropInfo['MANAGERNAME'] = tuple[2].replace("'", "")
        PropInfo['ASSISTANTNAME'] = tuple[3].replace("'", "")
        PropInfo['REGION'] = tuple[4].replace("'", "")
        PropInfo['STREETNAME'] = tuple[5].replace("'", "")
        PropInfo['CITY'] = tuple[6].replace("'", "")
        PropInfo['STATE'] = tuple[7].replace("'", "")
        PropInfo['ZIPCODE'] = tuple[8].replace("'", "")
        PropInfo['PHONENUMBER'] = tuple[9].replace("'", "")
        PropInfo['FAXNUMBER'] = tuple[10].replace("'", "")
        PropInfo['RVP'] = tuple[11].replace("'", "")
        PropInfo['EMAIL'] = tuple[12].replace("'", "")
        return PropInfo





def main():

    DirectoryTable = Database()
    DirectoryTable.createTable()
    propSheet = PropertySheetImporter()
    propSheet.importFile('Regional Prop List - East.csv', "east")
    for propDic in propSheet.properties():
        DirectoryTable.insertRecord(propDic)

    print(DirectoryTable.selectRecords('Ha', "*"))


    DirectoryTable.closeConnection()


if __name__ == '__main__':
    main()