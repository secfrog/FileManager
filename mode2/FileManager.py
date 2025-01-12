import os
import shutil
import sys

List_of_logs = []

def Read_files(file, dest=False):
    if not os.path.exists(file):
        print(f"Invalid path! {file}")
        List_of_logs.append(f"Invalid path {file} \n\n")
        print("Operation Canceled. Ending Script..")
        sys.exit()
    
    with open(file, 'r') as f:
        Paths = [line.rstrip('\n') for line in f.readlines()]
    
    PathsList = []
    for p in Paths:
        if os.path.exists(p):
            if dest == True and os.path.isfile(p):
                print(f'{p} is file not directory\nDestination ignored \n')
                List_of_logs.append(f'{p} is file not directory\nDestination ignored \n\n')
            
            else:
                PathsList.append(p)
        else:
            print(f'path {p} not found\npath ignored\n')
            List_of_logs.append(f'path {p} not found \npath ignored \n\n')
    
    return PathsList

Source_Paths_file = input(rf"Source_Paths_List's path: ")
Destination_Paths_List = input(rf"Destination_Paths_List's path: ")
print('')

SrcPathList = Read_files(Source_Paths_file)
DestPathList = Read_files(Destination_Paths_List, True)


def WhatToDo():
    ToDo = input('Copy[Co] | Move[Mo]: ').lower()
    match ToDo:
        case "co":
            print('Proceeding to copy')
        case "mo":
            confirm = input('Are you sure you want to move files? ').lower()
            if confirm in ['yes', 'y']:
                print('Proceeding to move')
            else:
                print('Operation canceled. Ending script..')
                sys.exit()
        case _:
            print('Operation canceled. Ending script..')
            sys.exit()
    return ToDo
ToDo = WhatToDo()


def Unique_Path(Path):
    Path_already_exist = True
    k = 1
    
    UniquePath = Path
    UniquePath2, extension = os.path.splitext(Path)

    while Path_already_exist:
        if os.path.exists(UniquePath):
            UniquePath = UniquePath2 + f'({k})' + extension
            k+=1
        else:
            Path_already_exist = False
    return UniquePath

paths_to_remove = [] # in case of a move operation
for src_path in SrcPathList:
    for dest_path in DestPathList:
        try:
            check_path = rf'{dest_path}/{os.path.basename(src_path)}'
            new_dest_path = Unique_Path(check_path)

            if ToDo == 'co':
                shutil.copy(src_path, new_dest_path)
                print(f'{src_path} copied to {new_dest_path}')
            elif ToDo == 'mo':
                shutil.copy(src_path, new_dest_path)
                print(f'{src_path} moved to {new_dest_path}')
                if src_path not in paths_to_remove:
                    paths_to_remove.append(src_path)

        except Exception as hmm:
            if ToDo == 'co':
                print(f'{src_path} not copied \n')
                List_of_logs.append(f'{src_path} not copied \n {hmm} \n\n')

            elif ToDo == 'mo':
                print(f'{src_path} not moved \n')
                List_of_logs.append(f'{src_path} not moved \n {hmm} \n\n')

for p in paths_to_remove:
    try:    
        os.remove(p)
    except Exception as hmm:
        print(f'file {p} not moved only transfered\n')
        List_of_logs.append(f'file {p} not moved only transfered\n{hmm}\n\n')

logs = Unique_Path('logs.txt')

with open(logs, 'w') as f:
    f.write('')

with open(logs, 'a') as f:
    for i in List_of_logs:
        f.write(i)