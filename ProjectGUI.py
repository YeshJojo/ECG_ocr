from tkinter import *
from tkinter import filedialog, font, ttk
from PIL import Image, ImageTk
import tkinter.font as font
import deep_OCR
import preProcessor
import phase_Two


class Window(Frame):

    def __init__(self, master=None):
        global myFont
        self.path = str
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Digitize ECG")
        # self.pack(fill=BOTH, expand=1)
        myFont = font.Font(family='Times', size=15)

        left = Frame(self.master, borderwidth=1, relief="solid")
        right = Frame(self.master, borderwidth=1, relief="solid")
        container = Frame(right, borderwidth=1, relief="solid", background="#ffffff")
        box1 = Frame(left, borderwidth=2, width=500, height=280, relief="solid")
        box2 = Frame(left, borderwidth=2, width=500, height=310, relief="solid")

        label1 = Label(container, fg="green", text="Welcome to ECG Signal Recovery - Developed by RVCien!")

        #####function implimentation done here
        rtext = Button(box2, text="Retrieve Text", fg="blue", width=15, height=2,
                       command=lambda: deep_OCR.deepOCR(self.path))
        rgraph = Button(box2, text="Retrieve Graph", fg="Blue", width=15, height=2,
                        command=lambda: preProcessor.preProcessor(self.path))
        saveb = Button(box2, text="Save", fg="dark green", width=15, height=2)
        clearr = Button(box2, text="Clear", fg="red", width=15, height=2,
                        command=lambda: self.clear_text(box1, textbox))
        textbox = Text(container, borderwidth=2, state='disabled')

        saveb['font'] = myFont
        rtext['font'] = myFont
        rgraph['font'] = myFont
        clearr['font'] = myFont
        label1['font'] = myFont

        left.pack(side="left", expand=True, fill="both")
        right.pack(side="right", expand=True, fill="both")
        container.pack(expand=True, fill="both", padx=5, pady=5)
        box1.pack(expand=True, fill="both", padx=10, pady=10)
        box2.pack(expand=True, fill="both", padx=10, pady=10)
        textbox.pack(expand=True, fill="both", padx=10, pady=10)
        textbox.grab_status()

        label1.pack()
        rtext.grid(row=1, column=3, padx=30, pady=40)
        rgraph.grid(row=2, column=3, padx=30, pady=10)
        saveb.grid(row=1, column=5, padx=30, pady=40)
        clearr.grid(row=2, column=5, padx=30, pady=10)

        # creating a menu instance
        menu = Menu(self.master)
        self.master.config(menu=menu)
        file = Menu(menu)

        # adds a command to the menu option, calling it exit, and the
        # command it runs on event is client_exit
        file.add_command(label="Load Img", command=lambda: self.showImg(box1))
        file.add_command(label="Exit", command=self.client_exit)

        # added "file" to our menu
        menu.add_cascade(label="File", menu=file)

    def showImg(self, loc):
        self.path = filedialog.askopenfilename(filetypes=[("Image File", '.jpg')])
        # im = Image.open(path)
        load = Image.open(self.path)
        load = load.resize((525, 305), Image.ANTIALIAS)
        render = ImageTk.PhotoImage(load)

        img = Label(loc, image=render)
        img.image = render
        img.place(x=0, y=0)
        # self.dispath(path)

        # labels can be text or images
        img = Label(self, image=render)
        img.image = render
        img.place(x=0, y=0)

    def client_exit(self):
        exit()

    def clear_text(self, box1, container):
        for widget in box1.winfo_children():
            widget.destroy()
        container.delete(1.0, END)


root = Tk()

root.geometry("1920x1080")
root.state('zoomed')
root.wm_iconbitmap('icon1.ico')
app = Window(root)
root.mainloop()
