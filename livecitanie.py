import tkinter as tk
from PIL import ImageGrab, ImageEnhance, ImageFilter, ImageOps
import pytesseract
import ctypes
import threading
import time

# Nastaviť aplikáciu ako DPI Aware
ctypes.windll.user32.SetProcessDPIAware()

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

def start_monitoring():
    threading.Thread(target=monitor_area).start()

def monitor_area():
    while True:
        screenshot = ImageGrab.grab(bbox)
        # Predspracovanie obrázka
        screenshot = screenshot.convert('L')
        enhancer = ImageEnhance.Contrast(screenshot)
        screenshot = enhancer.enhance(3.0)
        screenshot = screenshot.filter(ImageFilter.SHARPEN)
        screenshot = screenshot.point(lambda p: p > 128 and 255)
        screenshot = ImageOps.invert(screenshot)

        text = pytesseract.image_to_string(screenshot, config='--psm 6 outputbase digits')
        print("Detected numbers:", text)
        time.sleep(1)  # Časový interval medzi snímkami

root = tk.Tk()
root.attributes('-fullscreen', True)  # Celá obrazovka
root.attributes('-alpha', 0.3)  # Mierne transparentné okno

canvas = tk.Canvas(root, cursor="cross")
canvas.pack(fill=tk.BOTH, expand=True)

canvas.bind('<ButtonPress-1>', on_press)
canvas.bind('<B1-Motion>', on_drag)
canvas.bind('<ButtonRelease-1>', on_release)

root.mainloop()
