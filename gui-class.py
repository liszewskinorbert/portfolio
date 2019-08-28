from tkinter import *

class Application(Frame):

    def __init__(self,master):
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()


    def create_widgets(self):
        #Pierwszy przycisk
        self.bttn1 = Button(self, text = "Nic nie robie")
        self.bttn1.grid()

        #Drugi przycisk
        self.bttn2 = Button(self)
        self.bttn2.grid()
        self.bttn2.configure(text= "Ja rowniez")

        #Trzeci przycisk
        self.bttn3 = Button(self)
        self.bttn3.grid()
        self.bttn3["text"] = "To samo mnie dotyczy!"

# root
root = Tk()
root.title("Leniwe class")
root.geometry("300x200")
app = Application(root)

root.mainloop()




