import os
import argparse
import sqlite3

def connect_to_database(db_file):
    """ Connect to an SQLite database and return the connection object """
    try:
        if os.path.exists(db_file):
            # Establish a connection to the SQLite database
            conn = sqlite3.connect(db_file)
            print(f"Successfully connected to {db_file}")
            return conn

        print(f"Database file {db_file} does not exist.")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

    return None

def find_duplicates_by(conn, table_name, column_name, columns="path"):
    cursor = conn.cursor()

    # Dynamically build and execute SQL query to find duplicates based on 'hash' column
    query = f"""
    SELECT {columns}
    FROM {table_name} indx
    JOIN (
        SELECT {column_name}
        FROM {table_name}
        GROUP BY {column_name}
        HAVING COUNT(*) > 1
    ) duplicates
    ON indx.{column_name} = duplicates.{column_name};
    """

    cursor.execute(query)
    duplicates = cursor.fetchall()

    # Check if duplicates were found
    if duplicates:
        return duplicates

    return None

def main():
    # Argument parser setup
    parser = argparse.ArgumentParser(description="Connect to a SQLite database with indexed files/directories.")

    # Add database file parameter
    parser.add_argument('db_file', type=str, help="Path to the SQLite3 database file containing indexes files/directories")
    parser.add_argument('--table_name', type=str, default='file_indexes', help="Name of the table in SQLite database (default: file_indexes)")

    # Parse command-line arguments
    args = parser.parse_args()

    # Connect to the SQLite database
    conn = connect_to_database(args.db_file)

    duplicates = find_duplicates_by(conn, args.table_name, "size", "*")

    # Close the connection (if successful)
    if conn:
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    main()
