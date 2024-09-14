# files-organizer
Indexing files and directories with python CLI

`$dir_index = (Get-ChildItem -Directory -Name)`
`$dir_index | ForEach-Object { $dir = $_; $safeName = [IO.Path]::GetInvalidFileNameChars() -join ''; $outputFile = "$($dir -replace $safeName, '_').csv"; python.exe e:/scripts/index_dirfiles.py $dir (Join-Path "e:\scripts\bck_indexes" $outputFile) }`