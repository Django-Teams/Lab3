import tkinter as tk
import tkinter.font as tkFont
from tkinter import messagebox

from model.Dish import Dish
from repository.DishRepository import DishRepository
from service.IngredientService import IngredientService
from service.OrderService import OrderService


class AdminWindow:
    selected_ingredients = []
    update_selected_ingredients = []

    def __init__(self, root):
        self.root = root
        # setting title
        root.title("Admin")
        # setting window size
        width = 600
        height = 500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        title_text = tk.Label(root)
        ft = tkFont.Font(family='Times', size=38)
        title_text["font"] = ft
        title_text["fg"] = "#333333"
        title_text["justify"] = "center"
        title_text["text"] = "Admin"
        title_text["relief"] = "flat"
        title_text.place(x=160, y=70, width=257, height=63)

        create_button = tk.Button(root)
        create_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        create_button["font"] = ft
        create_button["fg"] = "#000000"
        create_button["justify"] = "center"
        create_button["text"] = "Create"
        create_button.place(x=40, y=410, width=208, height=54)
        create_button["command"] = self.create_dish

        back_button = tk.Button(root)
        back_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        back_button["font"] = ft
        back_button["fg"] = "#000000"
        back_button["justify"] = "center"
        back_button["text"] = "Back"
        back_button.place(x=20, y=20, width=70, height=25)
        back_button["command"] = self.show_main_window

        name_input = tk.Entry(root)
        name_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        name_input["font"] = ft
        name_input["fg"] = "#333333"
        name_input["justify"] = "center"
        name_input.place(x=20, y=140, width=247, height=37)

        self.name_input = name_input

        create_items = tk.Listbox(root, selectmode="multiple")
        create_items["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        create_items["font"] = ft
        create_items["fg"] = "#333333"
        create_items["justify"] = "center"
        create_items.place(x=20, y=190, width=246, height=176)
        create_items.bind('<<ListboxSelect>>', self.create_items_select)
        self.ingredients = IngredientService().get_ingredients()
        for i in self.ingredients:
            create_items.insert("end", i.name)

        edit_dishes = tk.Listbox(root)
        edit_dishes["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        edit_dishes["font"] = ft
        edit_dishes["fg"] = "#333333"
        edit_dishes["justify"] = "center"
        edit_dishes.place(x=310, y=140, width=267, height=322)
        edit_dishes.bind('<<ListboxSelect>>', self.edit_dish_select)
        self.dishes = OrderService().get_dishes()
        self.edit_dishes = edit_dishes
        for dish in self.dishes:
            edit_dishes.insert("end", dish.name + " " + str(dish.price) + " UAH")

        price_text = tk.Label(root)
        ft = tkFont.Font(family='Times', size=12)
        price_text["font"] = ft
        price_text["fg"] = "#333333"
        price_text["justify"] = "center"
        price_text["text"] = "Price: 0 UAH"
        price_text.place(x=50, y=370, width=185, height=30)
        self.price_text = price_text

    def create_dish(self):
        try:
            name = self.name_input.get()
            dish = Dish(name, self.selected_ingredients)
            DishRepository().create(dish)
            messagebox.showinfo("Success", "Your dish was created!")
            self.dishes.append(dish)
            price = 0
            for ing in dish.ingredients:
                price += round((ing.price * ing.count / 1000) * (100 + OrderService.MARKUP) / 100)
            self.edit_dishes.insert("end", dish.name + " " + str(price) + " UAH")
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def show_main_window(self):
        from view.MainWindow import MainWindow

        self.root.destroy()  # close the current window
        self.root = tk.Tk()  # create another Tk instance
        self.app = MainWindow(self.root)  # create Demo2 window
        self.root.mainloop()

    def create_items_select(self, event):
        w = event.widget
        price = 0
        self.selected_ingredients = []
        for i in w.curselection():
            ing = self.ingredients[i]
            ing.count = 200
            price += round((ing.price * ing.count / 1000) * (100 + OrderService.MARKUP) / 100)
            self.selected_ingredients.append(ing)
        self.price_text["text"] = "Price: " + str(price) + " UAH"

    def edit_dish_select(self, event):
        w = event.widget
        try:
            dish = self.dishes[w.curselection()[0]]
            self.lastDishIdx = w.curselection()[0];
            self.update_dish = dish
        except:
            return
        self.selected_ingredients = []
        edit_window = tk.Toplevel()
        edit_window.title("Update dish")
        width = 300
        height = 400
        screenwidth = edit_window.winfo_screenwidth()
        screenheight = edit_window.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        edit_window.geometry(alignstr)
        edit_window.resizable(width=False, height=False)

        update_button = tk.Button(edit_window)
        update_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        update_button["font"] = ft
        update_button["fg"] = "#000000"
        update_button["justify"] = "center"
        update_button["text"] = "Update"
        update_button.place(x=40, y=310, width=208, height=25)
        update_button["command"] = self.change_dish

        delete_button = tk.Button(edit_window)
        delete_button["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        delete_button["font"] = ft
        delete_button["fg"] = "#000000"
        delete_button["justify"] = "center"
        delete_button["text"] = "Delete"
        delete_button.place(x=40, y=340, width=208, height=25)
        delete_button["command"] = self.delete_dish

        update_name_input = tk.Entry(edit_window)
        update_name_input["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        update_name_input["font"] = ft
        update_name_input["fg"] = "#333333"
        update_name_input["justify"] = "center"
        update_name_input.insert(0, dish.name)
        update_name_input.place(x=20, y=40, width=247, height=37)

        self.update_name_input = update_name_input

        update_create_items = tk.Listbox(edit_window, selectmode="multiple")
        update_create_items["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times', size=10)
        update_create_items["font"] = ft
        update_create_items["fg"] = "#333333"
        update_create_items["justify"] = "center"
        update_create_items.place(x=20, y=90, width=246, height=176)
        update_create_items.bind('<<ListboxSelect>>', self.update_items_select)
        self.update_ingredients = IngredientService().get_ingredients()
        for i in self.ingredients:
            update_create_items.insert("end", i.name)
        for ing, count in dish.ingredients:
            for i in self.ingredients:
                if i.name == ing.name:
                    update_create_items.selection_set(self.ingredients.index(i))

        price = 0
        for ing, count in dish.ingredients:
            price += round((ing.price * count / 1000) * (100 + OrderService.MARKUP) / 100)
        price_text = tk.Label(edit_window)
        ft = tkFont.Font(family='Times', size=12)
        price_text["font"] = ft
        price_text["fg"] = "#333333"
        price_text["justify"] = "center"
        price_text["text"] = "Price: " + str(price) + " UAH"
        price_text.place(x=50, y=270, width=185, height=30)
        self.update_price_text = price_text

    def change_dish(self):
        try:
            self.dishes.remove(self.update_dish)
            self.update_dish.name = self.update_name_input.get()
            self.update_dish.ingredients = self.update_selected_ingredients
            DishRepository().update(self.update_dish)
            messagebox.showinfo("Success", "Your dish was updated!")
            price = 0
            for ing in self.update_dish.ingredients:
                price += round((ing.price * ing.count / 1000) * (100 + OrderService.MARKUP) / 100)
            self.edit_dishes.delete(self.lastDishIdx)
            self.edit_dishes.insert("end", self.update_dish.name + " " + str(price) + " UAH")
            self.root.destroy()  # close the current window
            self.root = tk.Tk()  # create another Tk instance
            self.app = AdminWindow(self.root)  # create Demo2 window
            self.root.mainloop()
        except Exception as ex:
            messagebox.showerror("Error", str(ex))

    def delete_dish(self):
        try:
            self.dishes.remove(self.update_dish)
            DishRepository().delete(self.update_dish)
            messagebox.showinfo("Success", "Your dish was deleted!")
            self.edit_dishes.delete(self.lastDishIdx)
        except Exception as ex:
            text = str(ex)
            if ex.args[0] == 1451:
                text = "You cant delete dish, its was ordered"
            messagebox.showerror("Error", text)

    def update_items_select(self, event):
        w = event.widget
        price = 0
        self.update_selected_ingredients = []
        for i in w.curselection():
            ing = self.update_ingredients[i]
            ing.count = 200
            price += round((ing.price * ing.count / 1000) * (100 + OrderService.MARKUP) / 100)
            self.update_selected_ingredients.append(ing)
        self.update_price_text["text"] = "Price: " + str(price) + " UAH"
