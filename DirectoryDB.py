# DirectoryDB.py
import sqlite3
import re

# --- Security: Whitelist of valid column names to prevent SQL injection ---
VALID_COLUMNS = {
    "PROPERTYNAME", "REGIONAL", "MANAGERNAME", "ASSISTANTNAME", "REGION",
    "STREETNAME", "CITY", "STATE", "ZIPCODE", "PHONENUMBER", "FAXNUMBER",
    "RVP", "EMAIL"
}


def get_db_connection():
    """Establishes and returns a connection to the database."""
    conn = sqlite3.connect("GatewayMGTDB.db")
    # This allows you to access columns by name
    conn.row_factory = sqlite3.Row
    return conn


def create_table(conn):
    """Creates the database table if it doesn't already exist."""
    table_sql = """CREATE TABLE IF NOT EXISTS GatewayMGTDB(
                    PROPERTYNAME VARCHAR(100) PRIMARY KEY,
                    REGIONAL VARCHAR(100),
                    MANAGERNAME VARCHAR(100),
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
    conn.execute(table_sql)
    conn.commit()


def check_duplicate(conn, prop_name):
    """Checks if a property name already exists in the database."""
    query = "SELECT count(*) FROM GatewayMGTDB WHERE PROPERTYNAME = ?"
    cursor = conn.cursor()
    cursor.execute(query, (prop_name,))
    data = cursor.fetchone()[0]
    return data >= 1


def insert_record(conn, prop_info):
    """Inserts a new property record if it's not a duplicate."""
    if not check_duplicate(conn, prop_info["PROPERTYNAME"]):
        sql = """INSERT INTO GatewayMGTDB (PROPERTYNAME, REGIONAL, MANAGERNAME, ASSISTANTNAME, STREETNAME, CITY, STATE,
                 ZIPCODE, PHONENUMBER, FAXNUMBER, EMAIL, REGION, RVP)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
        # Using .get() provides a safe default (None) if a key is missing
        conn.execute(sql, (
            prop_info.get('PROPERTYNAME'), prop_info.get('REGIONAL'), prop_info.get('MANAGERNAME'),
            prop_info.get('ASSISTANTNAME'), prop_info.get('STREETNAME'), prop_info.get('CITY'),
            prop_info.get('STATE'), prop_info.get('ZIPCODE'), prop_info.get('PHONENUMBER'),
            prop_info.get('FAXNUMBER'), prop_info.get('EMAIL'), prop_info.get('REGION'),
            prop_info.get('RVP')
        ))
        conn.commit()


def all_records(conn):
    """Retrieves all records from the database, ordered by name."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM GatewayMGTDB ORDER BY PROPERTYNAME ASC")
    return cursor.fetchall()


def select_records(conn, search_criteria):
    """
    Dynamically builds a secure SQL query based on a dictionary of search criteria.
    - search_criteria: A dictionary like {'STATE': 'AL', 'PROPERTYNAME': 'Park'}
    """
    base_query = "SELECT * FROM GatewayMGTDB"
    where_clauses = []
    values = []

    # Validate and build WHERE clauses for each search criterion
    for key, value in search_criteria.items():
        # CRITICAL SECURITY STEP: Ensure the key is a valid column name
        safe_key = re.sub(r'[^a-zA-Z0-9_]', '', key.upper())

        if safe_key in VALID_COLUMNS:
            where_clauses.append(f"{safe_key} LIKE ?")
            values.append(f"%{value}%")

    # If we have valid clauses, add them to the query
    if where_clauses:
        base_query += " WHERE " + " AND ".join(where_clauses)

    base_query += " ORDER BY PROPERTYNAME ASC"

    cursor = conn.cursor()
    cursor.execute(base_query, tuple(values))
    return cursor.fetchall()