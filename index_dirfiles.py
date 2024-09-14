"""
_summary_
"""
import os
import csv
import argparse
import mimetypes

from common import create_md5_hash, get_list_of_files_from

def get_file_metadata(paths):
    """Gets metadata about files and folders from a list of paths.

    Args:
    paths: A list of paths to files or folders.

    Returns:
    A list of dictionaries, each containing metadata for a file or folder.
    """
    metadata = []

    for path in paths:
        try:
            if os.path.isdir(path):
                file_type = "dir"
                file_size = 0
            elif os.path.isfile(path):
                file_type = "file"
                file_size = os.path.getsize(path)
            else:
                file_type = "n/a"
                file_size = os.path.getsize(path)

            file_info = {
                "path": os.path.abspath(path),
                "filename": os.path.basename(path),
                "extension": str.lower(os.path.splitext(path)[1][1:]),
                "size": file_size,
                "type": file_type,
                "mime_type": mimetypes.guess_type(path)[0],
                "created_time": os.path.getctime(path),
                "modified_time": os.path.getmtime(path),
            }

        # Handles i.e.: "[WinError 1920] The file cannot be accessed by the system" error
        except OSError as e:
            print(e)

            file_info = {
                "path": os.path.abspath(path),
                "filename": os.path.basename(path),
                "extension": str.lower(os.path.splitext(path)[1][1:]),
                "size": "n/a",
                "type": "n/a",
                "mime_type": mimetypes.guess_type(path)[0],
                "created_time": "n/a",
                "modified_time": "n/a",
            }

        file_info["hash"] = create_md5_hash(
            file_info["filename"]
            + file_info["type"]
            + str(file_info["size"]))

        file_info["hash_w_name_created"] = create_md5_hash(
            file_info["filename"]
            + file_info["type"]
            + str(file_info["size"])
            + str(file_info["created_time"]))

        file_info["hash_w_created"] = create_md5_hash(
            file_info["type"]
            + str(file_info["size"])
            + str(file_info["created_time"]))

        file_info["hash_w_name_modified"] = create_md5_hash(
            file_info["filename"]
            + file_info["type"]
            + str(file_info["size"])
            + str(file_info["modified_time"]))

        file_info["hash_w_modified"] = create_md5_hash(
            file_info["type"]
            + str(file_info["size"])
            + str(file_info["modified_time"]))

        metadata.append(file_info)

    return metadata


def main():
    """
    _summary_
    """
    parser = argparse.ArgumentParser(
        description="A Python script that indexes directories and files and outputs the list."
        )

    # Required parameters:
    parser.add_argument("start_dir", help="Directory path to root directory.")
    parser.add_argument("output_file", help="Path to file to write index data of given start_dir.")

    args = parser.parse_args()

    print(f"Running for {args.start_dir}; Saving to {args.output_file}.")

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
