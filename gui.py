import tkinter as tk

# Globálne premenné na uloženie hodnôt
start_value = None
end_value = None
button_value = None

def start_action():
    open_input_window("Start Value", set_start_value)

def end_action():
    open_input_window("End Value", set_end_value)

def button_action():
    open_input_window("Button Value", set_button_value)

def open_input_window(title, callback):
    input_window = tk.Toplevel(root)
    input_window.title(title)
    input_window.geometry("300x150")
    
    label = tk.Label(input_window, text=f"Zadajte hodnotu pre {title}:")
    label.pack(pady=10)
    
    entry = tk.Entry(input_window)
    entry.pack(pady=10)
    
    def ok_action():
        try:
            value = int(entry.get())  # Získať hodnotu z textového poľa a konvertovať na celé číslo
            callback(value)  # Zavolať príslušný callback na uloženie hodnoty
            print(f"Zadaná hodnota pre {title}:", value)  # Vypíše zadanú hodnotu do konzoly
            
            # Podmienka: ak hodnota pre Start Value > 300, zmeniť farbu tlačidla na červenú
            if title == "Start Value" and value > 300:
                start_button.config(bg="red")
            else:
                start_button.config(bg="SystemButtonFace")  # Obnoviť pôvodnú farbu tlačidla

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

root = tk.Tk()
root.title("Simple GUI")
root.geometry("400x300")

# Vytvorenie tlačidiel
start_button = tk.Button(root, text="FAST", command=start_action)
end_button = tk.Button(root, text="MEDIUM", command=end_action)
generic_button = tk.Button(root, text="SLOW", command=button_action)

# Umiestnenie tlačidiel pod sebou
start_button.pack(pady=10)
end_button.pack(pady=10)
generic_button.pack(pady=10)

root.mainloop()
