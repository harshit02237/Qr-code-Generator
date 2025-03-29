import qrcode
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from pyvirtualdisplay import Display

# Start a virtual display (required for Render)
display = Display(visible=False, size=(800, 600))
display.start()

# Function to Generate QR Code
def generate_qr():
    upi_id = upi_entry.get().strip()
    amount = amount_entry.get().strip()

    if not upi_id or not amount:
        messagebox.showerror("Error", "Please enter both UPI ID and Amount.")
        return

    try:
        float(amount)  # Validate amount as a number
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid amount.")
        return

    # UPI Payment URL (Works for all apps)
    upi_url = f"upi://pay?pa={upi_id}&pn=Recipient%20Name&mc=1234&am={amount}&cu=INR"

    # Generate and save the QR code
    qr = qrcode.make(upi_url)
    qr.save("UPI_QR.png")

    # Convert QR code to ImageTk format
    qr_img = Image.open("UPI_QR.png")
    qr_img = qr_img.resize((200, 200))  # Resize for UI
    qr_img = ImageTk.PhotoImage(qr_img)

    # Display QR Code
    qr_label.config(image=qr_img)
    qr_label.image = qr_img  # Keep reference to avoid garbage collection

# Create Main Window
root = tk.Tk()
root.title("UPI QR Code Generator")
root.geometry("400x500")
root.configure(bg="#222")  # Dark background

# Title Label
tk.Label(root, text="UPI QR Code Generator", font=("Arial", 16, "bold"), bg="#222", fg="white").pack(pady=10)

# UPI ID Entry
tk.Label(root, text="Enter Your UPI ID:", font=("Arial", 12), bg="#222", fg="white").pack()
upi_entry = tk.Entry(root, font=("Arial", 12), bg="#333", fg="white", bd=2, relief="flat")
upi_entry.pack(pady=5, ipadx=10, ipady=5)

# Amount Entry
tk.Label(root, text="Enter Amount:", font=("Arial", 12), bg="#222", fg="white").pack()
amount_entry = tk.Entry(root, font=("Arial", 12), bg="#333", fg="white", bd=2, relief="flat")
amount_entry.pack(pady=5, ipadx=10, ipady=5)

# Generate Button with Modern Styling
generate_btn = tk.Button(root, text="Generate QR Code", font=("Arial", 12, "bold"), bg="#ff9800", fg="white",
                         relief="flat", padx=10, pady=5, command=generate_qr)
generate_btn.pack(pady=15)

# QR Code Display Label
qr_label = tk.Label(root, bg="#222")
qr_label.pack(pady=10)

# Run GUI
root.mainloop()

# Stop the virtual display when done
display.stop()
