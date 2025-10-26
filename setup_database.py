# setup_database.py
# Run this script ONCE from your terminal to create and populate your database.
# Do NOT call this from your Flask application.

import DirectoryDB as db
from PropertySheetImporter import PropertySheetImporter

def setup():
    """
    Initializes the database, creates the table, and loads data from the CSV.
    """
    print("--- Setting up the database ---")

    # Connect to the database
    conn = db.get_db_connection()

    try:
        # Create the table
        print("Creating table if it doesn't exist...")
        db.create_table(conn)

        # Import data from the CSV file
        print("Importing data from Property_List_CSV.csv...")
        prop_sheet = PropertySheetImporter()
        prop_sheet.import_file('Property_List_CSV.csv', "east")

        # Insert each record into the database
        record_count = 0
        for prop_dic in prop_sheet.properties():
            db.insert_record(conn, prop_dic)
            record_count += 1

        print(f"Successfully inserted {record_count} records.")

    except Exception as e:
        print(f"An error occurred during database setup: {e}")
    finally:
        # Ensure the connection is always closed
        if conn:
            conn.close()
        print("--- Database setup complete! ---")

if __name__ == '__main__':
    setup()