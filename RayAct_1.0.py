import tkinter as tk
import time
import random
import csv
from PIL import Image, ImageTk, ImageChops
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Experimental setting
TOTAL_TRIALS = 5
current_trial = 0
reaction_times = []

# State variables
test_started = False
go_time = None

# End screen widgets
label_name = None
entry_name = None
save_button = None

# Root and frame
root = tk.Tk()
root.title("RayAct 1.0")
root.geometry("1920x1080")

frame = tk.Frame(root, bg="black")
frame.pack(fill="both", expand=True)

# Logo
def crop_black_border(img):
    bg = Image.new(img.mode, img.size, (0, 0, 0))
    diff = ImageChops.difference(img, bg)
    bbox = diff.getbbox()
    return img.crop(bbox) if bbox else img

logo_image = Image.open(resource_path("rayact_logo.png")).convert("RGB")
logo_image = crop_black_border(logo_image)
logo_image = logo_image.resize((220, 220), Image.LANCZOS)
logo_img = ImageTk.PhotoImage(logo_image)

logo_label = tk.Label(frame, image=logo_img, bg="black", bd=0, highlightthickness=0)
logo_label.image = logo_img
logo_label.place(relx=0.5, rely=0.3, anchor="center")

# Instructions
label_instruction = tk.Label(
    frame,
    text="Fixate on the cross and left click when the screen turns green",
    font=("Arial", 16),
    bg="black",
    fg="white"
)
label_instruction.place(relx=0.5, rely=0.7, anchor="center")

# Developer tag
label_developer = tk.Label(
     frame,
     text="developed by - Argus Rauniyar",
     font = ("Arial",12),
     bg = "black",
     fg = "grey"
)
label_developer.place(relx=0.5, rely=0.9, anchor="center")

# Timer labels
label_timer_value = tk.Label(frame, text="0000", font=("Arial", 48), bg="red", fg="white")
label_timer_unit = tk.Label(frame, text="milliseconds", font=("Arial", 16), bg="red", fg="white")

# Start hidden
label_timer_value.pack_forget()
label_timer_unit.pack_forget()

# Fixation cross
label_fixation = tk.Label(frame, text="+", font=("Arial", 60), fg="white", bg="red")

# Start button
def start_experiment():
    global current_trial
    logo_label.place_forget()
    start_button.place_forget()
    try_again_button.place_forget()
    label_developer.place_forget()

    current_trial = 0
    reaction_times.clear()

    # Show timer
    label_timer_value.pack(pady=(50, 0))
    label_timer_unit.pack(pady=(5, 0))

    frame.config(bg="red")
    label_timer_unit.config(bg="red")
    label_instruction.config(bg="red", text="wait for green")
    label_instruction.place(relx=0.5, rely=0.75, anchor="center")

    show_fixation()

start_button = tk.Button(frame, text="Start", font=("Arial", 20), width=10, command=start_experiment)
start_button.place(relx=0.5, rely=0.6, anchor="center")

# Try again button
try_again_button = tk.Button(frame, text="Try Again", font=("Arial", 18), width=12)

# Fixation and test logic
def show_fixation():
    global test_started
    test_started = False
    frame.config(bg="red")
    label_fixation.config(bg="red")
    label_fixation.place(relx=0.5, rely=0.5, anchor="center")
    root.after(random.randint(2000, 5000), start_test)

def start_test():
    global go_time, test_started
    frame.config(bg="green")
    label_timer_value.config(text="0000", bg="green")
    label_timer_unit.config(bg="green")
    label_instruction.config(text="click", bg="green")
    label_fixation.config(bg="green")
    go_time = time.perf_counter()
    test_started = True

def on_click(event):
    global test_started, current_trial
    if not test_started:
        return
    test_started = False
    current_trial += 1
    reaction_time = int((time.perf_counter() - go_time) * 1000)
    reaction_times.append(reaction_time)
    label_timer_value.config(text=str(reaction_time))
    frame.config(bg="red")
    label_fixation.config(bg="red")
    label_instruction.config(bg="red", text="wait for green")
    label_timer_unit.config(bg="red")
    label_timer_value.config(bg="red")
    if current_trial < TOTAL_TRIALS:
        show_fixation()
    else:
        end_experiment()
      

label_results = tk.Label(frame,text="",font=("Arial",18),fg="white",bg="black",justify="left")

frame.bind("<Button-1>", on_click)

# Experiment end 
def end_experiment():
      
      global entry_name, save_button, label_name

      #hides trial widgets
      label_timer_value.pack_forget()
      label_timer_unit.pack_forget()
      label_instruction.pack_forget()
      label_developer.pack_forget()

      frame.config(bg="black")

      # result text
      result_text = ""
      for i, rt in enumerate(reaction_times, start=1):
            result_text += f"Trial {i}: {rt} ms\n"
    
      if reaction_times:
           avg_time = sum(reaction_times) // len(reaction_times)
      else:
            avg_time = 0

      result_text += f"\nAverage time: {avg_time} ms"

      label_fixation.place_forget()

      label_results.config(text=result_text)
      label_results.place(relx=0.5, rely=0.3, anchor="center")

      try_again_button.place(relx=0.5, rely=0.9, anchor="center")

      #enter participant name
      label_name = tk.Label(frame, text="Enter Name:", font=("Arial", 16), fg = "white", bg="black")
      label_name.place(relx=0.5, rely=0.6, anchor="center")

      entry_name = tk.Entry(frame, font=("Arial",16))
      entry_name.place(relx=0.5,rely=0.7, anchor="center")

      label_timer_value.pack_forget()
      label_timer_unit.pack_forget()
      label_instruction.place_forget()
      label_developer.place_forget()

        #save as csv button
      def save_results():
            name = entry_name.get().strip()
            if not name:
                name = "Anonymous"
                        
                    #data row
            avg_time = sum(reaction_times) // len(reaction_times) if reaction_times else 0
            row = [name] + reaction_times + [avg_time]
                    
                    #save to csv
            with open ("reaction_times.csv", "a", newline="") as f:
                 writer = csv.writer(f)
                 writer.writerow(row)
            label_name.config(text="your results are saved", fg="green")
            entry_name.destroy()
            save_button.destroy()

      save_button = tk.Button(frame, text="Save as .csv", font=("Arial",16), command=save_results)
      save_button.place(relx=0.5, rely=0.78, anchor="center")

# valid clicks

def on_click(event):
      global test_started, current_trial

      if not test_started:
            return
      
      test_started = False
      current_trial+= 1
      
      reaction_time = int((time.perf_counter() - go_time)*1000)
      label_timer_value.config(text=str(reaction_time))

      reaction_times.append(reaction_time)

      frame.config(bg="red")
      label_fixation.config(bg="red")
      label_instruction.config(bg="red", text="wait for green")
      label_timer_unit.config(bg="red")
      label_timer_value.config(bg="red")

      if current_trial < TOTAL_TRIALS:
            show_fixation()
      else:
            end_experiment()

# binding click
frame.bind("<Button-1>", on_click)

# restarting experiment

def restart_experiment():
      global label_name, entry_name, save_button

      try_again_button.place_forget()
      label_results.place_forget()

      if label_name:
            label_name.destroy()
            label_name = None
      
      if entry_name:
            entry_name.destroy()
            entry_name = None

      if save_button:
            save_button.destroy()
            save_button = None

      frame.config(bg="black")

      label_developer.place(relx=0.5, rely=0.9, anchor="center")
      logo_label.place(relx=0.5, rely=0.3, anchor="center")
      start_button.place(relx=0.5, rely=0.6, anchor="center")
      

# Try again button

try_again_button = tk.Button(frame,text="Try Again",font=("Arial",18),width= 12,command=lambda: restart_experiment())

root.mainloop() 