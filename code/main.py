
# version 4.0
version="4.0"

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import os
from generator import generate_invoice
from datetime import date
from invoice_number_gen import new_number
from seller_addition import add_seller
from save_location import *
from reset import reset
import json


current_path = os.path.dirname(os.path.realpath(__file__))

def refresh_seller_combobox():
    try:
        full_file_path = os.path.join(current_path, "sellers.json")
        with open(full_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        global sellers_dict
        sellers_dict = {s["name"]: s for s in data["sellers"]}
        seller_combobox['values'] = list(sellers_dict.keys())
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się odświeżyć listy sprzedawców:\n{e}")


def validation():
    
    pesel=pesel_entry.get()
    if(pesel!=""):
        if(len(str(pesel))!=11):
            messagebox.showerror("Błąd", "Nieprawidłowy PESEL")
            return
        
    for row in item_rows:
        if(row[0].get()!=""):
            name = row[0].get()

            try:
                quantity = int(row[1].get())
            except ValueError:
                messagebox.showerror("Błąd", "Nieprawidłowa ilość")
                return
            
            try:
                unit_price = float(row[2].get())
            except ValueError:
                messagebox.showerror("Błąd", "Nieprawidłowa kwota")
                return 
    create_invoice()

def create_invoice():
    try:
        # Numer faktury
        number=new_number()
        naming="faktura_nr_"+str(number)+".pdf"
        number=number.replace("_", "/")

        # Pobieranie danych sprzedawcy
        selected_name = seller_combobox.get() 
        selected_seller = sellers_dict.get(selected_name)
        sellerp1=selected_seller["sellerp1"]
        sellerp2=selected_seller["sellerp2"]
        sellerp3=selected_seller["address"]
        sellerp4=selected_seller["post"]
        sellerp5=selected_seller["nip"]
        

        # Dane sprzedawcy i kupującego
        invoice_data = {
            "sellerp1":sellerp1,
            "sellerp2":sellerp2,
            "sellerp3":sellerp3,
            "sellerp4":sellerp4,
            "sellerp5":sellerp5,
            "buyerp1": buyer_name_entry.get().strip(),
            "buyerp2": buyer_street_entry.get().strip(),
            "buyerp3": buyer_code_entry.get().strip(),
            "buyerp4": "PESEL: " + pesel_entry.get(),
            "invoice_number": number,
            "date": date.today(),
            "items": [],
            "pay_method": payment_method_listbox.get(payment_method_listbox.curselection()),
        }

        for row in item_rows:
            if(row[0].get()!=""):
                name = row[0].get()
                quantity = int(row[1].get())
                unit_price = float(row[2].get())
                total = quantity * unit_price
                invoice_data["items"].append({"name": name, "quantity": quantity, "unit_price": unit_price, "total": total})

        generate_invoice(naming, invoice_data)
    except Exception as e:
        messagebox.showerror("Błąd", f"Nie udało się wygenerować faktury: {e}")

#Opcje       
def exit_app():
    root.destroy()
def show_files():
    os.startfile(give())
def change_path():
    change()
def new_seller():
    add_seller()
def refresh():
    refresh_seller_combobox()

# Interfejs użytkownika
root = tk.Tk()
root.title("Generator Faktur by Maciej Pewniak")
root.geometry("600x500")
filepath = "icon.ico"
full_file_path = os.path.join(current_path, filepath)
root.wm_iconbitmap(full_file_path)

# Pasek menu
menu_bar = tk.Menu(root)

# Menu "Opcje"
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Dodaj sprzedawcę", command=new_seller)
file_menu.add_command(label="Zmień lokalizację zapisu", command=change_path)
#zmień dane sprzedawcy
file_menu.add_command(label="Pokaż faktury", command=show_files)
file_menu.add_separator()
file_menu.add_command(label="Wyjdź", command=exit_app)
menu_bar.add_cascade(label="Opcje", menu=file_menu)

# Menu "Pomoc"
help_menu = tk.Menu(menu_bar, tearoff=0)
help_menu.add_command(label="Reset", command=lambda: reset())
help_menu.add_separator()
help_menu.add_command(label="O programie", command=lambda: messagebox.showinfo("O programie", "Generator Faktur by Maciej Pewniak v"+version))
menu_bar.add_cascade(label="Pomoc", menu=help_menu)

# Dodanie paska menu do okna
root.config(menu=menu_bar)

# Pobieranie bazy sprzedawców
full_file_path = os.path.join(current_path, "sellers.json")
with open(full_file_path, "r", encoding="utf-8") as f:
    sellers_data = json.load(f)["sellers"]
sellers_dict = {seller["name"]: seller for seller in sellers_data}

# Wybór sprzedawcy
tk.Label(root, text="Sprzedawca:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w")
seller_var = tk.StringVar()
seller_combobox = ttk.Combobox(root, textvariable=seller_var, values=list(sellers_dict.keys()), state="readonly")
seller_combobox.grid(row=0, column=1, padx=5, pady=5)
seller_combobox.current(0)  # Ustaw domyślną wartość (pierwszą z listy)
tk.Button(root, text="Odśwież", font=("Arial", 8, "bold"), command=refresh).grid(row=0, column=2, pady=20)


# Sekcja nabywcy
tk.Label(root, text="Dane Nabywcy:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="w")
tk.Label(root, text="Imię i nazwisko:").grid(row=2, column=0, sticky="w")
buyer_name_entry = tk.Entry(root, width=50)
buyer_name_entry.grid(row=2, column=1, pady=5, padx=10)
tk.Label(root, text="Adres:").grid(row=3, column=0, sticky="w")
buyer_street_entry = tk.Entry(root, width=50)
buyer_street_entry.grid(row=3, column=1, pady=5, padx=10)
tk.Label(root, text="Kod pocztowy:").grid(row=4, column=0, sticky="w")
buyer_code_entry = tk.Entry(root, width=50)
buyer_code_entry.grid(row=4, column=1, pady=5, padx=10)

# Numer faktury i data
tk.Label(root, text="PESEL:").grid(row=5, column=0, sticky="w")
pesel_entry = tk.Entry(root)
pesel_entry.grid(row=5, column=1, pady=5, padx=0)

# Pozycje faktury
tk.Label(root, text="Pozycje faktury:", font=("Arial", 10, "bold")).grid(row=7, column=0, sticky="w")

item_frame = tk.Frame(root)
item_frame.grid(row=8, column=0, columnspan=2, pady=10, padx=10)

item_rows = []
for i in range(5):
    name_var = tk.StringVar()
    qty_var = tk.StringVar()
    price_var = tk.StringVar()
    tk.Entry(item_frame, textvariable=name_var, width=40).grid(row=i, column=0)
    tk.Entry(item_frame, textvariable=qty_var, width=10).grid(row=i, column=1)
    tk.Entry(item_frame, textvariable=price_var, width=10).grid(row=i, column=2)
    item_rows.append((name_var, qty_var, price_var))

# Forma płatności
tk.Label(root, text="Forma Płatności:", font=("Arial", 10, "bold")).grid(row=9, column=0, sticky="w")
payment_method_listbox = tk.Listbox(root, height=2, exportselection=0)
payment_methods = ["Gotówka", "Karta płatnicza"]
for method in payment_methods:
    payment_method_listbox.insert(tk.END, method)
payment_method_listbox.grid(row=10, column=0, pady=2, padx=10)
payment_method_listbox.selection_set(0)

tk.Button(root, text="Generuj Fakturę", font=("Arial", 10, "bold"), command=validation).grid(row=11, column=0, columnspan=2, pady=20)

tk.Label(root, text="Verion:"+version).grid(row=11, column=2, sticky="w")

root.mainloop()
