import os
import argparse
import sqlite3
import pandas as pd

# Function to get all CSV files from the root folder and its subdirectories
def get_csv_files(root_folder):
    csv_files = []
    for root, _, files in os.walk(root_folder):
        for file in files:
            if file.endswith(".csv"):
                csv_files.append(os.path.join(root, file))
    return csv_files

# Function to combine CSV files into a single DataFrame
def combine_csv_files(csv_files):
    combined_df = pd.concat([pd.read_csv(file) for file in csv_files], ignore_index=True)
    return combined_df

# Function to load DataFrame into SQLite database
def load_to_sqlite(df, db_name, table_name):
    conn = sqlite3.connect(db_name)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()

# Main function to combine CSV files from a root folder and insert into SQLite
def main():
    # Setup argparse for command-line argument handling
    parser = argparse.ArgumentParser(description="Combine CSV files from a root folder and store them in an SQLite database.")
    parser.add_argument('root_folder', type=str, help="Root folder containing CSV files")
    parser.add_argument('output_db_file', type=str, help="Output SQLite database file")
    parser.add_argument('--table_name', type=str, default='file_indexes', help="Name of the table in SQLite database (default: file_indexes)")

    # Parse the arguments
    args = parser.parse_args()

    # Step 1: Get all CSV files from the root folder
    csv_files = get_csv_files(args.root_folder)

    if not csv_files:
        print(f"No CSV files found in the specified root folder: {args.root_folder}")
        return

    # Step 2: Combine CSV files into a single DataFrame
    combined_df = combine_csv_files(csv_files)

    # Step 3: Insert the combined DataFrame into an SQLite database
    load_to_sqlite(combined_df, args.output_db_file, args.table_name)

    print(f"CSV files combined and inserted into {args.output_db_file} (table: {args.table_name}).")

if __name__ == "__main__":
    main()
