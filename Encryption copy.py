import random
import time
import threading
import os
from tkinter import messagebox

import customtkinter

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("400x400")
app.title("OF's Encryption")

def message():
    messagebox.showinfo(
        parent=app,
        title='Warning',
        message='Hello'
    )

def message1():
    messagebox.showwarning(
        parent=app,
        title='Warning',
        message='Keys Do not match'
    )

def message2():
    messagebox.showwarning(
        parent=app,
        title='Warning',
        message='Key needs to 0-255'
    )

def timemessage(elapsedtime):
    messagebox.showinfo(
        parent=app,
        title='Complete',
        message=f"Process complete. It took: {elapsedtime} seconds"
    )

def encryption(key, directory):
    starttime = time.time()
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            if filename == '.DS_Store':
                continue
            
            if os.path.isdir(file_path):
                continue
            
            with open(file_path, 'rb') as file:
                data = file.read()
                
            data = bytearray(data)
            encrypteddata = bytes([value ^ key for value in data])
            
            with open(file_path, 'wb') as file:
                file.write(encrypteddata)

            file_path = '/Users/.../.../...' #create a place for the key to be stored
            with open(file_path, 'w') as file:
                file.write(str(key))
            
    endtime = time.time()
    elapsedtime = endtime - starttime
    timemessage(elapsedtime)
              
def decryption(key, directory):
    starttime = time.time()
    file_path = '/Users/.../.../...' #this is where the key should be stored
    with open(file_path, 'r') as file:
        user_key = int(file.read())
    
    if user_key != key:
        message1()
        return

    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            if filename == '.DS_Store':
                continue
            
            if os.path.isdir(file_path):
                continue
            
            with open(file_path, 'rb') as file:
                data = file.read()
                
            data = bytearray(data)
            decrypted_data = bytes([value ^ key for value in data])
            
            with open(file_path, 'wb') as file:
                file.write(decrypted_data)

    endtime = time.time()
    elapsedtime = endtime - starttime
    timemessage(elapsedtime)
                    
def button_callback():
    global itemnames
    print("Button click", optionmenu_1.get())
    selected_option = optionmenu_1.get()
    key = text_1.get("1.0", "end-1c")
    key = int(key)
    if selected_option == 'Encrypt':
        if key > 0:
            if key <= 255:
                print('Key accepted')
                directory = text_2.get('1.0', 'end-1c')
                directory = str(directory)
                os.chdir(directory)
                if os.path.getsize(directory) == 0:
                    text_2.insert("1.0", "Folder empty or not found")
                else: 
                    itemnames = os.listdir(directory)
                    print('Items found')
                    encryption(key, directory)
                
        
            else:
                message2()
                print('not accepted')
            
        else:
            message2()
            print('not accepted')
        
    elif selected_option == 'Decrypt':
        key = text_1.get("1.0", "end-1c")
        key = int(key)
        if key > 0:
            if key <= 255:
                file_path = '/Users/.../.../...'
                with open(file_path, 'r') as file:
                    user_key = file.read()
                    user_key = int(user_key)
                if user_key == key:
                    directory = text_2.get('1.0', 'end-1c').strip()
                    os.chdir(directory)
                    if os.path.getsize(directory) == 0:
                        text_2.insert("1.0", "Folder empty or not found")
                    else:
                        decryption(key, directory)
                                

                else: 
                    print('Keys do not match')  
                    message1() 
            else:
                message2()
        else:
            message2()  
    else:
        text_1.insert("1.0", "Please choose an, Encrypt or Decrypt.")

def on_option_change(*args):
    selected_option = optionmenu_1.get()
    text_1.delete("1.0", "end")  
    if selected_option == 'Encrypt':
        text_1.insert("1.0", "Please enter a key here (0-255). This will be the key you need to decrypt your files.")
    elif selected_option == 'Decrypt':
        text_1.insert("1.0", "Please enter the key here.")
    else:
        text_1.insert("1.0", "Please choose an option above.")

frame_1 = customtkinter.CTkFrame(master=app)
frame_1.pack(pady=20, padx=60, fill="both", expand=True)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text='Encrypt or Decrpypt')
label_1.pack(pady=10, padx=10)

button_1 = customtkinter.CTkButton(master=frame_1, command=button_callback, text='Start')
button_1.pack(pady=10, padx=10)

optionmenu_1 = customtkinter.CTkOptionMenu(frame_1, values=["Encrypt", "Decrypt"], command=on_option_change)
optionmenu_1.pack(pady=10, padx=10)
optionmenu_1.set("Choose to Encrypt or Decrypt")

text_1 = customtkinter.CTkTextbox(master=frame_1, width=200, height=100)
text_1.pack(pady=10, padx=10)

text_2 = customtkinter.CTkTextbox(master=frame_1, width=200, height=100)
text_2.pack(pady=10, padx=10)
text_2.insert("1.0","Input File Path. eg. /Users/.../.../...")


app.mainloop()
