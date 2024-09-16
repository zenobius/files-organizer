"""
This module provides functions for indexing directories and files, calculating their MD5 hashes,
and saving the metadata to a CSV file(s).
"""

import os
import csv
import argparse
import mimetypes

from common import create_md5_hash, get_list_of_files_from


def get_file_metadata(paths: list[str]) -> list[dict]:
    """Retrieves metadata for a list of files or directories.

    Args:
        paths: A list of file or directory paths.

    Returns:
        A list of dictionaries, each containing metadata for a file or directory.
    """

    metadata = []

    for path in paths:
        try:
            if os.path.isdir(path):
                file_ext = ""
                file_size = 0
                file_type = "dir"
            elif os.path.isfile(path):
                file_ext = str.lower(os.path.splitext(path)[1][1:])
                file_size = os.path.getsize(path)
                file_type = "file"
            else:
                file_ext = str.lower(os.path.splitext(path)[1][1:])
                file_size = os.path.getsize(path)
                file_type = "n/a"

            file_info = {
                "path": os.path.abspath(path),
                "name": os.path.basename(path),
                "name_no_ext": os.path.splitext(os.path.basename(path))[0],
                "ext": file_ext,
                "size": file_size,
                "type": file_type,
                "mime": mimetypes.guess_type(path)[0],
                "created_at": os.path.getctime(path),
                "modified_at": os.path.getmtime(path),
            }

        # Handles i.e.: "[WinError 1920] The file cannot be accessed by the system" error
        except OSError as e:
            print(e)

            file_info = {
                "path": os.path.abspath(path),
                "name": os.path.basename(path),
                "name_no_ext": os.path.splitext(os.path.basename(path))[0],
                "ext": str.lower(os.path.splitext(path)[1][1:]),
                "size": "n/a",
                "type": "n/a",
                "mime": mimetypes.guess_type(path)[0],
                "created_at": "n/a",
                "modified_at": "n/a",
            }

        file_info["hash"] = create_md5_hash(
            str(file_info["type"]) +
            str(file_info["name"]) +
            str(file_info["size"])
        )

        metadata.append(file_info)

    return metadata


def main():
    """The main entry point of the script.

    Parses command-line arguments, indexes files and directories, calculates their metadata, and
    saves the results to a CSV file.
    """

    parser = argparse.ArgumentParser(
        description="A Python script that indexes directories and files and outputs the list."
    )

    parser.add_argument("start_dir", help="Directory path to root directory")
    parser.add_argument("output_file", help="Path to file to write index data of given start_dir")

    args = parser.parse_args()

    print(f"Running for {args.start_dir}; Saving to {args.output_file}")

    files, dirs = get_list_of_files_from(args.start_dir)

    indexes = files + dirs

    metadata = get_file_metadata(indexes)

    with open(args.output_file, mode='w', newline='', encoding='utf-8') as csvfile:
        if metadata:
            writer = csv.DictWriter(csvfile, fieldnames=metadata[0].keys())
            writer.writeheader()
            writer.writerows(metadata)


if __name__ == "__main__":
    main()
