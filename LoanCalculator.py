import sys
from tkinter import Tk
from MyFrame import MyFrame

def main():
    root = Tk()
    root.geometry("380x420")
    app = MyFrame(root)  # creates the frame
    root.mainloop()

if __name__ == "__main__":
    sys.exit(int(main() or 0))