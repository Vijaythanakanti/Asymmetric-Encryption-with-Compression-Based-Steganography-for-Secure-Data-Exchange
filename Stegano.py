import math
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
import pytesseract


root=Tk()
root.title("Steganography - Hide a Secret Text Message in an Image")
root.geometry("700x600+150+90")
root.resizable(False,False)
root.configure(bg="#2f4155")

global mse
mse = msgleng =""

def showimage():
    global filename
    filename=filedialog.askopenfilename(initialdir=os.getcwd(),
                                        title='Select Image File',
                                        filetype=(("JPG file", "*.jpg"),
                                                  ("PNG file","*.png"),
                                                  ("All file","*.txt")))
    img=Image.open(filename)
    img=ImageTk.PhotoImage(img)
    lb1.configure(image=img,width=250,height=250)
    lb1.image=img

def save():
    split = os.path.splitext(filename)
    index=len(split)-1
    newfile = split[0] + "_stego"+split[index]
    secret.save(newfile)
    messagebox.showinfo("Save", "Stego Image Saved Successfully")



from rsa_python import rsa
class Cryptography:
    def __init__(self, key_size):
        self.key_size = key_size
        self.key_pair = rsa.generate_key_pair(self.key_size)
        self.public_key, self.private_key = self.key_pair["public"], self.key_pair["private"]
    def encrypt(self, message):
        return rsa.encrypt(message, self.public_key, self.key_pair["modulus"]), self.key_pair["modulus"]
    def decrypt(self, message):
        return rsa.decrypt(message, self.private_key,self.key_pair["modulus"])
    def customDecrypt(self,message,key,n):
        return rsa.decrypt(message, key, n)
    def get_public_key(self):
        return self.public_key
    def get_private_key(self):
        return self.private_key
    def get_key_size(self):
        return self.key_size
obj=Cryptography(1024)


def Hide():
    global secret
    global newfile

    #orginal file
    original_file=filename

    #message

    msg=text1.get(1.0,END)
    msg=msg.replace("\n","|")
    values=obj.encrypt(msg)
    cipher= values[0]
    n=values[1]
    key = str(obj.get_private_key())
    msgcon = cipher + "--" + key + "--" + str(n)
    print("private key\n"+key)
    print("Cipher Text\n"+ cipher)
    print("Messageconcatenation "+msgcon)
    message = msgcon
    msgleng =len(message)
    if len(message) == 1:
        messagebox.showinfo("Hide", "Please enter Text...")
    else:
        secret = lsb.hide(str(filename),message)
        split = os.path.splitext(filename)
        index = len(split) - 1
        newfile = split[0] + "_stego.png"
        secret.save(newfile)

        #Stego Image
        stegano_file=newfile

        # load the images and convert them to grayscale
        imgA = Image.open(original_file).convert('L')
        imgB = Image.open(stegano_file).convert('L')

        print(original_file)
        print(stegano_file)

        # convert the images to numpy arrays
        imgA = np.array(imgA)
        imgB = np.array(imgB)

        # calculate the MSE between the two images
        mse = np.mean((imgA - imgB) ** 2)

        #PSNR Callculation
        if (mse == 0):  # MSE is zero means no noise is present in the signal .
            # Therefore PSNR have no importance.
            return 100
        max_pixel = 255.0
        psnr = 20 * log10(max_pixel / sqrt(mse))

        # Calculate the SSIM
        ssim_value = ssim(imgA, imgB, multichannel=True)

        Label(frame6, text=str(msgleng), bg="#2f4155", font="Times 12 bold", fg="white").place(x=20, y=5)
        Label(frame6, text=str(mse), bg="#2f4155", font="Times 12 bold", fg="white").place(x=100, y=5)
        Label(frame6, text=str(psnr), bg="#2f4155", font="Times 12 bold", fg="white").place(x=300, y=5)
        Label(frame6, text=str(ssim_value), bg="#2f4155", font="Times 12 bold", fg="white").place(x=500, y=5)

        print("MSE: %.2f, SSIM: %.2f" % (mse, ssim_value))

        # Message Box
        messagebox.showinfo("Hide", "Data Hide Successfully")


def Show():
    extension = os.path.splitext(filename)[1]
    print("\n\n\n")
    print(filename)
    if extension == '.png':
        if filename is not None and filename.endswith("_stego.png"):
            clear_message = lsb.reveal(filename)
            emdmsg=clear_message.split("--")
            plain = obj.customDecrypt(emdmsg[0],int(emdmsg[1]),int(emdmsg[2]))
            plain = plain.replace("|","\n")
            text1.delete(1.0,END)
            text1.insert(END,plain)
        else:
            messagebox.showinfo("Message", "The image does not contain hidden text")
    else:
        messagebox.showinfo("Message","Select Only PNG Files..")
#icon
image_icon=PhotoImage(file="favicon.png")
root.iconphoto(False,image_icon)

#logo
logo=PhotoImage(file="logo.png")
Label(root,image=logo,bg="#2f4135").place(x=10,y=0)
Label(root,text="Steganography",bg="#2d4155",fg="white",font="arial 25 bold").place(x=100,y=20)

#first Frame
f=Frame(root,bg="black",width=340, height=280, relief=GROOVE)
f.place(x=10,y=80)

lb1=Label(f,bg="black")
lb1.place(x=40,y=10)

#Secomd Frame
frame2=Frame(root,bd=3,width=340,height=280,bg="white",relief=GROOVE)
frame2.place(x=350,y=80)

text1=Text(frame2,font="Times 20",bg="white",fg="black",relief=GROOVE,wrap=WORD)
text1.place(x=0,y=0,width=320,height=295)

scrollbar1=Scrollbar(frame2)
scrollbar1.place(x=320,y=0,height=300)

scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

#third Frame
frame3=Frame(root,bd=3,bg="#2f4155",width=330, height=100,relief=GROOVE)
frame3.place(x=10,y=370)

Button(frame3,text="Open Image",width=10,height=2,font="Times 14 bold",command=showimage).place(x=20,y=30)
Button(frame3,text="Save Image",width=10,height=2,font="Times 14 bold",command=save).place(x=180,y=30)
Label(frame3,text="Picture, Image, Photo File",bg="#2f4155",fg="yellow").place(x=20,y=5)

#fourth Frame
frame4=Frame(root,bd=3,bg="#2f4155",width=330, height=100,relief=GROOVE)
frame4.place(x=360,y=370)

Button(frame4,text="Hide Data",width=10,height=2,font="Times 14 bold",command=Hide).place(x=20,y=30)
Button(frame4,text="Show Data",width=10,height=2,font="Times 14 bold",command=Show).place(x=180,y=30)
Label(frame4,text="Action",bg="#2f4155",fg="yellow").place(x=20,y=5)

#Fifth Frame
frame5=Frame(root,bd=3,bg="#2f4155",width=680, height=100,relief=GROOVE)
frame5.place(x=10,y=480)
Label(frame5, text="Parametters for RSA", bg="#2f4155", fg="yellow").place(x=20, y=5)
Label(frame5, text="MSG Len", bg="#2f4155", font="Times 12", fg="white").place(x=20, y=30)
Label(frame5, text="MSE", bg="#2f4155", font="Times 12", fg="white").place(x=100, y=30)
Label(frame5, text="PSNR", bg="#2f4155", font="Times 12", fg="white").place(x=300, y=30)
Label(frame5, text="SSIM", bg="#2f4155", font="Times 12", fg="white").place(x=500, y=30)

#Sixth Frame
frame6=Frame(root,bd=2,bg="#2f4155",width=680, height=50,relief=GROOVE)
frame6.place(x=10,y=540)



root.mainloop()
