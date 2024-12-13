import random
import string
import json
import pyperclip
from tkinter import *
from tkinter import messagebox

# Constants for styling
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    """Generates a random password with letters, digits, and symbols."""
    letters = string.ascii_letters
    digits = string.digits
    symbols = string.punctuation

    password_entry.delete(0, END)

    # Combining all possible characters
    all_characters = [char for char in letters + digits + symbols]
    password = ""

    # Generating a 16-character password
    for _ in range(16):
        password += random.choice(all_characters)

    password_entry.insert(0, password)
    pyperclip.copy(password)  # Copy the password to clipboard


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    """Saves the website, email, and password in a JSON file."""
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    # Data validation: Ensure no fields are empty
    if len(website) == 0 or len(password) == 0 or email == "@gmail.com":
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty.")
        return

    data = {
        website.lower(): {
            "email": email,
            "password": password
        }
    }

    # Attempt to read the existing data from the JSON file
    try:
        with open("data_password.json", mode="r") as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = {}
    except FileNotFoundError:
        existing_data = {}

    # Update the data with the new entry
    existing_data.update(data)

    # Save the updated data back to the file
    with open("data_password.json", mode="w") as file:
        json.dump(existing_data, file, indent=4)

    # Show success message and clear the input fields
    messagebox.showinfo(title=website, message="Your password has been saved.")
    website_entry.delete(0, END)
    password_entry.delete(0, END)
    email_entry.delete(0, END)
    email_entry.insert(0, "@gmail.com")


# ----------------------------- SEARCH PASSWORD -------------------------------- #
def search_password():
    """Searches for the password of a given website."""
    website = website_entry.get().lower()

    try:
        with open("data_password.json", "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messagebox.showerror(title="Error", message="No data file found.")
        return

    # Check if the website exists in the data
    if website in data:
        email = data[website]["email"]
        password = data[website]["password"]
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
    else:
        messagebox.showinfo(title=website, message=f"{website} not found in the database.")

    website_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=70, pady=30)

# --------------------- Add Image ---------------------------------- #
image_canvas = Canvas(window, width=200, height=200)
logo_image = PhotoImage(file="logo.png")
image_canvas.create_image(100, 100, image=logo_image)
image_canvas.grid(column=1, row=0)

# ----------------- Create Labels --------------------------------- #
website_label = Label(text="Website:", font=("italic", 10, "bold"))
website_label.grid(column=0, row=1)

email_label = Label(text="Email/Username:", font=("italic", 10, "bold"))
email_label.grid(column=0, row=2)

password_label = Label(text="Password:", font=("italic", 10, "bold"))
password_label.grid(column=0, row=3)

# ---------------------- Create Input Boxes ----------------------------- #
website_entry = Entry(window, width=50)
website_entry.grid(row=1, column=1)
website_entry.focus()

email_entry = Entry(window, width=50)
email_entry.grid(row=2, column=1)
email_entry.insert(0, "@gmail.com")

password_entry = Entry(window, width=50)
password_entry.grid(row=3, column=1)

# ---------------------- Create Buttons -------------------------- #
generate_password_button = Button(
    window, text="Generate Password", width=22, bg=GREEN, font=("Arial", 9, "bold"), command=generate_password
)
generate_password_button.grid(row=3, column=2)

space = Label(window, text="")
space.grid(row=5, column=1)

add_button = Button(
    window, text="Add", width=35, bg="red", font=("Arial", 10, "bold"), command=save_password
)
add_button.grid(row=6, column=1)

search_button = Button(
    window, text="Search", width=22, bg="blue", font=("Arial", 9, "bold"), fg="white", command=search_password
)
search_button.grid(column=2, row=1)

window.mainloop()



