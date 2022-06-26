from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_dic = {
        website: {
            "email": email,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0 or len(email) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty.")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f" These are the details entered: \n Email: {email}"
                                                              f"\n Password: {password} \n Is it ok to save?")
        if is_ok:
            try:
                with open("data_pass.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data_pass.json", "w") as data_file:
                    json.dump(new_dic, data_file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_dic)
                with open("data_pass.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


def search_password():
    website = website_entry.get()
    # Reading  data
    # new_dict = {new_key:new_value for item in list}
    # new_dict = {new_key:new_value for (key, value) in dict.items()}
    # new_dict = {new_key:new_value for (key, value) in dict.items() if test}
    # new_list = [new_item for item in list]
    # new_list = [new_item for item in list if test]
    try:
        with open("data_pass.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f" Email: {email}\n Password: {password}")
        else:
            messagebox.showinfo(title="Error", message=f" No Data for {website} exists.")


# ---------------------------- UI SETUP -------------------------------
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=27)
website_entry.grid(row=1, column=1, padx=5, pady=5)
website_entry.focus()
email_entry = Entry(width=45)
email_entry.grid(row=2, column=1, columnspan=2, padx=5, pady=5)
email_entry.insert(0, "dheerajjain.dhe@gmail.com")
password_entry = Entry(width=27)
password_entry.grid(row=3, column=1, columnspan=1)

# Buttons
generate_password_button = Button(text="Generate Password", width=14, command=generate_password)
generate_password_button.grid(row=3, column=2, columnspan=1, padx=0, pady=0)
add_button = Button(text="Add", width=38, command=save_password)
add_button.grid(row=4, column=1, columnspan=2, padx=5, pady=10)
search_password_button = Button(text="Search", width=14, command=search_password)
search_password_button.grid(row=1, column=2, columnspan=1, padx=0, pady=0)

window.mainloop()
