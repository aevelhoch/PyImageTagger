import tkinter as tk

def fToC():
	fTemp = entTemp.get()
	cTemp = (5/9) * (float(fTemp) - 32)
	lblResult["text"] = f"{round(cTemp, 2)} \N{DEGREE CELSIUS}"

window = tk.Tk()
window.title("Temperature Converter")

frmEntry = tk.Frame(master=window)
entTemp = tk.Entry(master=frmEntry, width=10)
lblTemp = tk.Label(frmEntry, text="\N{DEGREE FAHRENHEIT}")

entTemp.grid(row=0, column=0, sticky="e")
lblTemp.grid(row=0, column=1, sticky="w")

btnConvert = tk.Button(
	master=window, 
	text="\N{RIGHTWARDS BLACK ARROW}",
	command=fToC)
lblResult = tk.Label(master=window, text="\N{DEGREE CELSIUS}")

frmEntry.grid(row=0, column=0, padx=10)
btnConvert.grid(row=0, column=1, pady=10)
lblResult.grid(row=0, column=2, padx=10)

window.mainloop()