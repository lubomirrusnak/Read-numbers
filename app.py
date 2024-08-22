import tkinter as tk
from PIL import ImageGrab, ImageEnhance, ImageFilter, ImageOps
import pytesseract
import ctypes
import threading
import time
import cv2
import numpy as np
from PIL import Image

# Nastaviť aplikáciu ako DPI Aware
ctypes.windll.user32.SetProcessDPIAware()

# Globálne premenné na uloženie hodnôt
start_value = None
end_value = None
button_value = None

# Premenné na uchovanie posledných zadaných hodnôt
last_start_value = None
last_end_value = None
last_button_value = None

def start_action():
    open_input_window("FAST", set_start_value, last_start_value)

def end_action():
    open_input_window("MEDIUM", set_end_value, last_end_value)

def button_action():
    open_input_window("SLOW", set_button_value, last_button_value)

def open_input_window(title, callback, last_value):
    input_window = tk.Toplevel(root)
    input_window.title(title)
    input_window.geometry("300x150")
    
    label = tk.Label(input_window, text=f"Zadajte hodnotu pre {title}:")
    label.pack(pady=10)
    
    entry = tk.Entry(input_window)
    entry.pack(pady=10)
    
    # Ak existuje posledná hodnota, predvyplníme ňou textové pole
    if last_value is not None:
        entry.insert(0, str(last_value))
    
    def ok_action():
        try:
            value = int(entry.get())  # Získať hodnotu z textového poľa a konvertovať na celé číslo
            callback(value)  # Zavolať príslušný callback na uloženie hodnoty
            
            # Uložíme poslednú zadanú hodnotu
            global last_start_value, last_end_value, last_button_value
            if title == "FAST":
                last_start_value = value
            elif title == "MEDIUM":
                last_end_value = value
            elif title == "SLOW":
                last_button_value = value
                
            print(f"Zadaná hodnota pre {title}:", value)  # Vypíše zadanú hodnotu do konzoly
            
            input_window.destroy()  # Zavrieť okno po stlačení OK
        except ValueError:
            # Ak hodnota nie je platné celé číslo, zobraziť chybové hlásenie (voliteľné)
            error_label = tk.Label(input_window, text="Prosím, zadajte platné číslo!", fg="red")
            error_label.pack()

    ok_button = tk.Button(input_window, text="OK", command=ok_action)
    ok_button.pack(pady=10)

def set_start_value(value):
    global start_value
    start_value = value

def set_end_value(value):
    global end_value
    end_value = value

def set_button_value(value):
    global button_value
    button_value = value

def start_monitoring_gui():
    monitoring_window = tk.Toplevel(root)
    monitoring_window.attributes('-fullscreen', True)  # Celá obrazovka
    monitoring_window.attributes('-alpha', 0.3)  # Mierne transparentné okno
    
    canvas = tk.Canvas(monitoring_window, cursor="cross")
    canvas.pack(fill=tk.BOTH, expand=True)
    
    def on_drag(event):
        global rect, start_x, start_y
        canvas.coords(rect, start_x, start_y, event.x, event.y)

    def on_press(event):
        global start_x, start_y, rect
        start_x, start_y = (event.x_root, event.y_root)  # Použiť globálne súradnice
        rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red')

    def on_release(event):
        global bbox
        end_x, end_y = (event.x_root, event.y_root)  # Použiť globálne súradnice
        bbox = (min(start_x, end_x), min(start_y, end_y), max(start_x, end_x), max(start_y, end_y))
        start_monitoring()
        canvas.delete(rect)  # Odstráni obdĺžnik po výbere
        monitoring_window.destroy()  # Zavrie výberové okno po výbere oblasti

    def start_monitoring():
        threading.Thread(target=monitor_area).start()

    def monitor_area():
        while True:
            screenshot = ImageGrab.grab(bbox)
            screenshot_np = np.array(screenshot)
            gray = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2GRAY)
            adaptive_thresh = cv2.adaptiveThreshold(
                gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                cv2.THRESH_BINARY_INV, 11, 2
            )
            processed_image = Image.fromarray(adaptive_thresh)
            text = pytesseract.image_to_string(processed_image, config='--psm 6 outputbase digits').strip()
            print("Detected numbers:", text)
            
            if text.isdigit():
                number = int(text)
                update_button_colors(number)

            time.sleep(0.1)

    def update_button_colors(number):
        # Reset colors to black
        start_button.config(bg="black")
        end_button.config(bg="black")
        generic_button.config(bg="black")
        
        # Check ranges and update button colors to red
        if start_value is not None and number <= start_value:
            start_button.config(bg="red")
        elif end_value is not None and start_value < number <= end_value:
            end_button.config(bg="red")
        elif button_value is not None and number > button_value:
            generic_button.config(bg="red")

    canvas.bind('<ButtonPress-1>', on_press)
    canvas.bind('<B1-Motion>', on_drag)
    canvas.bind('<ButtonRelease-1>', on_release)

root = tk.Tk()
root.title("Simple GUI")
root.geometry("400x300")

# Vytvorenie tlačidiel s počiatočnou farbou čiernou
start_button = tk.Button(root, text="FAST", command=start_action, bg="black", fg="white")
end_button = tk.Button(root, text="MEDIUM", command=end_action, bg="black", fg="white")
generic_button = tk.Button(root, text="SLOW", command=button_action, bg="black", fg="white")
monitoring_button = tk.Button(root, text="Start Monitoring", command=start_monitoring_gui, bg="black", fg="white")

# Umiestnenie tlačidiel pod sebou
start_button.pack(pady=10)
end_button.pack(pady=10)
generic_button.pack(pady=10)
monitoring_button.pack(pady=10)

root.mainloop()
