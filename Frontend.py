import tkinter as tk
import requests
from bs4 import BeautifulSoup
from string import punctuation
from tkinter import ttk
import pandas as pd

HEIGHT = 500
WIDTH = 600

def test_function(entry):
	print("This is the entry:", entry)

# api.openweathermap.org/data/2.5/forecast?q={city name},{country code}
# a4aa5e3d83ffefaba8c00284de6ef7c3
def counter(it):
    counts = {}
    for item in it:
        counts[item] = counts.get(item, 0) + 1
    return counts

def get_frequency(url):
	r = requests.get(url)

	soup = BeautifulSoup(r.content)

	text = (''.join(s.findAll(text=True))for s in soup.findAll('p'))

	c = counter((x.rstrip(punctuation).lower() for y in text for x in y.split()))

	ans=sorted(c.values(),reverse=True)
	sorted_dict = {}

	for i in ans:
	    for k in c.keys():
	        if c[k] == i:
	            sorted_dict[k] = c[k]
	            break
	lst_1=list(sorted_dict.keys())
	lst_2=list(sorted_dict.values())
	temp = {'Words':lst_1[:10],'Count':lst_2[:10]}
	df=pd.DataFrame(temp)

	clear_data()

	tv1["column"] = list(df.columns)
	tv1["show"] = "headings"
	for column in tv1["columns"]:
		tv1.heading(column, text=column) # let the column heading = column name
	
	df_rows = df.to_numpy().tolist()
	for row in df_rows:
		tv1.insert("", "end", values=row) 
	return None
def clear_data():
	tv1.delete(*tv1.get_children())
	return None



root = tk.Tk()


canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image = tk.PhotoImage(file='landscape.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

entry = tk.Entry(frame, font=40)
entry.place(relwidth=0.65, relheight=1)

button = tk.Button(frame, text="Submit", font=40, command=lambda: get_frequency(entry.get()))
button.place(relx=0.7, relheight=1, relwidth=0.3)

lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
lower_frame.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6,anchor='n')


#label = tk.Label(lower_frame)
#label.place(relwidth=1, relheight=1)

tv1 = ttk.Treeview(lower_frame)
tv1.place(relheight=1, relwidth=1) # set the height and width of the widget to 100% of its container (frame1).

treescrolly = tk.Scrollbar(lower_frame, orient="vertical", command=tv1.yview) # command means update the yaxis view of the widget
treescrollx = tk.Scrollbar(lower_frame, orient="horizontal", command=tv1.xview) # command means update the xaxis view of the widget
tv1.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set) # assign the scrollbars to the Treeview Widget
treescrollx.pack(side="bottom", fill="x") # make the scrollbar fill the x axis of the Treeview widget
treescrolly.pack(side="right", fill="y") # make the scrollbar fill the y axis of the Treeview widget

root.mainloop()