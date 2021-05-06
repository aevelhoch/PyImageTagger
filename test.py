import tkinter as tk
import random

def rollDie():
	value = random.randrange(1,21)
	lbl_value["text"] = f"{value}"
	
window = tk.Tk()

# set up window
window.rowconfigure([0,1], minsize=50, weight=1)
window.columnconfigure(0, minsize=150, weight=1)

btn_roll = tk.Button(master=window, text="ROLL!", command=rollDie)
btn_roll.grid(row=0, column=0, sticky="nsew")

lbl_value = tk.Label(master=window, text="Press butan to roll d20")
lbl_value.grid(row=1, column=0)


window.mainloop()