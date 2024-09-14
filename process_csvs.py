import os
import argparse
import sqlite3
import pandas as pd

from common import get_list_of_files_from_ext

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
    csv_files, _ = get_list_of_files_from_ext(args.root_folder, "csv")

    if not csv_files:
        print(f"No CSV files found in the specified root folder: {args.root_folder}")
        return

    print(f"Found {len(csv_files)} CSV files, processing...")

    # Step 2: Combine CSV files into a single DataFrame and save to SQLite db
    dtypes = {
        "path": "string",
        "filename": "string",
        "extension": "string",
        "size": int,
        "type": "string",
        "mime_type": "string",
        "created_time": "float",
        "modified_time": "float",
        "hash": "string",
        "hash_w_name_created": "string",
        "hash_w_created": "string",
        "hash_w_name_modified": "string",
        "hash_w_modified": "string"
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
        except Exception as e:
            print(f"Error importing {file}, size {os.path.getsize(file)}: {e}")

    print("Finished importing CSV files into database.")

    print(f"Adding additional columns to {args.table_name}: action, handler, status")
    conn.execute(f"ALTER TABLE {args.table_name} ADD COLUMN action TEXT NULL;")
    conn.execute(f"ALTER TABLE {args.table_name} ADD COLUMN handler TEXT NULL;")
    conn.execute(f"ALTER TABLE {args.table_name} ADD COLUMN status TEXT NULL;")

    print(f"Creating indexes on {args.table_name} table.")
    conn.execute(f"CREATE INDEX ix_file_indexes_path ON {args.table_name} (path);")
    conn.execute(f"CREATE INDEX ix_file_indexes_filename ON {args.table_name} (filename);")
    conn.execute(f"CREATE INDEX ix_file_indexes_extension ON {args.table_name} (extension);")
    conn.execute(f"CREATE INDEX ix_file_indexes_size ON {args.table_name} (size);")
    conn.execute(f"CREATE INDEX ix_file_indexes_type ON {args.table_name} (type);")
    conn.execute(f"CREATE INDEX ix_file_indexes_mime_type ON {args.table_name} (mime_type);")
    conn.execute(f"CREATE INDEX ix_file_indexes_hash ON {args.table_name} (hash);")
    conn.execute(f"CREATE INDEX ix_file_indexes_hash_w_name_created ON {args.table_name} (hash_w_name_created);")
    conn.execute(f"CREATE INDEX ix_file_indexes_hash_w_created ON {args.table_name} (hash_w_created);")
    conn.execute(f"CREATE INDEX ix_file_indexes_hash_w_name_modified ON {args.table_name} (hash_w_name_modified);")
    conn.execute(f"CREATE INDEX ix_file_indexes_hash_w_modified ON {args.table_name} (hash_w_modified);")
    conn.execute(f"CREATE INDEX ix_file_indexes_action ON {args.table_name} (action);")
    conn.execute(f"CREATE INDEX ix_file_indexes_handler ON {args.table_name} (handler);")
    conn.execute(f"CREATE INDEX ix_file_indexes_status ON {args.table_name} (status);")

    conn.close()

    print(f"{len(csv_files)} CSV files containing {count} rows combined and inserted into {args.output_db_file} (table: {args.table_name}).")

if __name__ == "__main__":
    main()
