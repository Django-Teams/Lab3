import tkinter as tk
import tkinter.font as tkFont


class MainWindow:
    def __init__(self, root):
        self.root = root
        # setting title
        root.title("Restaurant")
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
        GLabel_260["text"] = "Restaurant"
        GLabel_260["relief"] = "flat"
        GLabel_260.place(x=170, y=80, width=250, height=50)

        GButton_563 = tk.Button(root)
        GButton_563["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        GButton_563["font"] = ft
        GButton_563["fg"] = "#000000"
        GButton_563["justify"] = "center"
        GButton_563["text"] = "Menu"
        GButton_563.place(x=140, y=260, width=130, height=51)
        GButton_563["command"] = self.show_menu_window

        GButton_683 = tk.Button(root)
        GButton_683["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times', size=10)
        GButton_683["font"] = ft
        GButton_683["fg"] = "#000000"
        GButton_683["justify"] = "center"
        GButton_683["text"] = "Admin"
        GButton_683.place(x=310, y=260, width=130, height=52)
        GButton_683["command"] = self.show_admin_window

    def show_menu_window(self):
        from view.MenuWindow import MenuWindow

        self.root.destroy()  # close the current window
        self.root = tk.Tk()  # create another Tk instance
        self.app = MenuWindow(self.root)  # create Demo2 window
        self.root.mainloop()

    def show_admin_window(self):
        from view.AdminWindow import AdminWindow

        self.root.destroy()  # close the current window
        self.root = tk.Tk()  # create another Tk instance
        self.app = AdminWindow(self.root)  # create Demo2 window
        self.root.mainloop()
