# AutoFileTransfer
Automate file management


## To create paths_list.txt file
```bash
find /Path/to/folder/ -name '*.pdf' > paths_list.txt
```

this will find all files that end with .pdf in /Path/to/folder/ and write their paths to paths_list.txt

## Test it on blassa and blassa_okhra by running
```bash
find . -name '*.pdf' > paths_list.txt
```

## When using move[mo]
if you're afraid to forget each file's previous path, then copy the paths_list.txt to the destination folder, so you can return to it whenever needed
