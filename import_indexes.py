"""
Module to combine CSV files from a root folder and store them in an SQLite database.

This script takes a root folder containing CSV files, combines them into a single
table in an SQLite database, and creates indexes for efficient querying.

The script:
    - Gathers CSV files from the root folder.
    - Combines them into a single SQLite table.
    - Adds optional columns like 'action' and 'handler'.
    - Creates indexes for optimized lookups.
"""

import argparse
import sqlite3
import pandas as pd

from common import get_list_of_files_from_ext

def main() -> None:
    """
    Main function to combine CSV files from a root folder and insert them into an SQLite database.
    """

    parser = argparse.ArgumentParser(
        description="Combine CSV files from a root folder and store them in an SQLite database."
        )
    parser.add_argument(
        'root_folder',
        type=str,
        help="Root folder containing CSV files created by create_indexes.py"
        )
    parser.add_argument(
        'output_db_file',
        type=str,
        help="SQLite database/file to create"
        )
    parser.add_argument(
        '--table_name',
        type=str,
        default='indexed_files',
        help="Name of the table for indexes in SQLite database (default: indexed_files)"
        )

    args = parser.parse_args()

    csv_files, _ = get_list_of_files_from_ext(args.root_folder, "csv")

    if not csv_files:
        print(f"No CSV files found in the specified root folder: {args.root_folder}")
        return

    print(f"Found {len(csv_files)} CSV files, processing...")

    dtypes = {
        "path": "string",
        "name": "string",
        "name_no_ext": "string",
        "ext": "string",
        "size": "Int64",
        "type": "string",
        "mime": "string",
        "created_at": "float",
        "modified_at": "float",
        "hash": "string"
        }

    conn = sqlite3.connect(args.output_db_file)
    count = 0

    for file in csv_files:
        print(f"Importing {file}...")
        try:
            df = pd.read_csv(file, dtype=dtypes)
            if not df.empty:
                count += len(df)
                print(f"Saving {len(df)} rows from {file}")
                df.to_sql(args.table_name, conn, if_exists='append', index=False)

        except pd.errors.EmptyDataError:
            print(f"Error: {file} is empty. Skipping.")

        except FileNotFoundError:
            print(f"Error: {file} not found.")

        except sqlite3.DatabaseError as db_err:
            print(f"Database error while importing {file}: {db_err}")

    print("Finished importing CSV files into database.")

    print(f"Adding additional columns to {args.table_name}: action, handler")
    conn.execute(f"ALTER TABLE {args.table_name} ADD COLUMN action TEXT NULL;")
    conn.execute(f"ALTER TABLE {args.table_name} ADD COLUMN handler TEXT NULL;")

    print(f"Creating indexes on {args.table_name} table.")
    conn.execute(f"CREATE INDEX ix_file_indexes_path ON {args.table_name} (path);")
    conn.execute(f"CREATE INDEX ix_file_indexes_name ON {args.table_name} (name);")
    conn.execute(f"CREATE INDEX ix_file_indexes_ext ON {args.table_name} (ext);")
    conn.execute(f"CREATE INDEX ix_file_indexes_size ON {args.table_name} (size);")
    conn.execute(f"CREATE INDEX ix_file_indexes_type ON {args.table_name} (type);")
    conn.execute(f"CREATE INDEX ix_file_indexes_mime ON {args.table_name} (mime);")
    conn.execute(f"CREATE INDEX ix_file_indexes_hash ON {args.table_name} (hash);")
    conn.execute(f"CREATE INDEX ix_file_indexes_action ON {args.table_name} (action);")
    conn.execute(f"CREATE INDEX ix_file_indexes_handler ON {args.table_name} (handler);")

    conn.close()

    print(f"{len(csv_files)} CSV files containing {count} rows combined and inserted into {args.output_db_file} (table: {args.table_name}).")

if __name__ == "__main__":
    main()
