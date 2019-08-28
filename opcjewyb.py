from tkinter import *

class Application(Frame):

    def __init__(self, master):
        """Inicjalizacja"""
        super(Application, self).__init__(master)
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        """Etykiety z opisem"""
        Label(self,
              text = "Wybierz swoj ulubiony gatunek"
              ).grid(row = 0, column = 0, sticky = W)
        Label(self,
              text = "Wybierz jeden gatunek:"
              ).grid(row = 1, column = 0, sticky = W)
        self.favorite = StringVar()
        self.favorite.set(None)

        # utworz przycisk opcji wyboru komedii
        Radiobutton(self,
                    text = "komedia",
                    variable = self.favorite,
                    value = "komedia.",
                    command = self.update_text
                    ).grid(row = 2, column = 0, sticky = W)
        Radiobutton(self,
                    text = "dramat",
                    variable = self.favorite,
                    value = "dramat.",
                    command = self.update_text
                    ).grid(row = 3, column = 0, sticky = W)
        Radiobutton(self,
                    text = "romans",
                    variable = self.favorite,
                    value = "romans.",
                    command = self.update_text
                    ).grid(row = 4, column = 0, sticky = W)
        # utworz pole tekstowe
        self.results_txt = Text(self, width = 40, height = 5, wrap = WORD)
        self.results_txt.grid(row = 5, column = 0 , columnspan = 3)

    def update_text(self):
        """Zaktualizuj"""
        message = "twoim ulubionym gatunkiem filmu jest "
        message += self.favorite.get()
        self.results_txt.delete(0.0, END)
        self.results_txt.insert(0.0, message)


#main
root = Tk()
root.title("Wybor filmow 2")
app = Application(root)
root.mainloop()





