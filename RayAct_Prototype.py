import tkinter as tk
import time
import random

root = tk.Tk()
root.title("Reaction Time Test")
root.geometry("800x500")

frame = tk.Frame(root, bg = "red")
frame.pack(fill="both",expand = True)

label_timer_value = tk.Label(
    frame,
    text = "0000",
    font = ("Arial", 48),
    bg = "red",
    fg = "white"
)
 
label_timer_value.pack(pady=(120,0))
 
label_timer_unit = tk.Label (
    frame,
    text = "milliseconds",
    font=("Arial", 16),
    bg = "red",
    fg = "white"
)
label_timer_unit.pack()

label_instruction = tk.Label(
    frame,
    text = "Click when the screen turns Green",
    font = ("Arial", 18),
    bg = "red",
    fg = "white"
)
label_instruction.pack(pady=40)

# State Variables
test_started = False
go_time= None

# Start test after random delay

def start_test():
        global go_time, test_started

        frame.config(bg="green")
        label_timer_value.config(text="0000")
        label_instruction.config(text="click")

        go_time = time.perf_counter()
        test_started = True        

# early click message

def early_click():
    label_instruction.config(text="you clicked too soon")

# valid clicks

def on_click(event):
      global test_started

      if not test_started:
            early_click()
            return
      
      reaction_time = (time.perf_counter() - go_time)*1000
      reaction_time = int(reaction_time)

      label_timer_value.config(text=str(reaction_time))
      label_instruction.config(text="click when screen turns Green")

frame.config(bg="red")
test_started = False

# to restart after delay
root.after(random.randint(2000,5000),start_test)

# binding click
frame.bind("<Button-1>", on_click)
 
root.mainloop()
