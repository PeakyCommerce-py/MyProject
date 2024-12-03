import os
import time
import pyautogui
import pygetwindow as gw
import pandas as pd
import random
import string
from tkinter import Tk, Button, Label, filedialog, messagebox, StringVar, simpledialog
from datetime import datetime, timedelta
import telebot

# Initialize Telegram bot with your bot token
bot = telebot.TeleBot('7395514279:AAGvFUqdzTURrG6GXmRJO2U75UlACozCOLw')
admins = ['541466828', '1148095852']


# Function to send messages to the admin
def send_message_to_admin(text: str):
    for admin in admins:
        bot.send_message(admin, text)


class ZoiperCaller:
    def __init__(self, master):
        self.master = master
        self.master.title("Zoiper Auto Caller")
        self.master.geometry("400x300")

        self.zoiper_path = r"C:\Program Files (x86)\Zoiper5\Zoiper5.exe"
        self.phone_numbers = []
        self.current_index = 0

        self.label = Label(master, text="Choose an Excel file with phone numbers:")
        self.label.pack(pady=10)

        self.choose_button = Button(master, text="Choose File", command=self.load_file)
        self.choose_button.pack(pady=5)

        self.start_button = Button(master, text="Start Calling", command=self.start_calling)
        self.start_button.pack(pady=5)

        self.next_button = Button(master, text="Next Number", command=self.call_next_number)
        self.next_button.pack(pady=20)

        self.current_number_var = StringVar()
        self.current_number_label = Label(master, textvariable=self.current_number_var)
        self.current_number_label.pack(pady=10)

        self.hidden_file = os.path.join(os.getenv('APPDATA'), 'zoiper_caller_hidden.txt')
        self.check_first_use()

    def check_first_use(self):
        if os.path.exists(self.hidden_file):
            with open(self.hidden_file, 'r') as f:
                first_use_time = datetime.fromisoformat(f.readline().strip())
            if datetime.now() - first_use_time >= timedelta(days=7):
                self.verify_code()
        else:
            self.first_use()

    def first_use(self):
        token = self.generate_token()
        send_message_to_admin(f"First use token: {token}")
        user_token = self.prompt_token()
        if user_token != token:
            messagebox.showerror("Invalid Token", "The token you entered is incorrect.")
            self.master.quit()
        else:
            with open(self.hidden_file, 'w') as f:
                f.write(datetime.now().isoformat())

    def verify_code(self):
        token = self.generate_token()
        send_message_to_admin(f"Verification token: {token}")
        user_token = self.prompt_token()
        if user_token != token:
            messagebox.showerror("Invalid Code", "The code you entered is incorrect.")
            self.master.quit()

    def generate_token(self):
        return ''.join(random.choices(string.digits, k=8)) + ''.join(random.choices(string.ascii_uppercase, k=2))

    def prompt_token(self):
        return simpledialog.askstring("Verification", "Enter the verification code sent to the admin:")

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            self.phone_numbers = self.read_excel(file_path)
            messagebox.showinfo("File Loaded", f"Loaded {len(self.phone_numbers)} phone numbers.")
        else:
            messagebox.showwarning("No File", "No file selected!")

    def read_excel(self, file_path):
        df = pd.read_excel(file_path, dtype=str)
        return df['Phone Numbers'].tolist()

    def start_calling(self):
        if not self.phone_numbers:
            messagebox.showwarning("No Numbers", "No phone numbers loaded!")
            return

        if self.launch_zoiper():
            self.call_next_number()

    def launch_zoiper(self):
        os.startfile(self.zoiper_path)
        for _ in range(60):
            if any("Zoiper5" in window for window in gw.getAllTitles()):
                return True

        messagebox.showerror("Error", "Zoiper did not launch in time.")
        return False

    def call_next_number(self):
        if self.launch_zoiper():
            if self.current_index >= len(self.phone_numbers):
                messagebox.showinfo("Done", "All numbers have been called.")
                return

            phone_number = self.phone_numbers[self.current_index]
            self.current_number_var.set(f"Calling: {phone_number}")
            self.make_call(phone_number)
            self.current_index += 1

    def make_call(self, phone_number):
        if not self.is_zoiper_open():
            self.launch_zoiper()
            time.sleep(10)

        zoiper_window = self.get_zoiper_window()
        if zoiper_window is None:
            messagebox.showerror("Zoiper Not Found", "Zoiper window not found.")
            return

        self.bring_zoiper_to_front(zoiper_window)
        input_field_x = zoiper_window.left + 100
        input_field_y = zoiper_window.top + 80

        pyautogui.click(input_field_x, input_field_y)
        time.sleep(.2)
        pyautogui.typewrite(phone_number)
        time.sleep(.2)
        pyautogui.press('enter')

    def is_zoiper_open(self):
        return any("Zoiper5" in window for window in gw.getAllTitles())

    def get_zoiper_window(self):
        for window in gw.getAllTitles():
            if "Zoiper5" in window:
                return gw.getWindowsWithTitle(window)[0]
        return None

    def bring_zoiper_to_front(self, zoiper_window):
        zoiper_window.activate()
        time.sleep(1)


# Create the GUI application
root = Tk()
app = ZoiperCaller(master=root)
root.mainloop()
