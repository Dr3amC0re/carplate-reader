import tkinter as tk
import customtkinter as cst
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog as fd
import matplotlib.pyplot as plt
import pytesseract
import cv2

win = tk.Tk()
win.geometry('900x490+230+130')
win.resizable(0, 0)
win.title('Car Found')

def select_file():
    global filename

    filetypes = (
        ('Photo files', '*.jpg'),
        # ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    
    messagebox.showinfo(
        title='Selected File', 
        message=filename
    )
    
    global profil_photo
    profil_photo = ImageTk.PhotoImage(Image.open(filename).resize((400,265)))
    photo_label.config(image = profil_photo)
    photo_label.config(height = 265, width = 400)
    
    main()

    # print(filename)



def open_img(img_path):
    carplate_img = cv2.imread(img_path)
    carplate_img = cv2.cvtColor(carplate_img, cv2.COLOR_BGR2RGB)
    plt.axis('off')
    plt.imshow(carplate_img)
    # plt.show()

    return carplate_img 

def carplate_extract(image, carplate_haar_cascade):
    carplate_rects = carplate_haar_cascade.detectMultiScale(image, scaleFactor=1.1, minNeighbors=5)

    for x, y, w, h in carplate_rects:
        carplate_img = image[y+15:y+h-10, x+15:x+w-20]

    return carplate_img

def enlarge_img(image, scale_persent):
    width = int(image.shape[1] * scale_persent / 100)
    height = int(image.shape[0] * scale_persent / 100)
    dim = (width, height)
    plt.axis('off')
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    return resized_image


def main():

    carplete_img_rgb = open_img(img_path=filename)

    carplate_haar_cascade = cv2.CascadeClassifier('numDetect\haarcascade_russian_plate_number.xml')

    carplate_extract_img = carplate_extract(carplete_img_rgb, carplate_haar_cascade)
    carplate_extract_img = enlarge_img(carplate_extract_img, 150)
    plt.imshow(carplate_extract_img)
    # plt.show()

    carplate_extract_img_gray = cv2.cvtColor(carplate_extract_img, cv2.COLOR_RGB2GRAY)
    plt.axis('off')
    plt.imshow(carplate_extract_img_gray, cmap='gray')
    # plt.show()



    print('Номер авто: ', pytesseract.image_to_string(
        carplate_extract_img_gray,
        config='--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        )
    car_num.insert(0, pytesseract.image_to_string(
        carplate_extract_img_gray,
        config='--psm 6 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'))
    






    


frm1 = tk.Frame(win, height=55, bg='white')
cst.CTkButton(frm1, text='Faýly saýlamak', width=850, height=35, command=select_file, fg_color='#5ddbff', text_color='white', font=('Arial', 18), hover_color='#23e7eb').pack(pady=10)
frm1.pack(side=tk.TOP, fill=tk.X)



frm2 = tk.Frame(win, height=55, bg='white')


cst.CTkLabel(frm2, text='').pack(pady=1)
cst.CTkLabel(frm2, text='Ulganyň belgesi', font=('Arial', 22),  text_color='black', bg_color='white', width=700).pack()
car_num = cst.CTkEntry(frm2, width=850,  height=35, font=('Arial', 20), fg_color='#5ddbff', text_color='white', border_color='#5ddbff', corner_radius=0, justify='center')
car_num.pack()
cst.CTkLabel(frm2, text='').pack(pady=1)

frm2.pack(side=tk.BOTTOM, fill=tk.X)



frm3 = tk.Frame(win, width=450, bg='white')
frm3.pack_propagate(0)
cst.CTkLabel(frm3, text='').pack(pady=1)
photo_label = tk.Label(frm3, text='')
photo_label.pack(padx=3, pady=5)
frm3.pack(side=tk.LEFT, fill=tk.Y)

frm4 = tk.Frame(win, width=450, bg='white')
frm4.pack_propagate(0)

cst.CTkLabel(frm4, text='').pack(pady=3)

cst.CTkLabel(frm4, text='Ady we familiýasy', font=('Arial', 22), text_color='black', bg_color='white', width=400).pack()
fullname = cst.CTkEntry(frm4, width=400, height=35, font=('Arial', 20), fg_color='#5ddbff', text_color='white', border_color='#5ddbff', corner_radius=0, justify='center')
fullname.pack()

cst.CTkLabel(frm4, text='').pack(pady=8)

cst.CTkLabel(frm4, text='Bellige alnan ýeri', font=('Arial', 22),  text_color='black', bg_color='white', width=400).pack()
welayat = cst.CTkEntry(frm4, width=400,  height=35, font=('Arial', 19), fg_color='#5ddbff', text_color='white', border_color='#5ddbff', corner_radius=0, justify='center')
welayat.pack()

cst.CTkLabel(frm4, text='').pack(pady=8)

cst.CTkLabel(frm4, text='Doglan senesi', font=('Arial', 22),  text_color='black', bg_color='white', width=400).pack()
dob = cst.CTkEntry(frm4, width=400,  height=35, font=('Arial', 20), fg_color='#5ddbff', text_color='white', border_color='#5ddbff', corner_radius=0, justify='center')
dob.pack()



frm4.pack(side=tk.LEFT, fill=tk.Y)




win.mainloop()