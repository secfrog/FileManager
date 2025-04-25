import os
import shutil
import sys
from customtkinter import (
    CTk,
    CTkFrame,
    CTkLabel,
    CTkEntry,
    CTkCheckBox,
    CTkButton,
    CTkOptionMenu,
    StringVar,
    set_appearance_mode,
    set_default_color_theme
)


#########################GUI#########################
colors=("#3D3D3D", "#333333", "#4A4A4A", "#131313")

class Filemanager:
    def __init__(self, master):
        self.frame0 = Bg_frame(master)
        self.frame1 = Label_frame(self.frame0, "𓆏 Tab1")
        self.frame2 = Main_frame(self.frame0)
        
        self.List_of_logs = []

    def Read_files(self, file, dest=False):
        if not os.path.exists(file):
            print(f"Invalid path! {file}")
            self.List_of_logs.append(f"Invalid path {file} \n\n")
            print("Operation Canceled. Ending Script..")
            sys.exit()
        
        with open(file, 'r') as f:
            Paths = [line.rstrip('\n') for line in f.readlines()]
        
        PathsList = []
        for p in Paths:
            if os.path.exists(p):
                if dest == True and os.path.isfile(p):
                    print(f'{p} is file not directory\nDestination ignored \n')
                    self.List_of_logs.append(f'{p} is file not directory\nDestination ignored \n\n')
                
                else:
                    PathsList.append(p)
            else:
                print(f'path {p} not found\npath ignored\n')
                self.List_of_logs.append(f'path {p} not found \npath ignored \n\n')
        
        return PathsList

    def WhatToDo(self):
        ToDo = self.frame2.get_user_preferences()[-1]
        match ToDo:
            case "copy":
                print('Proceeding to copy')
            case "move":
                print('Proceeding to move')

        return ToDo

    def Unique_Path(self, Path):
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

    def do_work(self):
        try:
            SrcPathList = self.Read_files(self.frame2.get_user_preferences()[0])
            DestPathList = self.Read_files(self.frame2.get_user_preferences()[1], True)
        except:
            sys.exit()
        ToDo = self.WhatToDo()
        paths_to_remove = [] # in case of a move operation      
        for src_path in SrcPathList:
            for dest_path in DestPathList:
                try:
                    check_path = rf'{dest_path}/{os.path.basename(src_path)}'
                    new_dest_path = self.Unique_Path(check_path)        
                    match ToDo:
                        case "copy":
                            shutil.copy(src_path, new_dest_path)
                            print(f'{src_path} copied to {new_dest_path}')
                        case "move":
                            shutil.copy(src_path, new_dest_path)
                            print(f'{src_path} moved to {new_dest_path}')
                            if src_path not in paths_to_remove:
                                paths_to_remove.append(src_path)        
                except Exception as hmm:
                    match ToDo:
                        case "copy":
                            print(f'{src_path} not copied \n')
                            self.List_of_logs.append(f'{src_path} not copied \n {hmm} \n\n')        
                        case "move":
                            print(f'{src_path} not moved \n')
                            self.List_of_logs.append(f'{src_path} not moved \n {hmm} \n\n')     
        for p in paths_to_remove:
            try:    
                os.remove(p)
            except Exception as hmm:
                print(f'file {p} not moved only transfered\n')
                self.List_of_logs.append(f'file {p} not moved only transfered\n{hmm}\n\n')      
        logs = self.Unique_Path('logs.txt')     
        with open(logs, 'w') as f:
            f.write('')     
        with open(logs, 'a') as f:
            for i in self.List_of_logs:
                f.write(i)
        
class Bg_frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0)
        self.configure(fg_color=colors[0])
        self.pack(fill="both", expand=True)
        

class Label_frame(CTkFrame):
    def __init__(self, master, text="Default"):
        super().__init__(master, width=120, height=35, fg_color=colors[1], corner_radius=0)
        self.pack(ipadx=50, side="top", anchor="nw")
        self.pack_propagate(False) # To prevent frame resizing

        self.Text = text
        label1 = CTkLabel(master=self, text=self.Text, font=("Times New Roman", 16), text_color="white")
        label1.pack(side="left", padx=15, pady=2, anchor="center")

        button1 = CTkButton(
            master=self,
            text="\u2715",
            fg_color=colors[1],
            hover_color=colors[2],
            width=6,
            height=6,
            corner_radius=50,
            command=sys.exit,
        )
        button1.configure(cursor="arrow")
        button1.pack(side="right", padx=10)


class Main_frame(CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color=colors[1], corner_radius=0)
        self.pack(fill="both", expand=True)


        ### Entries
        self.ask_srcp = CTkEntry(master=self, placeholder_text="Source paths file", font=("Times New Roman", 16), justify="center", width=200)
        self.ask_destp = CTkEntry(master=self, placeholder_text="Destination paths file", font=("Times New Roman", 16), justify="center",  width=200)

        self.ask_srcp.place(x=10, y=100)
        self.ask_destp.place(x=10, y=140)
        ###


        ### Menus
        option_menu = StringVar(value="Menu")
        self.menu = CTkOptionMenu(master=self,variable=option_menu, values=["copy", "move"])
        self.menu.place(x=250, y=100)
        ###


        ### Checkboxes
        self.confirm = CTkCheckBox(master=self, text="Confirm",font=("Times New Roman", 14), checkbox_height=20, checkbox_width=20, border_width=2, border_color=colors[3], corner_radius=5)
        self.confirm.place(x=20, y=200)
        ###


        ### Buttons
        self.button = CTkButton(master=self, text="enter", command=self.get_user_preferences)
        self.button.place(x=250, y=200)

    
    def get_user_preferences(self):
        self.Source_Paths_file = self.ask_srcp.get()
        self.Destination_Paths_file = self.ask_destp.get()
        confirmed = self.confirm.get()
        self.option = self.menu.get()
        
        if len(self.Source_Paths_file) != 0 and len(self.Destination_Paths_file) != 0 and confirmed and self.option != "Menu":
            root.quit()
            root.withdraw()

            return (
                self.Source_Paths_file,
                self.Destination_Paths_file,
                self.option,
            )
            

def clear_focus(event):
    event.widget.focus_set()
#########################GUI#########################







if __name__ == '__main__':
    set_appearance_mode("dark")
    set_default_color_theme("dark-blue")

    root = CTk()
    root.geometry("400x350")
    root.title("File Manager")
    root.iconbitmap(bitmap="icon.ico")
    
    app = Filemanager(root)
     
    root.bind("<Button-1>", clear_focus)    
    
    root.mainloop()
    
    app.do_work()
