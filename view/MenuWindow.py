import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox

from service.OrderService import OrderService


class MenuWindow:
    order_dishes = []

    def __init__(self, root):
        self.root = root
        # setting title
        root.title("Menu")
        # setting window size
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_260 = tk.Label(root)
        ft = tkFont.Font(family='Times', size=38)
        GLabel_260["font"] = ft
        GLabel_260["fg"] = "#333333"
        GLabel_260["justify"] = "center"
        GLabel_260["text"] = "Menu"
        GLabel_260["relief"] = "flat"
        GLabel_260.place(x=160, y=70, width=257, height=63)

        order_button = tk.Button(root)
        order_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        order_button["font"] = ft
        order_button["fg"] = "#000000"
        order_button["justify"] = "center"
        order_button["text"] = "Order"
        order_button.place(x=380, y=430, width=208, height=54)
        order_button["command"] = self.make_order

        back_button = tk.Button(root)
        back_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        back_button["font"] = ft
        back_button["fg"] = "#000000"
        back_button["justify"] = "center"
        back_button["text"] = "Back"
        back_button.place(x=20, y=20, width=70, height=25)
        back_button["command"] = self.show_main_window

        text_to_pay = tk.Label(root)
        ft = tkFont.Font(family='Times', size=16)
        text_to_pay["font"] = ft
        text_to_pay["fg"] = "#333333"
        text_to_pay["justify"] = "center"
        text_to_pay["text"] = "To pay: 0 UAH"
        text_to_pay.place(x=120, y=430, width=238, height=52)
        self.text_to_pay = text_to_pay

        items = tk.Listbox(root, selectmode="multiple")
        items["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        items["font"] = ft
        items["fg"] = "#333333"
        items["justify"] = "center"
        items.place(x=10, y=170, width=577, height=248)
        items.bind('<<ListboxSelect>>', self.items_select)
        self.dishes = OrderService().get_dishes()
        for dish in self.dishes:
            items.insert("end", dish.name + " " + str(dish.price) + " UAH")

    def make_order(self):
        try:
            OrderService().order(self.order_dishes)
            messagebox.showinfo("Success", "Your order was created!")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def show_main_window(self):
        from view.MainWindow import MainWindow

        self.root.destroy()  # close the current window
        self.root = tk.Tk()  # create another Tk instance
        self.app = MainWindow(self.root)  # create Demo2 window
        self.root.mainloop()

    def items_select(self, event):
        w = event.widget
        price = 0
        self.order_dishes = []
        for i in w.curselection():
            dish = self.dishes[i]
            price += dish.price
            dish.count = 1
            self.order_dishes.append(dish)
        self.text_to_pay["text"] = "To pay: " + str(price) + " UAH"
