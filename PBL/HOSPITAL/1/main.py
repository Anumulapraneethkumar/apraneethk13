import os
from pathlib import Path
from tkinter import *
from tkinter import messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageDraw, ImageFont, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
import qrcode

# ------------------------------------------------------------
# Paths and Setup
# ------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
DATA = BASE_DIR / "data"
IMAGES = BASE_DIR / "images"

DATA.mkdir(exist_ok=True)
IMAGES.mkdir(exist_ok=True)

# ------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------
def make_png(path, text, size=(420, 140), bgcolor=(8, 77, 137)):
    """Create a placeholder PNG image with centered text (Pillow >=10 compatible)."""
    from PIL import Image, ImageDraw, ImageFont

    img = Image.new("RGB", size, bgcolor)
    draw = ImageDraw.Draw(img)
    try:
        # use a nicer truetype font if available
        font = ImageFont.truetype("arial.ttf", 32)
    except:
        font = ImageFont.load_default()

    # use textbbox instead of deprecated textsize
    bbox = draw.textbbox((0, 0), text, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((size[0] - w) / 2, (size[1] - h) / 2), text, fill=(255, 255, 255), font=font)
    img.save(path)

# Generate a default logo if not already present
logo_path = IMAGES / "logo.png"
if not logo_path.exists():
    make_png(logo_path, "Super Multispeciality\nHospital", size=(420, 140), bgcolor=(8, 77, 137))

# ------------------------------------------------------------
# Simple Excel-based Data Initialization
# ------------------------------------------------------------
patients_file = DATA / "patients.xlsx"
if not patients_file.exists():
    df = pd.DataFrame([
        {"ID": 1, "Name": "Akbar", "Age": 35, "Gender": "Male", "Visits": 3},
        {"ID": 2, "Name": "Priya", "Age": 29, "Gender": "Female", "Visits": 5},
    ])
    df.to_excel(patients_file, index=False)

# ------------------------------------------------------------
# Dashboard Windows
# ------------------------------------------------------------
def open_dashboard(role):
    dash = tb.Window(themename="superhero")
    dash.title(f"{role} Dashboard - Super Multispeciality Hospital")
    dash.geometry("1000x600")

    tb.Label(dash, text=f"{role} Dashboard", font=("Helvetica", 24, "bold")).pack(pady=20)

    if role.lower() == "admin":
        tb.Button(dash, text="View Patient Records", bootstyle=SUCCESS, command=show_patients).pack(pady=10)
        tb.Button(dash, text="Analytics (Patient Visits Graph)", bootstyle=INFO, command=show_graph).pack(pady=10)
    elif role.lower() == "receptionist":
        tb.Button(dash, text="Add / Update Patient Data", bootstyle=PRIMARY, command=add_patient).pack(pady=10)
        tb.Button(dash, text="Generate Patient QR Code", bootstyle=WARNING, command=generate_qr).pack(pady=10)
    elif role.lower() == "doctor":
        tb.Label(dash, text="Doctor's Appointments & Reports Section", font=("Helvetica", 14)).pack(pady=30)
    elif role.lower() == "pharmacy":
        tb.Label(dash, text="Pharmacy Billing and Inventory Management", font=("Helvetica", 14)).pack(pady=30)
    elif role.lower() == "lab":
        tb.Label(dash, text="Lab Test Reports & Uploads", font=("Helvetica", 14)).pack(pady=30)

    tb.Button(dash, text="Logout", bootstyle=DANGER, command=dash.destroy).pack(side=BOTTOM, pady=20)
    dash.mainloop()

# ------------------------------------------------------------
# Functions for Dashboards
# ------------------------------------------------------------
def show_patients():
    df = pd.read_excel(patients_file)
    top = Toplevel()
    top.title("Patient Records")
    tb.Label(top, text="Patient Data", font=("Helvetica", 16, "bold")).pack(pady=10)
    text = Text(top, width=70, height=15)
    text.pack(padx=10, pady=10)
    text.insert(END, df.to_string(index=False))

def show_graph():
    df = pd.read_excel(patients_file)
    plt.figure(figsize=(6, 4))
    plt.bar(df["Name"], df["Visits"])
    plt.title("Patient Visit Frequency")
    plt.xlabel("Patient")
    plt.ylabel("No. of Visits")
    plt.tight_layout()
    plt.show()

def add_patient():
    def save_patient():
        name, age, gender = name_var.get(), age_var.get(), gender_var.get()
        if not name or not age:
            messagebox.showerror("Error", "Please enter all fields")
            return
        df = pd.read_excel(patients_file)
        new_id = df["ID"].max() + 1
        new_row = {"ID": new_id, "Name": name, "Age": int(age), "Gender": gender, "Visits": 1}
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_excel(patients_file, index=False)
        messagebox.showinfo("Success", f"Patient {name} added successfully!")
        win.destroy()

    win = Toplevel()
    win.title("Add Patient")
    name_var, age_var, gender_var = StringVar(), StringVar(), StringVar()

    tb.Label(win, text="Patient Name:").grid(row=0, column=0, padx=10, pady=5)
    tb.Entry(win, textvariable=name_var).grid(row=0, column=1, padx=10, pady=5)
    tb.Label(win, text="Age:").grid(row=1, column=0, padx=10, pady=5)
    tb.Entry(win, textvariable=age_var).grid(row=1, column=1, padx=10, pady=5)
    tb.Label(win, text="Gender:").grid(row=2, column=0, padx=10, pady=5)
    tb.Combobox(win, textvariable=gender_var, values=["Male", "Female", "Other"]).grid(row=2, column=1, padx=10, pady=5)

    tb.Button(win, text="Save", bootstyle=SUCCESS, command=save_patient).grid(row=3, column=0, columnspan=2, pady=10)

def generate_qr():
    df = pd.read_excel(patients_file)
    patient_names = df["Name"].tolist()

    def create_qr():
        selected = combo.get()
        if not selected:
            messagebox.showerror("Error", "Select a patient")
            return
        qr_img = qrcode.make(f"Patient: {selected}")
        save_path = IMAGES / f"{selected}_qr.png"
        qr_img.save(save_path)
        messagebox.showinfo("Success", f"QR Code saved to {save_path}")

    qr_win = Toplevel()
    qr_win.title("Generate QR")
    tb.Label(qr_win, text="Select Patient:").pack(pady=5)
    combo = tb.Combobox(qr_win, values=patient_names)
    combo.pack(pady=5)
    tb.Button(qr_win, text="Generate QR", bootstyle=SUCCESS, command=create_qr).pack(pady=10)

# ------------------------------------------------------------
# Login Screen
# ------------------------------------------------------------
def login_screen():
    root = tb.Window(themename="cosmo")
    root.title("Super Multispeciality Hospital - Login")
    root.geometry("500x600")

    logo_img = ImageTk.PhotoImage(Image.open(logo_path))
    tb.Label(root, image=logo_img).pack(pady=20)

    tb.Label(root, text="Select Role", font=("Helvetica", 18, "bold")).pack(pady=10)
    roles = ["Admin", "Doctor", "Receptionist", "Pharmacy", "Lab"]
    for r in roles:
        tb.Button(root, text=f"Login as {r}", bootstyle=PRIMARY, width=25,
                  command=lambda role=r: [root.destroy(), open_dashboard(role)]).pack(pady=10)

    tb.Label(root, text="© Super Multispeciality Hospital 2025", font=("Helvetica", 10)).pack(side=BOTTOM, pady=10)

    root.mainloop()

# ------------------------------------------------------------
# Start Application
# ------------------------------------------------------------
if __name__ == "__main__":
    login_screen()
