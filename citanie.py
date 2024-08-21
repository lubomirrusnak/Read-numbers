import tkinter as tk
from PIL import ImageGrab, ImageEnhance, ImageFilter
import pytesseract
import ctypes

# Nastaviť aplikáciu ako DPI Aware
ctypes.windll.user32.SetProcessDPIAware()

def on_drag(event):
    global rect, start_x, start_y
    canvas.coords(rect, start_x, start_y, event.x, event.y)

def on_press(event):
    global start_x, start_y, rect
    start_x, start_y = (event.x, event.y)
    rect = canvas.create_rectangle(start_x, start_y, start_x, start_y, outline='red')

def on_release(event):
    window_x, window_y = root.winfo_rootx(), root.winfo_rooty()
    bbox = (min(start_x, event.x) + window_x, min(start_y, event.y) + window_y,
            max(start_x, event.x) + window_x, max(start_y, event.y) + window_y)

    screenshot = ImageGrab.grab(bbox)

    # Predspracovanie obrázka
    screenshot = screenshot.convert('L')  # Prevod na šedú škálu
    enhancer = ImageEnhance.Contrast(screenshot)
    screenshot = enhancer.enhance(2.0)  # Zvýšenie kontrastu
    screenshot = screenshot.filter(ImageFilter.SHARPEN)  # Zvýšenie ostrosti

    screenshot.show()  # Zobrazenie obrázka

    # Nastavenia pytesseract
    custom_config = r'--oem 3 --psm 6 outputbase digits'
    extracted_text = pytesseract.image_to_string(screenshot, config=custom_config)
    print("Extrahované čísla:")
    print(extracted_text)

    root.destroy()

root = tk.Tk()
root.attributes('-fullscreen', True)
root.attributes('-alpha', 0.3)

canvas = tk.Canvas(root, cursor="cross")
canvas.pack(fill=tk.BOTH, expand=True)

canvas.bind('<ButtonPress-1>', on_press)
canvas.bind('<B1-Motion>', on_drag)
canvas.bind('<ButtonRelease-1>', on_release)

root.mainloop()
