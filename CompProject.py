import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
import threading


basket = []  
confirmed = False

def GUI():
    global window, item_frame, qty_increase, qty_decrease, remove_last, confirm_button

    def scanned(itemname, category, price):
        global basket
        # Check if the item is already in the basket
        for item in basket:
            if item["name"] == itemname and item["category"] == category:
                return  # Item is already added to the basket

        # Add the item to the basket
        basket.append({"name": itemname, "category": category, "quantity": 1, "price": price})
        update_basket_display()  # Update the basket display

    def update_basket_display():
        for widget in item_frame.winfo_children():
            widget.destroy()  # Clear the existing items in the frame

        for index, item in enumerate(basket):
            name_label = ttk.Label(master=item_frame, text=item["name"])
            quantity_label = ttk.Label(master=item_frame, text=item["quantity"])

            inc_button = ttk.Button(master=item_frame, text="+", command=lambda idx=index: change_quantity(idx, 1))
            dec_button = ttk.Button(master=item_frame, text="-", command=lambda idx=index: change_quantity(idx, -1))

            name_label.grid(row=index, column=0, padx=10, pady=5)
            quantity_label.grid(row=index, column=1, padx=10, pady=5)
            inc_button.grid(row=index, column=2, padx=5)
            dec_button.grid(row=index, column=3, padx=5)

        item_frame.pack()

    def change_quantity(index, change):
        if 0 <= index < len(basket):
            basket[index]["quantity"] += change
            if basket[index]["quantity"] <= 0:
                basket.pop(index)  # Remove item if quantity becomes 0 or less
            update_basket_display()

    def confirm_order():
        global confirmed
        confirmed = True
        print("Order confirmed!")
        print(basket)  # Print the basket for demonstration

        displayBill()

    def displayBill():
        bill_window = tk.Toplevel(window)
        bill_window.title("Bill")
        bill_window.geometry("300x400")

        ttk.Label(master=bill_window, text="Your Bill", font="TimesNewRoman 18 bold").pack(pady=10)

        total_cost = 0
        for item in basket:
            item_cost = item["quantity"] * item["price"]
            total_cost += item_cost
            ttk.Label(master=bill_window, text=f"{item['name']} x {item['quantity']} = ${item_cost:.2f}").pack()

        ttk.Label(master=bill_window, text=f"Total: ${total_cost:.2f}", font="TimesNewRoman 16 bold").pack(pady=10)


    # GUI setup
    window = ttk.Window(themename='darkly')
    window.title('Menu')
    window.geometry('1100x800')

    title_label = ttk.Label(master=window, text='Select Your Meal', font='TimesNewRoman 24 bold')
    title_label.pack()

    # Category selection
    category_frame = ttk.Frame(master=window)
    category_frame.pack(pady=20)

    # Add buttons for each category
    ttk.Button(master=category_frame, text='Select Salad', command=lambda: Menu(scanned, window, "Salad")).pack(side='left', padx=10)
    ttk.Button(master=category_frame, text='Select Drink', command=lambda: Menu(scanned, window, "Drink")).pack(side='left', padx=10)
    ttk.Button(master=category_frame, text='Select Main Course', command=lambda: Menu(scanned, window, "Main Course")).pack(side='left', padx=10)
    ttk.Button(master=category_frame, text='Select Dessert', command=lambda: Menu(scanned, window, "Dessert")).pack(side='left', padx=10)

    # Basket and confirm section
    item_frame = ttk.Frame(master=window)

    confirm_button = ttk.Button(master=window, text='Confirm Order', command=confirm_order)
    confirm_button.pack(pady=20)

    window.mainloop()

def Menu(scannedFunc, windoww, category):
    # Define food items for each category
    food_items = {
        "Salad": [
            {"name": "Greek Salad", "price": 4.99, "info": "Fresh veggies with feta cheese"},
            {"name": "Caesar Salad", "price": 5.49, "info": "Romaine lettuce with Caesar dressing"}
        ],
        "Drink": [
            {"name": "Coke", "price": 1.99, "info": "Refreshing soda"},
            {"name": "Lemonade", "price": 2.49, "info": "Freshly squeezed lemons"}
        ],
        "Main Course": [
            {"name": "Grilled Chicken", "price": 10.99, "info": "Succulent grilled chicken breast"},
            {"name": "Fried Rice", "price": 14.99, "info": "Steamy hot fried rice"}
        ],
        "Dessert": [
            {"name": "Ice Cream", "price": 3.99, "info": "Creamy vanilla ice cream"},
            {"name": "Brownie", "price": 4.49, "info": "Chocolate brownie with nuts"}
        ]
    }

    menu_window = tk.Toplevel(windoww)
    menu_window.title(f"{category} Menu")
    menu_window.geometry("400x400")

    ttk.Label(master=menu_window, text=f"{category} Menu", font="TimesNewRoman 20 bold").pack(pady=10)

    def create_item_button(item):
        def button_command():
            scannedFunc(item["name"], category, item["price"])
        return button_command

    for item in food_items[category]:
        item_button = ttk.Button(
            master=menu_window,
            text=f"{item['name']} - ${item['price']}",
            command=create_item_button(item) 
        )
        item_button.pack(pady=5)

if __name__ == "__main__":
    gui_thread = threading.Thread(target=GUI)
    gui_thread.start()
    gui_thread.join()




'''
import mysql.connector
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as ttk
import threading


con = mysql.connector.connect(host='localhost', user='root', password='torgius', database='tanweer12k')
cur = con.cursor()
cur.execute('delete from receipt')

l = []
rowno = 1
confirmed = False


def GUI():
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
            global confirmed
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

    Menu(scanned, window)

    window.mainloop()

def Menu():
    #to do
    pass


if __name__ == "__main__":
    gui_thread = threading.Thread(target=GUI)
    detection_thread = threading.Thread(target=Menu)

    gui_thread.start()
    detection_thread.start()

    gui_thread.join()
    detection_thread.join()

con.close()
'''
