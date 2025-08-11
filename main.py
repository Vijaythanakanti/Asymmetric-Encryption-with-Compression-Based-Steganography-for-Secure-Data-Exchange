from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os
from stegano import lsb
from tkinter import messagebox
from math import log10, sqrt
import numpy as np 
from skimage.metrics import structural_similarity as ssim
from Cryptography import Cryptography
import Huffman as hff
import base64
import rsa

root = Tk()
root.title("Secure Transmission - Hide Encrypted Data in Image")
root.geometry("720x620+150+90")
root.resizable(False, False)
root.configure(bg="#1e1e2f")  # Darker background for modern look

obj = Cryptography(1024)

# === Functions ===
def showimage():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title='Select Image File',
                                          filetype=(("JPG file", "*.jpg"),
                                                    ("PNG file", "*.png"),
                                                    ("All file", "*.txt")))
    img = Image.open(filename)
    img = ImageTk.PhotoImage(img)
    lb1.configure(image=img, width=250, height=250)
    lb1.image = img

def save():
    split = os.path.splitext(filename)
    newfile = split[0] + "_stego.png"
    secret.save(newfile)
    messagebox.showinfo("Save", "Stego Image Saved Successfully")

def Hide():
    global secret
    msg = text1.get(1.0, END).replace("\n", "|")
    cipher, n = obj.encrypt(msg)
    cipher_b64 = base64.b64encode(cipher).decode('utf-8')
    
    # Get private key components
    private_key = obj.get_private_key()
    d = private_key.d  # Private exponent
    p = private_key.p  # First prime factor
    q = private_key.q  # Second prime factor
    
    # Format the message with all necessary key components
    msgcon = cipher_b64 + "--" + str(d) + "--" + str(n) + "--" + str(p) + "--" + str(q)

    if len(msgcon) == 1:
        messagebox.showinfo("Hide", "Please enter Text...")
    else:
        secret = lsb.hide(str(filename), msgcon)
        messagebox.showinfo("Hide", "Data Hide Successfully")

    split = os.path.splitext(filename)
    newfile = split[0] + "_stego.png"
    secret.save(newfile)

    # Quality metrics
    imgA = Image.open(filename).convert('L')
    imgB = Image.open(newfile).convert('L')
    imgA = np.array(imgA)
    imgB = np.array(imgB)

    mse = np.mean((imgA - imgB) ** 2)
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse)) if mse != 0 else 100
    ssim_value = ssim(imgA, imgB, channel_axis=None)

    Label(frame6, text=str(len(msgcon)), bg="#1e1e2f", font="Helvetica 12 bold", fg="white").place(x=20, y=5)
    Label(frame6, text=f"{mse:.2f}", bg="#1e1e2f", font="Helvetica 12 bold", fg="white").place(x=100, y=5)
    Label(frame6, text=f"{psnr:.2f}", bg="#1e1e2f", font="Helvetica 12 bold", fg="white").place(x=300, y=5)
    Label(frame6, text=f"{ssim_value:.2f}", bg="#1e1e2f", font="Helvetica 12 bold", fg="white").place(x=500, y=5)

def Show():
    try:
        # Get the steganographic image path
        stego_path = filedialog.askopenfilename(initialdir=os.getcwd(),
                                               title='Select Stego Image',
                                               filetype=(("PNG file", "*.png"),
                                                       ("All file", "*.*")))
        if not stego_path:
            return
            
        # Extract the hidden message
        hidden_message = lsb.reveal(stego_path)
        if not hidden_message:
            messagebox.showerror("Error", "No hidden message found in the image")
            return
            
        # Split the message into its components
        parts = hidden_message.split("--")
        if len(parts) != 5:  # We now expect 5 parts: cipher, d, n, p, q
            messagebox.showerror("Error", "Invalid message format")
            return
            
        # Decrypt the message
        cipher = base64.b64decode(parts[0].encode('utf-8'))
        d = int(parts[1])  # Private exponent
        n = int(parts[2])  # Modulus
        p = int(parts[3])  # First prime factor
        q = int(parts[4])  # Second prime factor
        
        # Create a temporary private key for decryption with all components
        temp_private_key = rsa.PrivateKey(n, 65537, d, p, q)
        plain = rsa.decrypt(cipher, temp_private_key).decode('utf-8')
        plain = plain.replace("|", "\n")
        
        # Display the decrypted message
        text1.delete(1.0, END)
        text1.insert(END, plain)
        messagebox.showinfo("Success", "Message decrypted successfully!")
        
    except Exception as e:
        messagebox.showerror("Error", f"Decryption failed: {str(e)}")

# === GUI Elements ===
image_icon = PhotoImage(file="favicon.png")
root.iconphoto(False, image_icon)

logo = PhotoImage(file="logo.png")
Label(root, image=logo, bg="#1e1e2f").place(x=10, y=0)
Label(root, text="Secure Transmission", bg="#1e1e2f", fg="#00ffff", font="Helvetica 24 bold").place(x=120, y=20)

# First Frame - Image Viewer
f = Frame(root, bg="#333", width=340, height=280)
f.place(x=10, y=80)
lb1 = Label(f, bg="#333")
lb1.place(x=40, y=10)

# Second Frame - Text Entry
frame2 = Frame(root, bd=3, width=340, height=280, bg="#f7f7f7")
frame2.place(x=360, y=80)
text1 = Text(frame2, font="Helvetica 14", bg="white", fg="black", wrap=WORD)
text1.place(x=0, y=0, width=320, height=295)
scrollbar1 = Scrollbar(frame2)
scrollbar1.place(x=320, y=0, height=300)
scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

# Third Frame - Open/Save Buttons
frame3 = Frame(root, bd=3, bg="#1e1e2f", width=330, height=100)
frame3.place(x=10, y=370)
Label(frame3, text="Image Options", bg="#1e1e2f", fg="orange", font="Helvetica 12 bold").place(x=20, y=5)
Button(frame3, text="Open Image", width=12, height=2, bg="#5dade2", fg="white", font="Helvetica 12 bold", command=showimage).place(x=20, y=30)
Button(frame3, text="Save Image", width=12, height=2, bg="#58d68d", fg="white", font="Helvetica 12 bold", command=save).place(x=180, y=30)

# Fourth Frame - Hide/Show Buttons
frame4 = Frame(root, bd=3, bg="#1e1e2f", width=330, height=100)
frame4.place(x=360, y=370)
Label(frame4, text="Steganography Tools", bg="#1e1e2f", fg="orange", font="Helvetica 12 bold").place(x=20, y=5)
Button(frame4, text="Hide Data", width=12, height=2, bg="#f39c12", fg="white", font="Helvetica 12 bold", command=Hide).place(x=20, y=30)
Button(frame4, text="Show Data", width=12, height=2, bg="#e74c3c", fg="white", font="Helvetica 12 bold", command=Show).place(x=180, y=30)

# Fifth Frame - Output Info
frame5 = Frame(root, bd=3, bg="#1e1e2f", width=680, height=100)
frame5.place(x=10, y=480)
Label(frame5, text="Image Quality Metrics", bg="#1e1e2f", fg="orange", font="Helvetica 12 bold").place(x=20, y=5)
Label(frame5, text="Msg Len", bg="#1e1e2f", fg="white", font="Helvetica 12").place(x=20, y=30)
Label(frame5, text="MSE", bg="#1e1e2f", fg="white", font="Helvetica 12").place(x=100, y=30)
Label(frame5, text="PSNR", bg="#1e1e2f", fg="white", font="Helvetica 12").place(x=300, y=30)
Label(frame5, text="SSIM", bg="#1e1e2f", fg="white", font="Helvetica 12").place(x=500, y=30)

# Sixth Frame - Dynamic Results
frame6 = Frame(root, bd=2, bg="#1e1e2f", width=680, height=50)
frame6.place(x=10, y=540)

root.mainloop()
