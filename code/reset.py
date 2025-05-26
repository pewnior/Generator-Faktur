from datetime import date
import os
from tkinter import messagebox
def reset():
   if messagebox.askyesno("Reset", "Czy na pewno chcesz zresetować numery oraz miejsce zapisu?"):
        today=date.today()
        cur_year=today.year
        current_path = os.path.dirname(os.path.realpath(__file__))
        filepath = "number.txt"
        full_file_path = os.path.join(current_path, filepath)

        f = open(full_file_path, "w")
        f.write(str(cur_year) +"\n" + "0")   
        f.close()

        filepath = "save_location_path.txt"
        full_file_path = os.path.join(current_path, filepath)
        f = open(full_file_path, "w")
        filepath = "../faktury"
        full_file_path = os.path.join(current_path, filepath)
        f.write(full_file_path)   
        f.close()
        messagebox.showinfo("Zresetowano", "Zresetowano numery oraz miejsce zapisu")