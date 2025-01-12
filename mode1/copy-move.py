import os
import shutil
import sys

with open('paths_list.txt', 'r') as f:
    paths = [line.rstrip('\n') for line in f.readlines()]


copy_or_move = input('copy[Co] | move[Mo]: ').lower()
if copy_or_move == 'co' :
    copy_or_move = 'copy'
elif copy_or_move =='mo' :
    confirm = input('are you sure you want move files? ').lower()
    if confirm == 'yes':
        copy_or_move = 'move'
    else:
        print("Operation canceled. Ending script.")
        sys.exit()
else:
    print("Operation canceled. Ending script.")
    sys.exit()


# Creating destination directory
def check_file_or_directory_existance(dir_or_file): # input: the file or directory you want to check on
    dir_or_file_already_exist = True
    k = 1
    
    unique = dir_or_file
    unique2, its_extension = os.path.splitext(dir_or_file)

    while dir_or_file_already_exist: # if file or folder is unique, the variable will be as False and the while loop will be breaked
        if os.path.exists(unique): # check and rename if not unique
            unique = unique2 + f'({k})' + its_extension
            k+=1
        else:
            dir_or_file_already_exist = False
    return unique # return the same file or directory if unique else the renamed file or directory will be returned
    
dest_dir = input('destination folder name: ')

if not(os.path.exists(dest_dir)):
    dest_dir = check_file_or_directory_existance(dest_dir)
    os.mkdir(dest_dir)
    print(f'{dest_dir} created successfully')



#init log file
log_file = check_file_or_directory_existance(f'{dest_dir}_logs.txt')
with open(log_file, 'w') as f:
    f.write('')

# copying files
for src_path in paths:
    try:
        if os.path.exists(src_path):
            # (you may think that wa have created a new destination directory, but the files that will be copied|moved can have the same name), the following lines handle that problem
            file_in_dest = rf'{dest_dir}/{os.path.basename(src_path)}' # to not overwrite files ;)
            dst_dir = check_file_or_directory_existance(file_in_dest)
            if copy_or_move == 'copy':
                shutil.copy(src_path, dst_dir)
                print(f'{src_path} copied successfully to {dst_dir}')
            elif copy_or_move == 'move':
                shutil.move(src_path, dst_dir)
                print(f'{src_path} moved successfully to {dst_dir}')

        else :
            print(f'No file or directory {src_path}')
            with open(log_file, 'a') as f:
                f.write(f'{src_path} No file or directory \n')

    except Exception as hmm:

        if copy_or_move == 'co':
            print(f'{src_path} not copied \n')
            
        else: 
            print(f'{src_path} not moved \n')

        with open(log_file, 'a') as f:
            if copy_or_move == 'co':
                f.write(f'{src_path} not copied \n {hmm} \n\n')
                
            else:
                f.write(f'{src_path} not moved \n {hmm} \n\n')

        
