from tkinter import *
from tkinter import ttk
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import filedialog
from math import sqrt
import platform
import psutil

# brightness
import screen_brightness_control as pct

# audio
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# weather
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from datetime import datetime
import requests
import pytz

# clock
from time import strftime

# calender
from tkcalendar import *

# open google
import pyautogui
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

from googletrans import Translator

import subprocess
import webbrowser as wb
import random

import mysql.connector

root = Tk()
root.title('Mac-soft Tool')
root.geometry("850x500+300+170")
root.resizable(False, False)
root.configure(bg='#292e2e')

# icon
image_icon = PhotoImage(file="Image/icon.png")
root.iconphoto(False, image_icon)

Body = Frame(root, width=900, height=600, bg="#d6d6d6")
Body.pack(pady=20, padx=20)

# ----------------------------
LHS = Frame(Body, width=310, height=435, bg='#f4f5f5',
            highlightbackground="#adacb1", highlightthickness=1)
LHS.place(x=10, y=20)

# logo
photo = PhotoImage(file="Image/laptop.png")
myimage = Label(LHS, image=photo, background="#f4f5f5")
myimage.place(x=2, y=10)

my_system = platform.uname()
l1 = Label(LHS, text=my_system.node, bg="#f4f5f5", font=(
    "Acumin Variable Concept", 15, 'bold'), justify="center")
l1.place(x=20, y=200)

l2 = Label(LHS, text=f"Version:{my_system.version}", bg="#f4f5f5", font=(
    "Acumin Variable Concept", 8), justify="center")
l2.place(x=20, y=225)

l3 = Label(LHS, text=f"System:{my_system.system}", bg="#f4f5f5", font=(
    "Acumin Variable Concept", 15), justify="center")
l3.place(x=20, y=250)

l4 = Label(LHS, text=f"Machine:{my_system.machine}", bg="#f4f5f5", font=(
    "Acumin Variable Concept", 15), justify="center")
l4.place(x=20, y=285)

l5 = Label(LHS, text=f"Total RAM Installed:{round(psutil.virtual_memory().total/1000000000,2)} GB", bg="#f4f5f5", font=(
    "Acumin Variable Concept", 15), justify="center")
l5.place(x=20, y=310)

l6 = Label(LHS, text=f"Processor:{my_system.processor}", bg="#f4f5f5", font=(
    "Acumin Variable Concept", 7), justify="center")
l6.place(x=20, y=340)

# ----------------------------
RHS = Frame(Body, width=470, height=230, bg='#f4f5f5',
            highlightbackground="#adacb1", highlightthickness=1)
RHS.place(x=330, y=10)

system = Label(RHS, text='System', font=(
    "Acumin Variable Concept", 15), bg="#f4f5f5")
system.place(x=10, y=10)


########################
def convertTime(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "%d:%02d:%02d" % (hours, minutes, seconds)


def none():
    global battery_png
    global battery_lable
    battery = psutil.sensors_battery()
    percent = battery.percent
    time = convertTime(battery.secsleft)
    lb1.config(text=f"{percent}%")
    lb1_plug.config(text=f'Plug in : {str(battery.power_plugged)}')
    lb1_time.config(text=f'{time} remaining')

    battery_lable = Label(RHS, background='#f4f5f5')
    battery_lable.place(x=15, y=50)

    lb1.after(1000, none)

    if battery.power_plugged == True:
        battery_png = PhotoImage(file="Image/charging.png")
        battery_lable.config(image=battery_png)
    else:
        battery_png = PhotoImage(file='Image/battery.png')
        battery_lable.config(image=battery_png)


lb1 = Label(RHS, font=("Acumin Variable Concept", 40, 'bold'), bg="#f4f5f5")
lb1.place(x=200, y=40)

lb1_plug = Label(RHS, font=("Acumin Variable Concept", 10), bg="#f4f5f5")
lb1_plug.place(x=20, y=100)

lb1_time = Label(RHS, font=("Acumin Variable Concept", 15), bg="#f4f5f5")
lb1_time.place(x=100, y=100)
none()

########################

# speaker part

lb1_speaker = Label(RHS, text="Speaker : ", font=(
    'arial', 10, 'bold'), bg="#f4f5f5")
lb1_speaker.place(x=10, y=150)
volume_value = tk.DoubleVar()


def get_current_volume_value():
    return '{: .2f}'.format(volume_value.get())


def volume_changed(event):
    device = AudioUtilities.GetSpeakers()
    interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevel(-float(get_current_volume_value()), None)


style = ttk.Style()
style.configure("TScale", background='#f4f5f5')

volume = ttk.Scale(RHS, from_=60, to=0, orient='horizontal',
                   command=volume_changed, variable=volume_value)
volume.place(x=90, y=150)

########################

# brightness part
lb1_brightness = Label(RHS, text='Brightness', font=(
    'arial', 10, 'bold'), bg='#f4f5f5')
lb1_brightness.place(x=10, y=190)

current_value = tk.DoubleVar()


def get_current_value():
    return '{: .2f}'.format(current_value.get())


def brightness_changed(event):
    pct.set_brightness(get_current_value())


brightness = ttk.Scale(RHS, from_=0, to=100, orient='horizontal',
                       command=brightness_changed, variable=current_value)
brightness.place(x=90, y=190)

#########################


def weather():
    app1 = Toplevel()
    app1.geometry("850x500+300+170")
    app1.title('Weather')
    app1.configure(bg='#f4f5f5')
    app1.resizable(False, False)

    # icon
    image_icon = PhotoImage(file='Image/App1.png')
    app1.iconphoto(False, image_icon)

    def getWeather():
        try:
            city = textfield.get()

            geolocator = Nominatim(user_agent="geoapiExercises")
            location = geolocator.geocode(city)
            obj = TimezoneFinder()
            result = obj.timezone_at(
                lng=location.longitude, lat=location.latitude)

            home = pytz.timezone(result)
            local_time = datetime.now(home)
            current_time = local_time.strftime("%I:%M %p")
            clock.config(text=current_time)
            name.config(text="CURRENT WEATHER")

            # weather

            api = "https://api.openweathermap.org/data/2.5/weather?q=" + \
                city+"&appid=646824f2b7b86caffec1d0b16ea77f79"

            json_data = requests.get(api).json()
            condition = json_data['weather'][0]['main']
            description = json_data['weather'][0]['description']
            temp = int(json_data['main']['temp']-273.15)
            pressure = json_data['main']['pressure']
            humidity = json_data['main']['humidity']
            wind = json_data['wind']['speed']

            t.config(text=(temp, "°"))
            c.config(text=(condition, "|", "FEELS", "LIKE", temp, '°'))

            w.config(text=wind)
            h.config(text=humidity)
            d.config(text=description)
            p.config(text=pressure)

        except Exception as e:
            messagebox.showerror("Weather App", "Invalid Entry")

    # search box
    Search_image = PhotoImage(file='Image/search.png')
    myimage = Label(app1, image=Search_image, bg='#f4f5f5')
    myimage.place(x=20, y=20)

    textfield = tk.Entry(app1, justify='center', width=17, font=(
        'poppins', 25, 'bold'), bg='#404040', border=0, fg='white')
    textfield.place(x=50, y=40)
    textfield.focus()

    Search_icon = PhotoImage(file='Image/search_icon.png')
    myimage_icon = Button(app1, image=Search_icon, borderwidth=0,
                          cursor="hand2", bg="#404040", command=getWeather)
    myimage_icon.place(x=400, y=34)

    # logo
    Logo_image = PhotoImage(file='Image/logo.png')
    logo = Label(app1, image=Logo_image, bg='#f4f5f5')
    logo.place(x=150, y=100)

    # bottom box
    Frame_image = PhotoImage(file='Image/box.png')
    frame_image = Label(app1, image=Frame_image, bg='#f4f5f5')
    frame_image.pack(padx=5, pady=5, side=BOTTOM)

    # time
    name = Label(app1, font=('arial', 15, 'bold'), bg='#f4f5f5')
    name.place(x=30, y=100)

    clock = Label(app1, font=('Helvetica', 20), bg='#f4f5f5')
    clock.place(x=30, y=130)

    # label
    label1 = Label(app1, text="WIND", font=(
        'Helvetica', 15), fg='white', bg='#1ab5ef')
    label1.place(x=120, y=400)

    label2 = Label(app1, text="HUMIDITY", font=(
        'Helvetica', 15), fg='white', bg='#1ab5ef')
    label2.place(x=250, y=400)

    label3 = Label(app1, text="DESCRIPTION", font=(
        'Helvetica', 15), fg='white', bg='#1ab5ef')
    label3.place(x=430, y=400)

    label4 = Label(app1, text="PRESSURE", font=(
        'Helvetica', 15), fg='white', bg='#1ab5ef')
    label4.place(x=650, y=400)

    t = Label(app1, font=('arial', 70, 'bold'), fg='#ee666d', bg='#f4f5f5')
    t.place(x=400, y=150)
    c = Label(app1, font=('arial', 15, 'bold'), bg='#f4f5f5')
    c.place(x=400, y=250)

    w = Label(app1, text='...', font=('arial', 20, 'bold'), bg='#1ab5ef')
    w.place(x=120, y=430)
    h = Label(app1, text='...', font=('arial', 20, 'bold'), bg='#1ab5ef')
    h.place(x=280, y=430)
    d = Label(app1, text='...', font=('arial', 20, 'bold'), bg='#1ab5ef')
    d.place(x=450, y=430)
    p = Label(app1, text='...', font=('arial', 20, 'bold'), bg='#1ab5ef')
    p.place(x=670, y=430)

    app1.mainloop()


def clock():
    app2 = Toplevel()
    app2.geometry("850x110+300+10")
    app2.title('Clock')
    app2.configure(bg="#292e2e")
    app2.resizable(False, False)

    # icon
    image_icon = PhotoImage(file="Image/App2.png")
    app2.iconphoto(False, image_icon)

    def clock():
        text = strftime('%H:%M:%S %p')
        lb1.config(text=text)
        lb1.after(1000, clock)

    lb1 = Label(app2, font=('digital-7', 50, 'bold'),
                width=20, bg='#f4f5f5', fg='#292e2e')
    lb1.pack(anchor='center', pady=20)
    clock()

    app2.mainloop


def calender():
    app3 = Toplevel()
    app3.geometry("300x300+40+40")
    app3.title('Calender')
    app3.configure(bg="#292e2e")
    app3.resizable(False, False)

    # icon

    image_icon = PhotoImage(file="Image/App3.png")
    app3.iconphoto(False, image_icon)

    mycal = Calendar(app3, setmode='day', date_pattern='d/m/yy')
    mycal.pack(padx=15, pady=20)

    app3.mainloop()


# Node
button_mode = True


def mode():
    global button_mode
    if button_mode:
        LHS.config(bg="#292e2e")
        myimage.config(bg="#292e2e")
        l1.config(bg="#292e2e", fg="#d6d6d6")
        l2.config(bg="#292e2e", fg="#d6d6d6")
        l3.config(bg="#292e2e", fg="#d6d6d6")
        l4.config(bg="#292e2e", fg="#d6d6d6")
        l5.config(bg="#292e2e", fg="#d6d6d6")
        l6.config(bg="#292e2e", fg="#d6d6d6")

        RHB.config(bg="#292e2e")
        app1.config(bg="#292e2e")
        app2.config(bg="#292e2e")
        app3.config(bg="#292e2e")
        app4.config(bg="#292e2e")
        app5.config(bg="#292e2e")
        app6.config(bg="#292e2e")
        app7.config(bg="#292e2e")
        app8.config(bg="#292e2e")
        app9.config(bg="#292e2e")
        app10.config(bg="#292e2e")
        apps.config(bg="#292e2e", fg="#d6d6d6")

        button_mode = False
    else:
        LHS.config(bg="#292e2e")
        myimage.config(bg="#f4f5f5")
        l1.config(bg="#f4f5f5", fg="#292e2e")
        l2.config(bg="#f4f5f5", fg="#292e2e")
        l3.config(bg="#f4f5f5", fg="#292e2e")
        l4.config(bg="#f4f5f5", fg="#292e2e")
        l5.config(bg="#f4f5f5", fg="#292e2e")
        l6.config(bg="#f4f5f5", fg="#292e2e")

        RHB.config(bg="#f4f5f5")
        app1.config(bg="#f4f5f5")
        app2.config(bg="#f4f5f5")
        app3.config(bg="#f4f5f5")
        app4.config(bg="#f4f5f5")
        app5.config(bg="#f4f5f5")
        app6.config(bg="#f4f5f5")
        app7.config(bg="#f4f5f5")
        app8.config(bg="#f4f5f5")
        app9.config(bg="#f4f5f5")
        app10.config(bg="#f4f5f5")
        apps.config(bg="#f4f5f5", fg="#292e2e")

        button_mode = True


def game():
    class GuessNumberGame:
        def __init__(self, master):
            self.master = master
            self.master.title("Guess the Number")
            self.master.geometry("500x300")

            self.num_to_guess = random.randint(1, 100)
            self.num_guesses = 0

            self.guess_label = tk.Label(self.master, text="Guess a number between 1 and 100:")
            self.guess_label.pack()

            self.guess_entry = tk.Entry(self.master)
            self.guess_entry.pack()

            self.guess_button = tk.Button(self.master, text="Guess", command=self.check_guess)
            self.guess_button.pack()

            self.result_label = tk.Label(self.master, text="")
            self.result_label.pack()

        def check_guess(self):
            guess = int(self.guess_entry.get())
            self.num_guesses += 1

            if guess < self.num_to_guess:
                self.result_label.config(text="Too low! Guess again.")
            elif guess > self.num_to_guess:
                self.result_label.config(text="Too high! Guess again.")
            else:
                self.result_label.config(text=f"Congratulations! You guessed the number in {self.num_guesses} guesses.")
                self.guess_button.config(state=tk.DISABLED)
                self.guess_entry.config(state=tk.DISABLED)

    root = tk.Tk()
    game = GuessNumberGame(root)
    root.mainloop()
    
    # app5 = Toplevel()
    # app5.geometry("300x500+670+170")
    # app5.title('Ludo')
    # app5.config(bg="#dee2e5")
    # app5.resizable(False, False)

    # # icon
    # image_icon = PhotoImage(file='Image/App5.png')
    # app5.iconphoto(False, image_icon)

    # ludo_image = PhotoImage(file='Image/ludo back.png')
    # Label(app5, image=ludo_image).pack()

    # label = Label(app5, text='', font=('times', 150))

    # def roll():
    #     dice = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
    #     label.configure(
    #         text=f'{random.choice(dice)}{random.choice(dice)}', fg="#29232e")
    #     label.pack()

    # btn_image = PhotoImage(file="Image/ludo button.png")
    # btn = Button(app5, image=btn_image, bg="#dee3e5", command=roll)
    # btn.pack(padx=10, pady=10)

    # app5.mainloop()


def screenshot():
    root.iconify()

    myScreenshot = pyautogui.screenshot()
    file_path = filedialog.asksaveasfilename(defaultextension='.png')
    myScreenshot.save(file_path)


def file():
    subprocess.Popen(r'explorer /select,"C:\path\of\folder\file"')


def browser():
    class MainWindow(QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            self.browser = QWebEngineView()
            self.browser.setUrl(QUrl('http://google.com'))
            self.setCentralWidget(self.browser)
            self.showMaximized()

            # navbar
            navbar = QToolBar()
            self.addToolBar(navbar)

            back_btn = QAction('Back', self)
            back_btn.triggered.connect(self.browser.back)
            navbar.addAction(back_btn)

            forward_btn = QAction('Forward', self)
            forward_btn.triggered.connect(self.browser.forward)
            navbar.addAction(forward_btn)

            reload_btn = QAction('Reload', self)
            reload_btn.triggered.connect(self.browser.reload)
            navbar.addAction(reload_btn)

            home_btn = QAction('Home', self)
            home_btn.triggered.connect(self.navigate_home)
            navbar.addAction(home_btn)

            self.url_bar = QLineEdit()
            self.url_bar.returnPressed.connect(self.navigate_to_url)
            navbar.addWidget(self.url_bar)

            self.browser.urlChanged.connect(self.update_url)

        def navigate_home(self):
            self.browser.setUrl(
                QUrl('https://www.facebook.com/people/Mamun-Mia-Turan/100064537459484/'))

        def navigate_to_url(self):
            url = self.url_bar.text()
            self.browser.setUrl(QUrl(url))

        def update_url(self, q):
            self.url_bar.setText(q.toString())

    app = QApplication(sys.argv)
    QApplication.setApplicationName('My Browser')
    window = MainWindow()
    app.exec_()


def close_apps():
    wb.register('Chrome', None)
    wb.open('https://chat.openai.com/chat')


def calculator():
    class Calculator:
        def __init__(self, master):
            self.master = master
            master.title("Calculator")

            # create entry field for display
            self.display = tk.Entry(master, width=25, justify="right")
            self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

            # create buttons for numbers and operators
            self.create_button("7", 1, 0)
            self.create_button("8", 1, 1)
            self.create_button("9", 1, 2)
            self.create_button("/", 1, 3)
            self.create_button("4", 2, 0)
            self.create_button("5", 2, 1)
            self.create_button("6", 2, 2)
            self.create_button("*", 2, 3)
            self.create_button("1", 3, 0)
            self.create_button("2", 3, 1)
            self.create_button("3", 3, 2)
            self.create_button("-", 3, 3)
            self.create_button("0", 4, 0)
            self.create_button(".", 4, 1)
            self.create_button("C", 4, 2)
            self.create_button("+", 4, 3)
            self.create_button("%", 5, 0)
            self.create_button("sqrt", 5, 1)
            self.create_button("^", 5, 2)
            self.create_button("(", 6, 0)
            self.create_button(")", 6, 1)
            self.create_button("=", 6, 2, 2)

        def create_button(self, text, row, column, columnspan=1):
            button = tk.Button(self.master, text=text, padx=10, pady=5,
                               command=lambda: self.button_click(text))
            button.grid(row=row, column=column,
                        columnspan=columnspan, padx=2, pady=2)

        def button_click(self, text):
            if text == "=":
                try:
                    expression = self.display.get()
                    expression = expression.replace('^', '**')
                    expression = expression.replace('%', '/100*')
                    result = eval(expression)
                    self.display.delete(0, tk.END)
                    self.display.insert(0, str(result))
                except:
                    self.display.delete(0, tk.END)
                    self.display.insert(0, "Error")
            elif text == "C":
                self.display.delete(0, tk.END)
            elif text == "sqrt":
                try:
                    number = float(self.display.get())
                    result = sqrt(number)
                    self.display.delete(0, tk.END)
                    self.display.insert(0, str(result))
                except:
                    self.display.delete(0, tk.END)
                    self.display.insert(0, "Error")
            else:
                self.display.insert(tk.END, text)

    root = tk.Tk()
    app = Calculator(master=root)
    root.mainloop()


def translator():
    class TranslatorApp:
        def __init__(self, master):
            self.master = master
            master.title("English to Bangla Translator")

            # create input frame with label and entry field
            input_frame = tk.Frame(master)
            input_frame.pack(padx=20, pady=20)
            input_label = tk.Label(
                input_frame, text="Enter English text:", font=("Arial", 12))
            input_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            self.input_field = tk.Entry(
                input_frame, width=50, font=("Arial", 12))
            self.input_field.grid(row=1, column=0, padx=10, pady=10)

            # create button frame with translate and clear buttons
            button_frame = tk.Frame(master)
            button_frame.pack(padx=20, pady=20)
            translate_button = tk.Button(button_frame, text="Translate", font=(
                "Arial", 12), padx=10, pady=5, command=self.translate)
            translate_button.pack(side="left")
            clear_button = tk.Button(button_frame, text="Clear", font=(
                "Arial", 12), padx=10, pady=5, command=self.clear_input)
            clear_button.pack(side="left", padx=10)

            # create output frame with label and result text box
            output_frame = tk.Frame(master)
            output_frame.pack(padx=20, pady=20)
            output_label = tk.Label(
                output_frame, text="Bangla Translation:", font=("Arial", 12))
            output_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
            self.result_text = tk.Text(
                output_frame, height=4, width=50, font=("Arial", 12))
            self.result_text.grid(row=1, column=0, padx=10, pady=10)

        def translate(self):
            # get input text
            input_text = self.input_field.get()

            # create translator object and translate input text to Bangla
            translator = Translator()
            result = translator.translate(input_text, dest="bn").text

            # display translation result
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", result)

        def clear_input(self):
            # clear input field and result text box
            self.input_field.delete(0, "end")
            self.result_text.delete("1.0", "end")

    root = tk.Tk()
    app = TranslatorApp(master=root)
    root.mainloop()


def bmiCalculator():

    # Create the main window
    root = tk.Tk()
    root.title("BMI Calculator")
    root.geometry("400x300")

    # Create the labels and entry fields for height and weight
    height_frame = ttk.Frame(root)
    height_frame.pack(pady=10)

    feet_label = ttk.Label(height_frame, text="Feet:")
    feet_label.pack(side=tk.LEFT)
    feet_entry = ttk.Entry(height_frame, width=5)
    feet_entry.pack(side=tk.LEFT)

    inches_label = ttk.Label(height_frame, text="Inches:")
    inches_label.pack(side=tk.LEFT)
    inches_entry = ttk.Entry(height_frame, width=5)
    inches_entry.pack(side=tk.LEFT)

    weight_frame = ttk.Frame(root)
    weight_frame.pack(pady=10)

    weight_label = ttk.Label(weight_frame, text="Weight (kg):")
    weight_label.pack(side=tk.LEFT)
    weight_entry = ttk.Entry(weight_frame)
    weight_entry.pack(side=tk.LEFT)

    # Create the function to calculate BMI
    def calculate_bmi():
        feet = float(feet_entry.get()) # 5.0
        inches = float(inches_entry.get()) # 9.0
        height = (feet * 12 + inches) * 0.0254  # Convert height to meters
        weight = float(weight_entry.get())
        # Calculate BMI using the metric system formula
        bmi = weight / (height ** 2)
        result_label.config(text="Your BMI is {:.3f}".format(bmi))

    # Create the button to calculate BMI
    calculate_button = ttk.Button(
        root, text="Calculate BMI", command=calculate_bmi)
    calculate_button.pack(pady=10)

    # Create the label to display the result
    result_label = ttk.Label(root, text="")
    result_label.pack()

    # Start the main event loop
    root.mainloop()


def note():
    
    # Create a new window
    root = Tk()
    root.title("Task Manager")
    root.geometry("800x600")
    root.config(bg="#E5E5E5")

    # Define the task list
    tasks = []
    # Create a connection to the MySQL database
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="todonote"
    )

    # Create a cursor to execute SQL queries
    mycursor = mydb.cursor()
    # Function to add a new task to the list


    def add_task():
        name = name_entry.get()
        deadline = deadline_entry.get()
        status = status_var.get()
        if name and deadline:
            task = {"name": name, "deadline": deadline, "status": status}
            tasks.append(task)
            sql = "INSERT INTO tasks (name, deadline, status) VALUES (%s, %s, %s)"
            val = (name, deadline, status)
            mycursor.execute(sql, val)
            mydb.commit()
            update_task_list()
        else:
            messagebox.showerror("Error", "Please enter task name and deadline.")

    # Function to edit a task in the list


    def edit_task():
        selected_task = task_list.curselection()
        if selected_task:
            task = tasks[selected_task[0]]
            task["name"] = name_entry.get()
            task["deadline"] = deadline_entry.get()
            task["status"] = status_var.get()
            sql = "UPDATE tasks SET name = %s, deadline = %s, status = %s WHERE id = %s"
            val = (name_entry.get(), deadline_entry.get(),
                status_var.get(), task["id"])
            mycursor.execute(sql, val)
            mydb.commit()
            update_task_list()

    # Function to delete a task from the list


    def delete_task():
        selected_task = task_list.curselection()
        if selected_task:
            task = tasks[selected_task[0]]
            sql = "DELETE FROM tasks WHERE id = %s"
            val = (task["id"],)
            mycursor.execute(sql, val)
            mydb.commit()
            tasks.pop(selected_task[0])
            update_task_list()

    # Function to update the task list


    def update_task_list():
        task_list.delete(0, END)
        mycursor.execute("SELECT * FROM tasks")
        rows = mycursor.fetchall()
        for row in rows:
            task = {"id": row[0], "name": row[1],
                    "deadline": row[2], "status": row[3]}
            tasks.append(task)
            task_list.insert(
                END, f"{task['name']} - {task['deadline']} - {task['status']}")


    # Create a label for the task list
    task_list_label = Label(root, text="Task List",
                            font=("Arial Bold", 16), bg="#E5E5E5")
    task_list_label.grid(row=0, column=0, padx=10, pady=10)

    # Create a listbox for the task list
    task_list = Listbox(root, font=("Arial", 12), width=50)
    task_list.grid(row=1, column=0, padx=20, pady=(0, 10), columnspan=2)

    # Create a label for the task form
    task_form_label = Label(root, text="Task Form",
                            font=("Arial Bold", 16), bg="#E5E5E5")
    task_form_label.grid(row=0, column=2, padx=10, pady=10)

    # Create a label for the task name
    name_label = Label(root, text="Task Name", font=("Arial", 12), bg="#E5E5E5")
    name_label.grid(row=1, column=2, padx=10, pady=10, sticky=W)

    # Create a label for the task name
    name_label = Label(root, text="Task Name", font=("Arial", 12))
    name_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")

    # Create an entry for the task name
    name_entry = Entry(root, font=("Arial", 12))
    name_entry.grid(row=2, column=1, padx=10, pady=10)

    # Create a label for the deadline
    deadline_label = Label(root, text="Deadline", font=("Arial", 12))
    deadline_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")

    # Create an entry for the deadline
    deadline_entry = Entry(root, font=("Arial", 12))
    deadline_entry.grid(row=3, column=1, padx=10, pady=10)

    # Create a label for the status
    status_label = Label(root, text="Status", font=("Arial", 12))
    status_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")

    # Create a variable for the status
    status_var = StringVar()
    status_var.set("Not Started")

    # Create a radio button for the not started status
    not_started_radio = Radiobutton(
        root, text="Not Started", variable=status_var, value="Not Started", font=("Arial", 12))
    not_started_radio.grid(row=5, column=0, padx=10, pady=10, sticky="w")

    # Create a radio button for the in progress status
    in_progress_radio = Radiobutton(
        root, text="In Progress", variable=status_var, value="In Progress", font=("Arial", 12))
    in_progress_radio.grid(row=6, column=0, padx=10, pady=10, sticky="w")

    # Create a radio button for the completed status
    completed_radio = Radiobutton(
        root, text="Completed", variable=status_var, value="Completed", font=("Arial", 12))
    completed_radio.grid(row=7, column=0, padx=10, pady=10, sticky="w")

    # Create a button to add a task
    add_button = Button(root, text="Add Task", command=add_task, font=(
        "Arial", 12), bg="green", fg="white", activebackground="darkgreen", activeforeground="white")
    add_button.grid(row=8, column=0, padx=10, pady=10, sticky="w")

    # Create a button to edit a task
    edit_button = Button(root, text="Edit Task", command=edit_task, font=(
        "Arial", 12), bg="orange", fg="white", activebackground="darkorange", activeforeground="white")
    edit_button.grid(row=8, column=1, padx=10, pady=10, sticky="e")

    # Create a button to delete a task
    delete_button = Button(root, text="Delete Task", command=delete_task, font=(
        "Arial", 12), bg="red", fg="white", activebackground="darkred", activeforeground="white")
    delete_button.grid(row=8, column=2, padx=10, pady=10, sticky="e")
    # Update the task list
    update_task_list()

    root.mainloop()


def close_window():
    root.destroy()


# ----------------------------
RHB = Frame(Body, width=470, height=190, bg='#f4f5f5',
            highlightbackground="#adacb1", highlightthickness=1)
RHB.place(x=330, y=255)

apps = Label(RHB, text='Apps', font=(
    "Acumin Variable Concept", 15), bg="#f4f5f5")
apps.place(x=10, y=10)

app1_image = PhotoImage(file='Image/App1.png')
app1 = Button(RHB, image=app1_image, bd=0, command=weather)
app1.place(x=15, y=50)

app2_image = PhotoImage(file='Image/App2.png')
app2 = Button(RHB, image=app2_image, bd=0, command=clock)
app2.place(x=75, y=50)

app3_image = PhotoImage(file='Image/App3.png')
app3 = Button(RHB, image=app3_image, bd=0, command=calender)
app3.place(x=135, y=50)

app4_image = PhotoImage(file='Image/App4.png')
app4 = Button(RHB, image=app4_image, bd=0, command=mode)
app4.place(x=195, y=50)

app5_image = PhotoImage(file='Image/icons8-games-folder-48.png')
app5 = Button(RHB, image=app5_image, bd=0, command=game)
app5.place(x=260, y=45)

app6_image = PhotoImage(file='Image/App6.png')
app6 = Button(RHB, image=app6_image, bd=0, command=screenshot)
app6.place(x=330, y=50)

app7_image = PhotoImage(file='Image/App7.png')
app7 = Button(RHB, image=app7_image, bd=0, command=file)
app7.place(x=400, y=50)

app8_image = PhotoImage(file='Image/App8.png')
app8 = Button(RHB, image=app8_image, bd=0, command=browser)
app8.place(x=15, y=120)

app9_image = PhotoImage(file='Image/chatbot.png')
app9 = Button(RHB, image=app9_image, bd=0, command=close_apps)
app9.place(x=75, y=120)

app11_image = PhotoImage(file='Image/calculator.png')
app11 = Button(RHB, image=app11_image, bd=0, command=calculator)
app11.place(x=135, y=120)

app12_image = PhotoImage(file='Image/translator.png')
app12 = Button(RHB, image=app12_image, bd=0, command=translator)
app12.place(x=195, y=120)

app13_image = PhotoImage(file='Image/bmi.png')
app13 = Button(RHB, image=app13_image, bd=0, command=bmiCalculator)
app13.place(x=260, y=120)

app14_image = PhotoImage(file='Image/icons8-todo-list.gif')
app14 = Button(RHB, image=app14_image, bd=0, command=note)
app14.place(x=330, y=120)

app10_image = PhotoImage(file='Image/App10.png')
app10 = Button(RHB, image=app10_image, bd=0, command=close_window)
app10.place(x=400, y=120)

root.mainloop()
