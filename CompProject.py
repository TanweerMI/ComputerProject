import mysql.connector
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
from tkinter import messagebox

con = mysql.connector.connect(host='localhost', user='root', password='torgius', database='tanweer12k')
cur = con.cursor()
cur.execute('delete from receipt')


def Menu():
    menu_items = {
    "Salad": ["Greek Salad", "Caesar Salad"],
    "Drink": ["Coke", "Lemonade"],
    "Main Course": ["Grilled Chicken", "Fried Rice"],
    "Dessert": ["Ice Cream", "Brownie"]
    }

    basket=[]

    def open_category_window(category):
        category_window = tk.Toplevel(root)
        category_window.title(f"Choose an item from {category}")
        category_window.geometry("300x200")
        
        label = tk.Label(category_window, text=f"Select a {category}", font=("Arial", 14))
        label.pack(pady=10)
        
        selected_item = tk.StringVar(master=category_window)
        dropdown = ttk.Combobox(category_window, textvariable=selected_item, font=("Arial", 12), state="readonly")
        dropdown['values'] = menu_items[category]
        dropdown.pack(pady=10)

        def confirm_selection():
            if selected_item.get():
                basket.append(selected_item.get())
                category_window.destroy()
                messagebox.showinfo("Added to Basket", f"{selected_item.get()} added to basket!")

        confirm_button = tk.Button(category_window, text="Select", font=("Arial", 12), command=confirm_selection)
        confirm_button.pack(pady=10)

    root = ttk.Window(themename='minty')
    root.title("Menu Selector")
    root.geometry("700x860")

    title_label = tk.Label(root, text="Select a Category", font=("Arial Bold", 20))
    title_label.pack(pady=20)

    for category in menu_items:
        button = tk.Button(root, text=category, font=("Arial", 14), width=15, command=lambda c=category: open_category_window(c))
        button.pack(pady=10)
    button = tk.Button(root, text='Proceed To Basket', font=("Arial", 14), width=15, command=lambda:GUI(basket))
    button.pack(pady=30)

    def GUI(basket):
        window = tk.Toplevel(root)
        window.title('Menu')
        window.geometry('1100x800')

        title_label = ttk.Label(master=window, text='SCANNED ITEMS', font='TimesNewRoman 24 bold')
        title_label.pack()

        input_frame = ttk.Frame(master=window)
        qty_increase = ttk.Button(master=input_frame, text='INC')
        qty_decrease = ttk.Button(master=input_frame, text='DEC')
        remove_last = ttk.Button(master=input_frame, text='REMOVE')
        confirm_button = ttk.Button(master=input_frame, text='CONFIRM')
        receipt_button = ttk.Button(master=input_frame, text='CHECKOUT')

        qty_increase.grid(row=0, column=0, padx=15, pady=15, columnspan=2, sticky='we')
        qty_decrease.grid(row=1, column=0, padx=15, pady=15, columnspan=2, sticky='we')
        remove_last.grid(row=2, column=0, columnspan=2, pady=15, sticky='we')
        confirm_button.grid(row=3, column=0, columnspan=2, pady=15, sticky='we')
        receipt_button.grid(row=4, column=0, columnspan=2, pady=15, sticky='we')

        input_frame.pack(side='right', fill='y', padx=20, pady=150)

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

        rowno = 1
        confirmed = False
        index=0
        l = []
        inserted = ''

        def scanned(name):
            nonlocal rowno, l, confirmed
            if confirmed == False and rowno!=1:
                return None
            
            confirmed = False
            l.clear()

            cur.execute('select * from Items')
            for i in cur.fetchall():
                if i[1] == name:
                    l = [i[1], str(i[2]), i[3]]
                    break
            
            quantity = tk.IntVar(window, 1)
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
                nonlocal confirmed, rowno
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
                nonlocal confirmed, index, inserted
                confirmed = True
                if inserted!=l[0]:
                    cur.execute(f"insert into receipt values('{l[0]}',{float(l[1])},'{l[2]}',{quantity.get()},{total_var.get()})")
                    con.commit()
                    inserted=l[0]
                print(inserted)
                if index < len(basket) - 1:
                    index += 1
                    scanned(basket[index])

            def receipt():
                nonlocal confirmed
                if confirmed == False:
                    cur.execute(f"insert into receipt values('{l[0]}',{float(l[1])},'{l[2]}',{quantity.get()},{float(total_var.get())})")
                    con.commit()
                window.destroy()
                final()
            
            qty_increase.config(command=inc)
            qty_decrease.config(command=dec)
            remove_last.config(command=rem)
            confirm_button.config(command=confirm)
            receipt_button.config(command=receipt)

            rowno += 1
            item_frame.pack(pady=20)
        
        if basket:
            scanned(basket[0])
        
        item_frame.pack(side='left')
        window.mainloop()

    def final():
        receipt = ttk.Toplevel(root)
        receipt.title('Receipt')
        receipt.geometry('400x460')
        receipt.configure(bg='#3b3b3b')
        pri=0
        total=0
        cur.execute('select * from receipt')
        rec = cur.fetchall()
        for i in rec:
            pri+=int(i[4])
            total+=int(i[3])
        price = ttk.Label(master=receipt, text=f'TOTAL: {pri}$', font='TimesNewRoman 18 bold', background='#3b3b3b', foreground='white')
        tot = ttk.Label(master=receipt, text=f'ITEMS PURCHASED: {total}', font='TimesNewRoman 18 bold', background='#3b3b3b', foreground='white')
        price.pack()
        tot.pack()

    root.mainloop()

Menu()

con.close()
