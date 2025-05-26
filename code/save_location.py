from tkinter import filedialog, messagebox
import os

current_path = os.path.dirname(os.path.realpath(__file__))

def give():
    filepath = "save_location_path.txt"
    full_file_path = os.path.join(current_path, filepath)
    f = open(full_file_path, "r")
    path=f.readline()
    f.close()
    return path

def select_folder():
        folder_path = filedialog.askdirectory(title="Wybierz folder zapisu")
        return folder_path

def change():
    folder_path=select_folder()
    filepath = "save_location_path.txt"
    full_file_path = os.path.join(current_path, filepath)
    f = open(full_file_path, "w")
    f.write(folder_path)
    f.close()
    messagebox.showinfo("Dokonano zmiany", "Dokonano zmiany")

    

