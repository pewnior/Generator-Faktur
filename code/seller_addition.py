import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

current_path = os.path.dirname(os.path.realpath(__file__))
JSON_FILE = os.path.join(current_path, "sellers.json")

def add_seller():
    
    def save_new_seller():
        new_seller = {
            "name": name_var.get().strip(),
            "sellerp1": sellerp1_var.get().strip(),
            "sellerp2": sellerp2_var.get().strip(),
            "address": adress_var.get().strip(),
            "post": post_var.get().strip(),
            "nip": nip_var.get().strip()
        }

        # Walidacja pól
        if not all(new_seller.values()):
            messagebox.showerror("Błąd", "Wszystkie pola muszą być wypełnione.")
            return
        
        # Walidacja NIP
        if not (new_seller["nip"].isdigit() and len(new_seller["nip"]) == 10):
            messagebox.showerror("Błąd", "NIP musi zawierać dokładnie 10 cyfr.")
            return

        # Wczytanie istniejącego JSON-a lub utworzenie nowego
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {"sellers": []}

        # Dodanie nowego sprzedawcy
        data["sellers"].append(new_seller)

        # Zapis do pliku
        with open(JSON_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        messagebox.showinfo("Sukces", "Nowy sprzedawca został dodany.")
        add_window.destroy()

    # Nowe okno
    add_window = tk.Toplevel()
    add_window.title("Dodaj nowego sprzedawcę")

    # Zmienne
    name_var = tk.StringVar()
    sellerp1_var = tk.StringVar()
    sellerp2_var = tk.StringVar()
    adress_var = tk.StringVar()
    post_var = tk.StringVar()
    nip_var = tk.StringVar()

    # Układ formularza
    fields = [
        ("Nazwa sprzedawcy", name_var),
        ("Nazwa firmy część 1", sellerp1_var),
        ("Nazwa formy część 2", sellerp2_var),
        ("Adres", adress_var),
        ("Kod i poczta", post_var),
        ("NIP", nip_var)
    ]

    for i, (label_text, var) in enumerate(fields):
        ttk.Label(add_window, text=label_text + ":").grid(row=i, column=0, sticky="w", padx=5, pady=2)
        ttk.Entry(add_window, textvariable=var, width=40).grid(row=i, column=1, padx=5, pady=2)

    # Przycisk zapisu
    ttk.Button(add_window, text="Zapisz", command=save_new_seller).grid(row=len(fields), column=0, columnspan=2, pady=10)

    add_window.grab_set()  # Fokus na nowe okno


