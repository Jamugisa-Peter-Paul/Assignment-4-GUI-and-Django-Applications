from tkinter.ttk import Frame, Button, Label, Entry, Style
from tkinter import Toplevel

class StudentIDDlg(Toplevel):
    def __init__(self, initialText, title, labeltext=''):
        Toplevel.__init__(self)
        self.initUI(initialText, title, labeltext)

    def initUI(self, initialText, title, labeltext=''):
        self.STID = initialText
        self.geometry("280x140")
        if len(title) > 0:
            self.title(title)
        self.style = Style()
        self.style.theme_use("default")

        style = Style()
        style.configure("Exit.TButton", foreground="red", background="white")
        style.configure("MainButton.TButton", foreground="yellow", background="red")

        if len(labeltext) == 0:
            labeltext = 'Please enter your ID..'

        xpos = 20
        ypos = 25
        xpos2 = xpos + 140

        Label(self, text=labeltext, foreground="#ff0000", background="light blue", font="Arial 9").place(x=xpos, y=ypos)
        self.txtID = Entry(self)
        self.txtID.place(x=xpos2, y=ypos, width=120)
        self.txtID.bind("<Return>", self.ok)
        self.txtID.bind("<Escape>", self.cancel)
        self.txtID.focus_set()

        ypos += 40
        okButton = Button(self, text="OK", command=self.ok)
        okButton.place(x=xpos2, y=ypos)

    def getID(self):
        return self.STID

    def ok(self, event=None):
        self.STID = self.txtID.get().strip()
        self.destroy()

    def cancel(self, event=None):
        self.destroy()