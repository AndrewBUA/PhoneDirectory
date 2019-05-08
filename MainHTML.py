from flask import Flask, render_template, request
from DirectoryDB import Database
from PropertySheetImporter import PropertySheetImporter

app = Flask(__name__)


def makeDB():
    DirectoryTable = Database()
    DirectoryTable.createTable()
    propSheet = PropertySheetImporter()
    propSheet.importFile('Regional Prop List - East.csv', "east")
    for propDic in propSheet.properties():
        DirectoryTable.insertRecord(propDic)
    return DirectoryTable


@app.route('/', methods = ['POST', 'GET'])
def homepage():
    DirectoryTable = makeDB()
    return render_template("Directory.html", DirectoryTable = DirectoryTable.allRecords())

@app.route('/PropertySearch', methods=['POST', 'GET'])
def handle_data():
    projectpath = request.form['searchProperty']
    DirectoryTable = Database()
    DirectoryTable.createTable()
    data = DirectoryTable.selectRecords(projectpath, "*")
    return render_template("Directory.html", DirectoryTable = data)

if __name__ == "__main__":
    app.run()