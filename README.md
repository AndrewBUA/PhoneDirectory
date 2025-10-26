# Phone Directory Web Application

This project is a simple, searchable phone directory web application built with Python and Flask. It allows users to view, search, and get details for various properties listed in a directory. The application features a live search function that dynamically updates the displayed results as the user types.
## Features

  Live Search: The application implements a real-time search that filters properties by name or other attributes as the user types into the search bar.

  Dynamic Content Loading: Search results are fetched asynchronously using AJAX, providing a smooth and responsive user experience without needing to reload the page.

  Advanced Search Syntax: Users can perform targeted searches using a column:value syntax (e.g., State:AL or Regional:"John Doe") to filter by specific fields.

  Modal for Detailed View: Clicking on a property name opens a modal dialog that displays more detailed information about the property, such as manager and assistant names, and full address.

  Database Backend: The application uses SQLite to store and manage the property data, with a clear separation of database logic from the web application.

  CSV Data Import: A setup script is provided to easily populate the database from a CSV file.

## Screenshots

Here’s a look at the application in action:

Main Directory View:

<img width="2084" height="1358" alt="Untitled" src="https://github.com/user-attachments/assets/193d68db-86f8-4c96-9009-88bcac451142" />


Live Search Functionality:

<img width="1914" height="377" alt="Untitled" src="https://github.com/user-attachments/assets/a3fa2c13-320b-4e34-ad20-91408ffee697" />


Detailed Property View (Modal):

<img width="2198" height="1024" alt="image" src="https://github.com/user-attachments/assets/205013f1-2d42-449c-a779-9460b3fb8a23" />



## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

Make sure you have the following installed:

    Python 3.x
    Flask
    sqlite3

You can install Flask/sqlite3 using pip:

    <>Bash
    pip install Flask
    pip install sqlite3

  

## Installation

Clone the repository:
    
    <>Bash
    git clone https://github.com/your-username/your-repo-name.git
    cd your-repo-name

  

Prepare your data file:
Make sure you have your property data in a CSV file named Property_List_CSV.csv in the root directory of the project.

Set up the database:
Run the setup_database.py script once to create the GatewayMGTDB.db file and populate it with data from your CSV.

    <>Bash    
    python setup_database.py


This will create the SQLite database and import all the records.

## Usage

After setting up the database, you can start the Flask application by running:

    <>Bash
    python MainHTML.py
  

The application will be accessible at http://127.0.0.1:5000 in your web browser.

## Project Structure

The project is organized into the following files:

    MainHTML.py: The main Flask application file. It handles routing, database connections, and rendering the HTML template.

    DirectoryDB.py: Contains all the functions for interacting with the SQLite database, including creating tables, inserting records, and querying data.

    setup_database.py: A utility script to initialize the database and import data from the CSV file. This should only be run once.

    PropertySheetImporter.py: A class that handles the logic for reading and parsing the Property_List_CSV.csv file.

    templates/Directory.html: The HTML template for the main page, which includes the search bar, property table, and modal structure. It uses Jinja2 for templating.

    static/: This directory contains static assets like CSS files, images, and the favicon.ico.

    .gitignore: Specifies files and directories that should be ignored by Git, such as the database file and the source CSV.

## .gitignore

The .gitignore file is configured to exclude the following files from the repository:

### Code
    
    # Ignore the db
    GatewayMGTDB.db

    # Ignore the Property List CSV
    Property_List_CSV.csv

This is done to:

Avoid versioning data: The database file (.db) changes every time data is added or modified, and it's generally not recommended to version control databases.

Keep sensitive or large data private: The Property_List_CSV.csv might contain private information or be very large, so it's best to keep it out of the repository. Users of the project are expected to provide their own CSV file.
