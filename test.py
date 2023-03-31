import tkinter as tk
import tkinter.font as tkFont

class App:
    def __init__(self, root):
        #setting title
        root.title("undefined")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        GLabel_741=tk.Label(root)
        GLabel_741["anchor"] = "nw"
        GLabel_741["bg"] = "#ffffff"
        GLabel_741["borderwidth"] = "2px"
        ft = tkFont.Font(family='Times',size=10)
        GLabel_741["font"] = ft
        GLabel_741["fg"] = "#333333"
        GLabel_741["justify"] = "left"
        GLabel_741["text"] = "output text goes here"
        GLabel_741["relief"] = "ridge"
        GLabel_741.place(x=10,y=280,width=580,height=210)

        GButton_957=tk.Button(root)
        GButton_957["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_957["font"] = ft
        GButton_957["fg"] = "#000000"
        GButton_957["justify"] = "center"
        GButton_957["text"] = "Button"
        GButton_957.place(x=20,y=240,width=70,height=25)
        GButton_957["command"] = self.GButton_957_command

        GButton_46=tk.Button(root)
        GButton_46["bg"] = "#f0f0f0"
        ft = tkFont.Font(family='Times',size=10)
        GButton_46["font"] = ft
        GButton_46["fg"] = "#000000"
        GButton_46["justify"] = "center"
        GButton_46["text"] = "Button"
        GButton_46.place(x=110,y=240,width=70,height=25)
        GButton_46["command"] = self.GButton_46_command

        GListBox_533=tk.Listbox(root)
        GListBox_533["borderwidth"] = "1px"
        ft = tkFont.Font(family='Times',size=10)
        GListBox_533["font"] = ft
        GListBox_533["fg"] = "#333333"
        GListBox_533["justify"] = "center"
        GListBox_533.place(x=20,y=20,width=247,height=101)

    def GButton_957_command(self):
        print("command")


    def GButton_46_command(self):
        print("command")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
