import os 
import sqlite3
import bcrypt
import customtkinter
import time
from tkinter import messagebox
import threading

customtkinter.set_appearance_mode("dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

app = customtkinter.CTk()
app.geometry("300x400")
app.title("Login")
app.resizable(False,False)
app.eval('tk::PlaceWindow . centre')

font1 = ('Helvetica',25,'bold')
font2 = ('Arial',17,'bold')
font3 = ('Arial',13,'bold')
font4 = ('Arial',13,'bold','underline')

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

cursor.execute('''
    create table if not exists users (
        username text not null,
        password text not null)''')

def login():
    print("Login Page")
    #remember.place(x=100,y=165)
    button_1.place(x=70,y=250)
    button_2.place(x=900,y=2500)
    text.place(x=30,y=200)
    text2.place(x=500,y=2005)
    entry_3.place(x=900,y=1650)
    login_button.place(x=2000,y=2050)
    signup_button.place(x=180,y=200)
    app.title('Login')

def message1():
    messagebox.showwarning(
        parent=app,
        title='Warning',
        message='Passwords do not match'
    )

def message2():
    messagebox.showwarning(
        parent=app,
        title='Warning',
        message='Password must be >= 6 characters'
    )

def message3():
    messagebox.showwarning(
        parent=app,
        title='Warning',
        message='Please fill in username and password'
    )

def message4():
    messagebox.showwarning(
        parent=app,
        title='Warning',
        message='Keys Do not match'
    )

def message5():
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

def warning():
    messagebox.showinfo(
        parent=app,
        title='Warning',
        message=f"Please remember your key, if lost you will loose your files"
    )

def go():
    print('Sign up click')
    User = entry_1.get()
    pass1 = entry_2.get()
    pass2 = entry_3.get()
    if User != '' and pass1 != '' and pass2 != '':
        str(pass1)
        str(pass2)
        print(pass1)
        print(pass2)
        if pass1 == pass2:
            if len(pass1) >= 6:
                print('Password meets all requirements')
                cursor.execute('select username from users where username=?', [User])
                if cursor.fetchone() is not None:
                    messagebox.showerror('Error','Username already exists.')
                else:
                    encodedpass = pass1.encode('utf-8')
                    hashedpass = bcrypt.hashpw(encodedpass, bcrypt.gensalt())
                    print(hashedpass)
                    cursor.execute('insert into users values (?,?)', [User, hashedpass])
                    connection.commit()
                    messagebox.showinfo('Success', 'Account has been created.')

            else:
                message2()
        else:
            message1()
    else:
        message3()

def lgo():
    print('Login click')
    User = entry_1.get()
    pass1 = entry_2.get()
    if User != '' and pass1 != '':
        cursor.execute('select password from users where username=?', [User])
        result = cursor.fetchone()
        if result:
            if bcrypt.checkpw(pass1.encode('utf-8'), result[0]):
                messagebox.showinfo(parent=app,
                                    title='Success',
                                    message='Logged in successfully'
                                )
                button_1.place(x=900,y=2500)
                button_2.place(x=900,y=2500)
                text.place(x=5000,y=20000)
                text2.place(x=500,y=2050)
                entry_3.place(x=900,y=1650)
                login_button.place(x=2000,y=2050)
                signup_button.place(x=2000,y=2000)
                entry_1.place(x=900,y=750)
                entry_2.place(x=900,y=1200)
                app.title('Encryption')
                encryptionapp()

                #app.destroy()
                ##from Encryption import app1
                #app1.mainloop()

            else:
                messagebox.showerror('Error', 'Invalid Password')
        else:
            messagebox.showerror('Error', 'Invalid Username')
    else:
        messagebox.showerror('Error','Username does not exist.')

def encryptionapp():
    warning()
    start.place(x=70, y=250)
    selection.place(x=30, y=60)
    keyyy.place(x=30, y=130)
    filepath.place(x=30, y=170)

def button_callback():
    global itemnames
    print("Button click", selection.get())
    selected_option = selection.get()
    key = keyyy.get("1.0", "end-1c")
    key = int(key)
    if selected_option == 'Encrypt':
        if key > 0:
            if key <= 255:
                print('Key accepted')
                directory = filepath.get('1.0', 'end-1c')
                directory = str(directory)
                os.chdir(directory)
                if os.path.getsize(directory) == 0:
                    filepath.insert("1.0", "Folder empty or not found")
                else: 
                    itemnames = os.listdir(directory)
                    print('Items found')
                    encryption(key, directory)
                
        
            else:
                message5()
                print('not accepted')
            
        else:
            message5()
            print('not accepted')
        
    elif selected_option == 'Decrypt':
        key = keyyy.get("1.0", "end-1c")
        key = int(key)
        if key > 0:
            if key <= 255:
                #file_path = '/Users/.../Desktop/Key/...'
                #with open(file_path, 'r') as file:
                    #user_key = file.read()
                    #user_key = int(user_key)
                #if user_key == key:
                directory = filepath.get('1.0', 'end-1c').strip()
                os.chdir(directory)
                if os.path.getsize(directory) == 0:
                    filepath.insert("1.0", "Folder empty or not found")
                else:
                    encryption(key, directory)
                                

                #else: 
                    #print('Keys do not match')  
                    #message4() 
            else:
                message5()
        else:
            message5()  
    else:
        keyyy.insert("1.0", "Please choose an, Encrypt or Decrypt.")

def encryption(key, directory):
    starttime = time.time()
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_size = os.path.getsize(file_path)
            num_threads = 7
            chunk_size = file_size // num_threads
            threads = []
            for i in range(num_threads):
                start = i * chunk_size
                end = start + chunk_size if i < num_threads - 1 else file_size
                t = threading.Thread(target=encrypt_chunk, args=(key, file_path, start, end))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
            
            
            #if filename == '.DS_Store':
            #    continue
            
            #if os.path.isdir(file_path):
            #    continue
            
            #with open(file_path, 'rb') as file:
            #    data = file.read()
                
            #data = bytearray(data)
            #encrypteddata = bytes([value ^ key for value in data])
            
            #with open(file_path, 'wb') as file:
            #    file.write(encrypteddata)

            #file_path = '/Users/.../Desktop/Key/...'
            #with open(file_path, 'w') as file:
                #file.write(str(key))
            
    endtime = time.time()
    elapsedtime = endtime - starttime
    timemessage(elapsedtime)
    
def encrypt_chunk(key, file_path, start, end):
    with open(file_path, 'rb+') as file:
        file.seek(start)
        data = file.read(end - start)
        encrypted_data = bytearray([value ^ key for value in data])
        file.seek(start)
        file.write(encrypted_data)

def decryption(key, directory):
    starttime = time.time()
    #file_path = '/Users/.../Desktop/Key/...'
    #with open(file_path, 'r') as file:
        #user_key = int(file.read())
    
    #if user_key != key:
        #message4()
        #return

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

def signup():
    print("Sign up page")
    #remember.place(x=1000,y=1650)
    button_1.place(x=900,y=2500)
    button_2.place(x=70,y=250)
    text.place(x=500,y=2000)
    text2.place(x=30,y=205)
    entry_3.place(x=70,y=165)
    login_button.place(x=180,y=205)
    signup_button.place(x=2000,y=2000)
    app.title('Sign up')

def on_option_change(*args):
    selected_option = selection.get()
    keyyy.delete("1.0", "end")  
    if selected_option == 'Encrypt':
        selection.place(x=70, y=60)
        keyyy.configure(width=210, height=62)
        keyyy.place(x=30, y=100)
        keyyy.insert("1.0", "Please enter key here (0-255). This will be the key you need to decrypt your files.")
    elif selected_option == 'Decrypt':
        selection.place(x=70, y=60)
        keyyy.configure(width=210, height=62)
        keyyy.place(x=30, y=100)
        keyyy.insert("1.0", "Please enter the key here.")
    else:
        keyyy.insert("1.0", "Please choose an option above.")

frame_1 = customtkinter.CTkFrame(master=app, width=270, height=350)
frame_1.place(x=15,y=20)

label_1 = customtkinter.CTkLabel(master=frame_1, justify=customtkinter.LEFT, text='')
label_1.place(x=0,y=0)

entry_1 = customtkinter.CTkEntry(master=frame_1, placeholder_text="User Name")
entry_1.place(x=70,y=75)

entry_2 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Password")
entry_2.place(x=70,y=120)

entry_3 = customtkinter.CTkEntry(master=frame_1, placeholder_text="Confirm Password")
entry_3.place(x=1000, y=1650)

button_1 = customtkinter.CTkButton(master=frame_1, command=lgo, text='Login')
button_1.place(x=70,y=250)

button_2 = customtkinter.CTkButton(master=frame_1, command=go, text='Sign up')
button_2.place(x=900,y=2500)

text = customtkinter.CTkLabel(master=frame_1, text="Don't have an account? ")
text.place(x=30,y=200)

text2 = customtkinter.CTkLabel(master=frame_1, text="Password must be > 6.")
text2.place(x=500,y=2000)

signup_button = customtkinter.CTkButton(frame_1, text="Sign up", command=signup, font=font4, fg_color='transparent', text_color='#fff' , bg_color='transparent', width=40)
signup_button.place(x=180, y=200)

login_button = customtkinter.CTkButton(frame_1, text="Login Page", command=login, font=font4, fg_color='transparent', text_color='#fff' , bg_color='transparent', width=40)
login_button.place(x=2000, y=2000)

start = customtkinter.CTkButton(master=frame_1, command=button_callback, text='Start')
start.place(x=1000, y=1000)

selection = customtkinter.CTkOptionMenu(frame_1, values=["Encrypt", "Decrypt"], command=on_option_change)
selection.place(x=1000, y=1000)
selection.set("Choose to Encrypt or Decrypt")

keyyy = customtkinter.CTkTextbox(master=frame_1, width=210, height=30)
keyyy.insert("1.0", "Please choose an option")
keyyy.place(x=1000, y=1000)

filepath = customtkinter.CTkTextbox(master=frame_1, width=210, height=68)
filepath.place(x=1000, y=1000)
filepath.insert("1.0","Input File Path. eg. /Users/.../Desktop/Files")

app.mainloop()

connection.close()