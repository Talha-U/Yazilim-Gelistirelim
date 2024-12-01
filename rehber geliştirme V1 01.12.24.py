import tkinter as tk
from tkinter import messagebox
from datetime import datetime

file_path = "rehber.txt"

def load_contacts():
    contacts = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                name, phone, address, created_at, updated_at = line.strip().split(",")
                contacts[name] = {
                    "phone": phone,
                    "address": address,
                    "created_at": created_at,
                    "updated_at": updated_at
                }
    except FileNotFoundError:
        pass
    return contacts

def save_contacts():
    with open(file_path, "w") as file:
        for name, info in contacts.items():
            file.write(f"{name},{info['phone']},{info['address']},{info['created_at']},{info['updated_at']}\n")

contacts = load_contacts()

def add_contact():
    name = name_entry.get()
    phone = phone_entry.get()
    address = address_entry.get()

    if name and phone and address:
        created_at = updated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        contacts[name] = {
            "phone": phone,
            "address": address,
            "created_at": created_at,
            "updated_at": updated_at
        }
        save_contacts()
        messagebox.showinfo("Başarılı", "Kişi başarıyla eklendi!")
        clear_entries()
    else:
        messagebox.showerror("Hata", "İsim, telefon numarası ve adres boş olamaz!")

def update_contact(name):
    updated_phone = phone_entry.get()
    updated_address = address_entry.get()
    if updated_phone and updated_address:
        contacts[name]['phone'] = updated_phone
        contacts[name]['address'] = updated_address
        contacts[name]['updated_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_contacts()
        response = messagebox.askquestion("Doğrulama", "Değişiklikleri kaydetmek istiyor musunuz?")
    if response == 'yes': 
        messagebox.showinfo("Başarılı","bilgiler başarıyla güncellendi!")
        contact_window.destroy()
    else:
        messagebox.showerror("Hata", "Telefon ve adres boş olamaz!")

def open_contact_window(name):
    global contact_window, name_entry, phone_entry, address_entry
    contact_window = tk.Toplevel(root)
    contact_window.title(f"{name} Bilgilerini Düzenle")
    contact_window.geometry("300x300")

    name_label = tk.Label(contact_window, text="İsim:")
    name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    name_entry = tk.Entry(contact_window)
    name_entry.insert(0, name)
    name_entry.grid(row=0, column=1, padx=10, pady=5)

    phone_label = tk.Label(contact_window, text="Telefon Numarası:")
    phone_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    phone_entry = tk.Entry(contact_window)
    phone_entry.insert(0, contacts[name]['phone'])
    phone_entry.grid(row=1, column=1, padx=10, pady=5)

    address_label = tk.Label(contact_window, text="Adres:")
    address_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    address_entry = tk.Entry(contact_window)
    address_entry.insert(0, contacts[name]['address'])
    address_entry.grid(row=2, column=1, padx=10, pady=5)

    save_button = tk.Button(contact_window, text="Kaydet", command=lambda: update_contact(name))
    save_button.grid(row=3, column=0, columnspan=2, pady=10)

def display_contacts():
    display_window = tk.Toplevel(root)
    display_window.title("Kişiler Listesi")
    display_window.geometry("1920x1080")

    header_frame = tk.Frame(display_window)
    header_frame.grid(row=0, column=0, columnspan=6, pady=10, sticky="ew")

    header_label1 = tk.Label(header_frame, text="Sıra No", font=("Arial", 10, "bold"), width=10)
    header_label1.grid(row=0, column=0, padx=10, pady=5)
    header_label2 = tk.Label(header_frame, text="Adı Soyadı", font=("Arial", 10, "bold"), width=20)
    header_label2.grid(row=0, column=1, padx=10, pady=5)
    header_label3 = tk.Label(header_frame, text="Telefon Numarası", font=("Arial", 10, "bold"), width=20)
    header_label3.grid(row=0, column=2, padx=10, pady=5)
    header_label4 = tk.Label(header_frame, text="Adres", font=("Arial", 10, "bold"), width=30)
    header_label4.grid(row=0, column=3, padx=10, pady=5)
    header_label5 = tk.Label(header_frame, text="Eklenme Tarihi", font=("Arial", 10, "bold"), width=20)
    header_label5.grid(row=0, column=4, padx=10, pady=5)

    row = 1
    for idx, (name, info) in enumerate(contacts.items(), 1):
        data_frame = tk.Frame(display_window)
        data_frame.grid(row=row, column=0, columnspan=6, pady=5, sticky="ew")

        seq_label = tk.Label(data_frame, text=idx, font=("Arial", 10), width=10)
        seq_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        name_label = tk.Label(data_frame, text=name, font=("Arial", 10), width=20)
        name_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        phone_label = tk.Label(data_frame, text=info['phone'], font=("Arial", 10), width=20)
        phone_label.grid(row=0, column=2, padx=10, pady=5, sticky="w")
        
        address_label = tk.Label(data_frame, text=info['address'], font=("Arial", 10), width=30)
        address_label.grid(row=0, column=3, padx=10, pady=5, sticky="w")
        
        created_at_label = tk.Label(data_frame, text=info['created_at'], font=("Arial", 10), width=20)
        created_at_label.grid(row=0, column=4, padx=10, pady=5, sticky="w")

        update_button = tk.Button(data_frame, text="Güncelle", command=lambda name=name: open_contact_window(name))
        update_button.grid(row=0, column=5, padx=10, pady=5)
        
        row += 1

    total_label = tk.Label(display_window, text=f"Toplam Kişi Sayısı: {len(contacts)}", font=("Arial", 12, "bold"))
    total_label.grid(row=row, column=0, columnspan=6, pady=10, sticky="ew")

def search_contact():
    name = name_entry.get()
    if name in contacts:
        open_contact_window(name)
    else:
        messagebox.showerror("Hata", "Kişi bulunamadı!")

def remove_contact():
    name = name_entry.get()
    if name in contacts:
        del contacts[name]
        save_contacts()
        messagebox.showinfo("Başarılı", f"'{name}' kişisi silindi.")
        clear_entries()
    else:
        messagebox.showerror("Hata", "Listede böyle bir kişi bulunmamakta")

def clear_entries():
    name_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)

root = tk.Tk()
root.title("Telefon Rehberi")
root.geometry("500x300")
root.configure(bg="#f0f0f0")

name_label = tk.Label(root, text="Adı Soyadı:", bg="#f0f0f0", font=("Arial", 10))
name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1, padx=10, pady=5)

phone_label = tk.Label(root, text="Telefon Numarası:", bg="#f0f0f0", font=("Arial", 10))
phone_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
phone_entry = tk.Entry(root)
phone_entry.grid(row=1, column=1, padx=10, pady=5)

address_label = tk.Label(root, text="Adres:", bg="#f0f0f0", font=("Arial", 10))
address_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
address_entry = tk.Entry(root)
address_entry.grid(row=2, column=1, padx=10, pady=5)

add_button = tk.Button(root, text="Kişiye Ekle", command=add_contact, bg="#4CAF50", fg="white")
add_button.grid(row=3, column=0, padx=10, pady=10, sticky="ew")

search_button = tk.Button(root, text="Kişi Ara", command=search_contact, bg="#008CBA", fg="white")
search_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

display_button = tk.Button(root, text="Kişiler Listesi", command=display_contacts, bg="#FF5722", fg="white")
display_button.grid(row=3, column=2, padx=10, pady=10, sticky="ew")

remove_button = tk.Button(root, text="Kişiyi Sil", command=remove_contact, bg="#f44336", fg="white")
remove_button.grid(row=3, column=3, padx=10, pady=10, sticky="ew")

root.mainloop()
