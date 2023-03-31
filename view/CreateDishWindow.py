import tkinter as tk
from tkinter import messagebox, ttk

from service.IngredientService import IngredientService
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

        label = ttk.Label(root, text="Введіть назву:")
        label.pack()

        entry = ttk.Entry(root)
        entry.pack()

        list_label = ttk.Label(root, text="Виберіть елементи:")
        list_label.pack()

        items = tk.Listbox(root, selectmode=tk.MULTIPLE)
        items.pack()

        items.bind('<<ListboxSelect>>', self.items_select)
        self.ingredients = IngredientService().get_ingredients()
        for i in self.ingredients:
            items.insert("end", i.name)

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
