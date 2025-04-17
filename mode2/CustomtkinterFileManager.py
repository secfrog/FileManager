import os
import shutil
import sys
import customtkinter




############# User Interface #############
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("600x600")


frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="File Manager")
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="Source Paths List")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="Destination Paths List")
entry2.pack(pady=12, padx=10)

Copybox = customtkinter.CTkCheckBox(master=frame, text="Copy")
Copybox.pack(pady=12, padx=10)

Movebox = customtkinter.CTkCheckBox(master=frame, text="Move")
Movebox.pack(pady=12, padx=10)

checkbox = customtkinter.CTkCheckBox(master=frame, text="Confirm")
checkbox.pack(pady=12, padx=10)
#############                #############

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


def WhatToDo():
    ToDo = (Copybox.get(), Movebox.get())
    match ToDo:
        case (1, 0):
            print('Proceeding to copy')
        case (1, 0):
            print('Proceeding to move')
    return ToDo


def get_Source_and_dest_Paths_file():
    global Source_Paths_file, Destination_Paths_List

    Source_Paths_file = entry1.get()
    Destination_Paths_List = entry2.get()
    checkbox.get()
    
    if len(Source_Paths_file) != 0 and len(Destination_Paths_List) != 0 and checkbox.get() and ((Copybox.get() and not Movebox.get()) or (Movebox.get() and not Copybox.get())):
        root.quit()
        root.withdraw()

#####
button = customtkinter.CTkButton(master=frame, text="enter", command=get_Source_and_dest_Paths_file)
button.pack(pady=12, padx=10)
root.mainloop()
#####


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
        
def do_work():
    if 'Source_Paths_file' in globals():
        SrcPathList = Read_files(Source_Paths_file)
        DestPathList = Read_files(Destination_Paths_List, True)
        ToDo = WhatToDo()
        paths_to_remove = [] # in case of a move operation

        for src_path in SrcPathList:
            for dest_path in DestPathList:
                try:
                    check_path = rf'{dest_path}/{os.path.basename(src_path)}'
                    new_dest_path = Unique_Path(check_path)

                    match ToDo:
                        case (1,0):
                            shutil.copy(src_path, new_dest_path)
                            print(f'{src_path} copied to {new_dest_path}')
                        case (0,1):
                            shutil.copy(src_path, new_dest_path)
                            print(f'{src_path} moved to {new_dest_path}')
                            if src_path not in paths_to_remove:
                                paths_to_remove.append(src_path)

                except Exception as hmm:
                    match ToDo:
                        case (1,0):
                            print(f'{src_path} not copied \n')
                            List_of_logs.append(f'{src_path} not copied \n {hmm} \n\n')

                        case (0,1):
                            print(f'{src_path} not moved \n')
                            List_of_logs.append(f'{src_path} not moved \n {hmm} \n\n')

        for p in paths_to_remove:
            try:    
                os.remove(p)
            except Exception as hmm:
                print(f'file {p} not moved only transfered\n')
                List_of_logs.append(f'file {p} not moved only transfered\n{hmm}\n\n')
do_work()

logs = Unique_Path('logs.txt')

with open(logs, 'w') as f:
    f.write('')

with open(logs, 'a') as f:
    for i in List_of_logs:
        f.write(i)

