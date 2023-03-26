from tkinter import *
from tkinter import ttk
from tkinter import ttk, messagebox
import tkinter as tk
from tkinter import filedialog
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

# camera
import cv2


import subprocess
import webbrowser as wb
import random

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
    app5 = Toplevel()
    app5.geometry("300x500+670+170")
    app5.title('Ludo')
    app5.config(bg="#dee2e5")
    app5.resizable(False, False)

    # icon
    image_icon = PhotoImage(file='Image/App5.png')
    app5.iconphoto(False, image_icon)

    ludo_image = PhotoImage(file='Image/ludo back.png')
    Label(app5, image=ludo_image).pack()

    label = Label(app5, text='', font=('times', 150))

    def roll():
        dice = ['\u2680', '\u2681', '\u2682', '\u2683', '\u2684', '\u2685']
        label.configure(
            text=f'{random.choice(dice)}{random.choice(dice)}', fg="#29232e")
        label.pack()

    btn_image = PhotoImage(file="Image/ludo button.png")
    btn = Button(app5, image=btn_image, bg="#dee3e5", command=roll)
    btn.pack(padx=10, pady=10)

    app5.mainloop()


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


def camera():
    pass


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

app5_image = PhotoImage(file='Image/App5.png')
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

app9_image = PhotoImage(file='Image/App9.png')
app9 = Button(RHB, image=app9_image, bd=0, command=close_apps)
app9.place(x=75, y=120)

app11_image = PhotoImage(file='Image/App6.png')
app11 = Button(RHB, image=app11_image, bd=0, command=camera)
app11.place(x=135, y=120)

app10_image = PhotoImage(file='Image/App10.png')
app10 = Button(RHB, image=app10_image, bd=0, command=close_window)
app10.place(x=400, y=120)


root.mainloop()
