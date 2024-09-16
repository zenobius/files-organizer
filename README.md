# files-organizer
## !!! THIS IS WORK IN PROGRESS !!!
Please don't judge me ;-)

# What?
These scripts provide __VERY BASIC__ way to index all files and directories (recursively) in given path to help you with organizing you messy drive or backup folder.

# How?
Use `create_indexes.py` to.. create indexes (py). It takes `start_dir` parameter and goes through all files and directories in it gathering basic data and saves it to `output_file` in CSV format.

For details see source file.

Use 'import_indexes.py` to import CSV files created by `create_indexes.py` into a SQLite database for easy(ier) data searching.

For details see source file.

__Don't use__ `search_indexes.py` as it's still work in progress and I'm doing my operations by manual SQL queries.

# Why?
I'm in "Autumn Cleaning" mode and I have (now had) a Backups folder that's reminiscent of that one drawer in your kitchen that contains everything that doesn't have its place or that one box you have with all the things you've gathered for last 20 years including that Nokia 3310 charger you know you should throw out.

My first lines of code written in gwbasic on an IBM AT clone, my own PHP framework, you know the drill.

I wanted to finally deduplicate files, get rid of all archives containing duplicates, index all files containing some history (like GG archives, or IRC logs, or old Usenet posts), delete anything that's not needed and so on.. so here we are.

I've started with 3095685 entries in the indexes (430141 directories and 2665544 files).

# Usage
I use windows as day-to-day system (WSL2 is great) to work and play, so I've started with using explorer to search for what I wanted. TL;DR: it sucks. Then I went to PowerShell scripts but it turns out I need to allow Windows to execute scripts (not one liners) and I didn't want to open myself to that kind of pain.

PowerShell one liners didn't do the trick and I didn't want to perform indexing after every action I took so I chosen using PowerShell and Python to do my bidding.

## Examples
I don't want my PC to choke while storing >3mln data points in memory so I use PowerShell and Python at the same time:

* Creating local variable to store a list of directories (not files, not recursive) in current directory to index:
`$dir_index = (Get-ChildItem -Directory -Name)`

* Check if the list is correct and contains what I wanted:
`$dir_index`
it just echos/outputs the list of directories to cmd

* Process all directories in `$dir_index` by calling `create_indexes.py` script with proper arguments:
`$dir_index | ForEach-Object { $dir = $_; $safeName = [IO.Path]::GetInvalidFileNameChars() -join ''; $outputFile = "$($dir -replace $safeName, '_').csv"; python.exe create_indexes.py $dir (Join-Path "c:\output_directory" $outputFile) }` creates CSV file with indexes for each directory stored in `$dir_index`

* Import CSV files into one SQLite db file: `python.exe import_indexes.py c:\output_directory c:\database_containing_indexes_file.db`

Now you can work the data. Here are some examples:

* Find all archives:
`sqlite3 c:\database_containing_indexes_file.db "SELECT path FROM indexed_files WHERE ext IN ('zip', 'rar', '7z', 'gz', 'tar') ORDER BY path;" > c:\all_archives.csv`

* Unzip all the archives using `7-zip` to directories named like the archive filename:
`Import-Csv -Path "C:\all_archives.csv" | ForEach-Object { $destDir = Join-Path -Path ([System.IO.Path]::GetDirectoryName($_.Path)) -ChildPath ([System.IO.Path]::GetFileNameWithoutExtension($_.Path)); New-Item -Path $destDir -ItemType Directory -Force; & 'C:\Program Files\7-Zip\7z.exe' x $_.Path -o"$destDir" -y }`

* Remove all files exported from db in previous step:
`Import-Csv -Path "e:\scripts\bck_indexes_check\qwe" -Header Path | ForEach-Object { Remove-Item -Path $_.Path -Force -Recurse }`

* Find duplicates of files based on hash (simple: type [file/dir] + name + size)
`sqlite3 e_indexed_files.db "SELECT * FROM indexed_files ind JOIN ( SELECT hash FROM indexed_files GROUP BY hash HAVING COUNT(hash) > 1 ) dupl ON ind.hash = dupl.hash;" > c:\duplicates_by_hash.csv`

And so on and so on..

