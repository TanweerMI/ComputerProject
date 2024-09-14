import mysql.connector
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk

con = mysql.connector.connect(host='localhost', user='root', password='torgius', database='tanweer12k')
cur = con.cursor()
cur.execute('delete from receipt')

l = []
rowno = 1
confirmed = False

#call this function after scanning, with label name as argument
def scanned(itemname):
    global rowno, l, confirmed

    if confirmed == False and rowno!=1:
        return None
    
    confirmed = False
    l.clear()
    quantity = tk.IntVar(window, 1)

    separator1 = ttk.Separator(master=item_frame, orient='vertical')
    separator2 = ttk.Separator(master=item_frame, orient='vertical')
    separator3 = ttk.Separator(master=item_frame, orient='vertical')
    separator4 = ttk.Separator(master=item_frame, orient='vertical')

    separator1.grid(row=rowno, column=1, sticky='ns', padx=5, pady=5)
    separator2.grid(row=rowno, column=3, sticky='ns', padx=5, pady=5)
    separator3.grid(row=rowno, column=5, sticky='ns', padx=5, pady=5)
    separator4.grid(row=rowno, column=7, sticky='ns', padx=5, pady=5)

    cur.execute('select * from Items')
    for i in cur.fetchall():
        if i[1] == itemname:
            l = [i[1], str(i[2]), i[3]]
            break
    
    total_var = tk.DoubleVar(window, float(l[1]))

    itna = ttk.Label(master=item_frame, text=l[0])
    price = ttk.Label(master=item_frame, text=l[1])
    info = ttk.Label(master=item_frame, text=l[2])
    qty = ttk.Label(master=item_frame, textvariable=quantity)
    total = ttk.Label(master=item_frame, textvariable=total_var)

    itna.grid(row=rowno, column=0)
    price.grid(row=rowno, column=2)
    info.grid(row=rowno, column=4)
    qty.grid(row=rowno, column=6)
    total.grid(row=rowno, column=8)

    def inc():
        quantity.set(quantity.get() + 1)
        total_var.set(quantity.get() * float(l[1]))

    def dec():
        if quantity.get() > 1:
            quantity.set(quantity.get() - 1)
            total_var.set(quantity.get() * float(l[1]))

    def rem():
        global confirmed, rowno
        cur.execute(f"delete from receipt where item_name = '{l[0]}'")
        con.commit()
        itna.destroy()
        price.destroy()
        info.destroy()
        qty.destroy()
        total.destroy()
        confirmed = True
        rowno-=1
    
    def confirm():
        global confirmed
        confirmed = True
        cur.execute(f"insert into receipt values('{l[0]}',{float(l[1])},'{l[2]}',{quantity.get()},{total_var.get()})")
        con.commit()

    def receipt():
        if confirmed == False:
            cur.execute(f"insert into receipt values('{l[0]}',{float(l[1])},'{l[2]}',{quantity.get()},{float(total_var.get())})")
            con.commit()

    qty_increase.config(command=inc)
    qty_decrease.config(command=dec)
    remove_last.config(command=rem)
    confirm_button.config(command=confirm)
    receipt_button.config(command=receipt)

    rowno += 1

    item_frame.pack(pady=20)

window = ttk.Window(themename = 'darkly')
window.title('Menu')
window.geometry('1100x800')

title_label = ttk.Label(master=window, text='SCANNED ITEMS', font='TimesNewRoman 24 bold')
title_label.pack()

input_frame = ttk.Frame(master=window)
qty_increase = ttk.Button(master=input_frame, text='INC')
qty_decrease = ttk.Button(master=input_frame, text='DEC')
remove_last = ttk.Button(master=input_frame, text='REMOVE')
test_button = ttk.Button(master=input_frame, text='TESTING',command=lambda: scanned('Regular-Tomato'))
confirm_button = ttk.Button(master=input_frame, text='CONFIRM')
receipt_button = ttk.Button(master=input_frame, text='CHECKOUT')


qty_increase.grid(row=0, column=0, padx=15, pady=15)
qty_decrease.grid(row=0, column=1, padx=15, pady=15)
remove_last.grid(row=1, column=0, columnspan=2, pady=15, sticky='we')
test_button.grid(row=2, column=0, columnspan=2, pady=15, sticky='we')
confirm_button.grid(row=3, column=0, columnspan=2, pady=15, sticky='we')
receipt_button.grid(row=4, column=0, columnspan=2, pady=15, sticky='we')

input_frame.pack(side='right')

item_frame = ttk.Frame(master=window)

itemname = ttk.Label(master=item_frame, text='Item Name', font='TimesNewRoman 18 bold')
price = ttk.Label(master=item_frame, text='Price', font='TimesNewRoman 18 bold')
info = ttk.Label(master=item_frame, text='Info', font='TimesNewRoman 18 bold')
qty = ttk.Label(master=item_frame, text='Quantity', font='TimesNewRoman 18 bold')
total = ttk.Label(master=item_frame, text='Total', font='TimesNewRoman 18 bold')

itemname.grid(row=0, column=0)
price.grid(row=0, column=2, padx=40)
info.grid(row=0, column=4, padx=110)
qty.grid(row=0, column=6, padx=10)
total.grid(row=0, column=8, padx=10)

separator1 = ttk.Separator(master=item_frame, orient='vertical')
separator2 = ttk.Separator(master=item_frame, orient='vertical')
separator3 = ttk.Separator(master=item_frame, orient='vertical')
separator4 = ttk.Separator(master=item_frame, orient='vertical')

separator1.grid(row=0, column=1, sticky='ns', padx=5, pady=5)
separator2.grid(row=0, column=3, sticky='ns', padx=5, pady=5)
separator3.grid(row=0, column=5, sticky='ns', padx=5, pady=5)
separator4.grid(row=0, column=7, sticky='ns', padx=5, pady=5)

item_frame.pack(side='left')

window.mainloop()

con.close()
