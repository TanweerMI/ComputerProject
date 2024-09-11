import mysql.connector
import tkinter as tk
from tkinter import ttk

con = mysql.connector.connect(host='localhost',user='root',password='torgius',database='tanweer12k')
cur=con.cursor()

l=[]
rowno=1
quantity=1

def scanned(itemname):
    global rowno,quantity,l
    try:
        itna = ttk.Label(master=item_frame, text=l[0])
        price = ttk.Label(master=item_frame, text=l[1])
        info = ttk.Label(master=item_frame, text=l[2])
        qty = ttk.Label(master=item_frame, text=l[3])
        total = ttk.Label(master=item_frame, text=l[4])
        itna.grid(row=rowno,column=0)
        price.grid(row=rowno,column=1)
        info.grid(row=rowno,column=2)
        qty.grid(row=rowno,column=3)
        total.grid(row=rowno,column=4)
    
        rowno+=1

        item_frame.pack(pady=20)
    except:
        pass

    l.clear()

    cur.execute('select * from Items')
    for i in cur.fetchall():
        if i[1]==itemname:    
            l=[i[1],str(i[2]),i[3],str(quantity),str(quantity*i[2])]
            break

def inc():
    global quantity
    l[4]=str(float(l[4])/quantity)
    quantity+=1
    l[3]=str(quantity)
    l[4]=str(float(l[4])*quantity)
    
def dec():
    global quantity
    l[4]=str(float(l[4])/quantity)
    quantity-=1
    l[3]=str(quantity)
    l[4]=str(float(l[4])*quantity)

def rem():
    #remove last item
    pass

window = tk.Tk()
window.title('Menu')
window.geometry('1000x700')
title_label = ttk.Label(master=window, text='SCANNED ITEMS', font='TimesNewRoman 24 bold')
title_label.pack()
input_frame = ttk.Frame(master=window)
qty_increase = ttk.Button(master=input_frame, text='INC', command=inc)
qty_decrease = ttk.Button(master=input_frame, text='DEC', command=dec)
#change command
remove_last = ttk.Button(master=input_frame, text='REMOVE', command=lambda: scanned('Regular-Tomato'))
qty_increase.grid(row=0,column=0,padx=10)
qty_decrease.grid(row=0,column=1,padx=10)
remove_last.grid(row=1, column=0,columnspan=2,pady=10,sticky='we')
input_frame.pack(side='right')

item_frame = ttk.Frame(master=window)
itemname = ttk.Label(master=item_frame, text='Item Name', font='TimesNewRoman 18 bold')
price = ttk.Label(master=item_frame, text='Price',font='TimesNewRoman 18 bold')
info = ttk.Label(master=item_frame, text='Info',font='TimesNewRoman 18 bold')
qty = ttk.Label(master=item_frame, text='Quantity',font='TimesNewRoman 18 bold')
total = ttk.Label(master=item_frame, text='Total',font='TimesNewRoman 18 bold')
itemname.grid(row=0,column=0)
price.grid(row=0,column=1,padx=40)
info.grid(row=0,column=2,padx=110)
qty.grid(row=0,column=3,padx=10)
total.grid(row=0,column=4,padx=10)
item_frame.pack(side='left')

window.mainloop()

con.close()