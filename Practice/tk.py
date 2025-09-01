from tkinter import *

# import streamlit as st
class Amit_ML:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x700+0+0")
        self.root.title("RAWNAA GUI")
        self.root.configure(bg="white")
        self.icon_title = PhotoImage(
            file="")
        title = Label(self.root, text="RAWNAA", image=self.icon_title, compound=LEFT,
                      font=("time new roman", 40, "bold"), bg="#010c48", fg="white", anchor="w", padx=20).place(x=0, y=0, relwidth=1, height=70)
        btn_logout = Button(self.root, text="Logout", font=(
            "times new roman", 15, "bold"), bg="white", cursor="hand2").place(x=1150, y=10, height=50, width=150)
        # self.lbl_clock = Label(
        #     self.root, text="Welcome to Inventory Management System \t\t Dat:DD-MM-YYYY\t\t Time: HH:MM:SS", font=("times new roman", 15), bg="#4d636d", fg="white")
        # self.lbl_clock.place(x=3, y=70, relwidth=0.2, height=120)



if __name__ == "__main__":
    root = Tk()
    obj = Amit_ML(root)
    root.mainloop()
