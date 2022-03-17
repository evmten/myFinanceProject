import tkinter as tk               
from tkinter import font as tkfont
from tkinter import ttk
import calendar
import sqlite3 as lite

root =tk.Tk

class SampleApp(root):

    def __init__(self, *args, **kwargs):
        root.__init__(self, *args, **kwargs)

        self.title_font = tkfont.Font(family='Arial', size=20, weight="bold")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (Main, IncomeData, ExpensesData, ShowExpensesData, ShowIncomeData):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Main")

    def show_frame(self, page_name):
        #Show a frame for the given page name
        frame = self.frames[page_name]
        frame.tkraise()


class Main(ttk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        label = ttk.Label(self, text="Main", font=controller.title_font)
        label.pack(padx = 20, pady = 20)

        btnIncome = tk.Button(self, text="Income", font = "Arial 15 bold", activeforeground='green', command=lambda: controller.show_frame("IncomeData"))
        btnIncome.pack(fill = 'both', expand = 1, padx = 30, pady = 15)
        
        btnExpenses = tk.Button(self, text="Expenses", font = "Arial 15 bold", activeforeground='green', command=lambda: controller.show_frame("ExpensesData"))
        btnExpenses.pack(fill = 'both', expand = 1, padx = 30, pady = 15)

        self.btnPrintIncomeData = tk.Button(self, text="Income Data", font = "Arial 15 bold", activeforeground='green', 
                                command=lambda: controller.show_frame("ShowIncomeData"))
        self.btnPrintIncomeData.pack(fill = 'both', expand = 1, padx = 30, pady = 15)

        self.btnPrintData = tk.Button(self, text="Expenses Data", font = "Arial 15 bold", activeforeground='green', 
                                        command=lambda: controller.show_frame("ShowExpensesData"))
        self.btnPrintData.pack(fill = 'both', expand = 1, padx = 30, pady = 15)
        

class IncomeData(tk.Frame):

    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        #Connecting DataBase, Creating table
        def query_db():
            try:
                connection = lite.connect('MyFinance.db')
                with connection:
                    cursor = connection.cursor()
                    cursor.execute('''CREATE TABLE IF NOT EXISTS incomeData(date DATE NOT NULL, salaris INT NOT NULL)''')
                    return cursor.fetchall()
            except lite.Error as er:
                print(er)
                return 0
        
        query_db()

        self.button = tk.Button(self, text="Back to Main", font = "Arial 15 bold", activeforeground='green',
                            command=lambda: controller.show_frame("Main"))
        self.button.pack()
        #UI Window fields
        self.myTextDate = tk.StringVar()
        self.myLabelDate = tk.Label(self, textvariable = self.myTextDate, font = "Arial 13 bold", )
        self.myLabelDate.pack(fill = 'both', expand = 1, padx = 25, pady = 5)
        self.myTextDate.set('Date: ' )

        self.date = tk.Entry(self, bd=2)
        self.date.pack(fill = 'both', expand = 1, padx = 25, pady = 5)
        
        self.myTextSalaris = tk.StringVar()
        self.myLabelSalaris = tk.Label(self, textvariable = self.myTextSalaris, font = "Arial 13 bold")
        self.myLabelSalaris.pack(fill = 'both', expand = 1, padx = 25, pady = 5)
        self.myTextSalaris.set('Salaris: ' )
        
        self.salaris = tk.Entry(self, bd=2)
        self.salaris.pack(fill = 'both', expand = 1, padx = 25, pady = 5)

        def btnPressed():
            
            connection = lite.connect('MyFinance.db')
            cursor = connection.cursor()

            def check_empty() :

                popup_win = tk.Toplevel()

                if ((len(self.date.get()) != 0) & (len(self.salaris.get()) != 0)):
                    incomedata = (self.date.get(), self.salaris.get())
                    try:
                        cursor.execute('INSERT INTO incomeData VALUES(?,?)', incomedata)
                    except lite.IntegrityError as e:
                        print("Couldn't insert data {}:\n {}".format(incomedata, e))
                        pass
                    connection.commit()

                    self.myTextSaved = tk.StringVar()
                    self.myLabelSaved = tk.Label(popup_win, textvariable = self.myTextSaved, font = "Arial 13 bold", fg = 'green')
                
                    self.myLabelSaved.pack(fill = 'both', expand = 1, padx = 25, pady = 5)
                    self.myTextSaved.set("Saved")
                    
                    self.date.delete(0, tk.END)
                    self.salaris.delete(0, tk.END)
                
                else:
                    self.myTextRequired = tk.StringVar()
                    self.myLabelRequired = tk.Label(popup_win, textvariable = self.myTextRequired, font = "Arial 13 bold", fg = 'red')

                    self.myLabelRequired.pack(fill = 'both', expand = 1, ipadx = 25, ipady = 5)
                    self.myTextRequired.set("Input Required")

                    self.date.delete(0, tk.END)
                    self.salaris.delete(0,tk.END)

                    
                self.button_close = tk.Button(popup_win, text="Close", command=popup_win.destroy)
                self.button_close.pack(fill='x')
                   
                 
            check_empty()
            
        self.btn = tk.Button(self, text="SAVE", font = "Arial 15 bold", activeforeground='green', command = btnPressed)
        self.btn.pack(fill = 'both', expand = 1, padx = 25, pady = 15)
        

class ShowIncomeData(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
    
        # def showData():
        connection = lite.connect('MyFinance.db')
        cursor = connection.cursor()

        try:
            cursor.execute('SELECT * FROM incomeData')
            incomeRecords = cursor.fetchall()

            self.button = tk.Button(self, text="Back to Main", font = "Arial 15 bold", activeforeground='green',
                        command=lambda: controller.show_frame("Main"))
            self.button.grid(column=3)

            j = 0

            for row in incomeRecords:
                
                j+=1
                self.myTextVar = tk.StringVar()
                self.myLabelVar = tk.Label(self, textvariable = self.myTextVar, font = "Arial 13 bold")
                self.myLabelVar.grid(row = j, column = 1,)
                self.myTextVar.set((j ,'.'))
                

                self.myTextDateData = tk.StringVar()
                self.myLabelDateData = tk.Label(self, textvariable = self.myTextDateData, font = "Arial 13 bold")
                self.myLabelDateData.grid(row = j, column = 2)
                self.myTextDateData.set(('Date:',row[0]))
                    
                self.myTextAmountData = tk.StringVar()
                self.myLabelAmountData = tk.Label(self, textvariable = self.myTextAmountData, font = "Arial 13 bold")
                self.myLabelAmountData.grid(row = j, column = 3)
                self.myTextAmountData.set(('Salaris:',row[1]))

        except lite.IntegrityError as e:
            print('Couldn\'t load the data')
            pass

        connection.commit()  

class ExpensesData(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        #Connecting DataBase, Creating table
        def query_db():
            try:
                connection = lite.connect('MyFinance.db')
                with connection:
                    cursor = connection.cursor()
                    cursor.execute('''CREATE TABLE IF NOT EXISTS expensesData(date DATE NOT NULL, amount INT NOT NULL)''')
                    return cursor.fetchall()
            except lite.Error as er:
                print(er)
                return 0
        
        query_db()

        #UI Window fields
        self.myTextDate2 = tk.StringVar()
        self.myLabelDate2 = tk.Label(self, textvariable = self.myTextDate2, font = "Arial 13 bold", )
        self.myLabelDate2.pack(fill = 'both', expand = 1, padx = 25, ipady = 5)
        self.myTextDate2.set('Date: ' )

        self.date = tk.Entry(self, bd=2)
        self.date.pack(fill = 'both', expand = 1, padx = 25, ipady = 5)
        
        self.myTextAmount = tk.StringVar()
        self.myLabelAmount = tk.Label(self, textvariable = self.myTextAmount, font = "Arial 13 bold")
        self.myLabelAmount.pack(fill = 'both', expand = 1, padx = 25, ipady = 5)
        self.myTextAmount.set('Amount: ' )
        
        self.salaris = tk.Entry(self, bd=2)
        self.salaris.pack(fill = 'both', expand = 1, padx = 25, ipady = 5)

        def btnPressed():
            
            connection = lite.connect('MyFinance.db')
            cursor = connection.cursor()

            def check_empty() :

                popup_win = tk.Toplevel()

                if ((len(self.date.get()) != 0) & (len(self.salaris.get()) != 0)):
                    incomedata = (self.date.get(), self.salaris.get())
                    try:
                        cursor.execute('INSERT INTO expensesData VALUES(?,?)', incomedata)
                    except lite.IntegrityError as e:
                        print("Couldn't insert data {}:\n {}".format(incomedata, e))
                        pass
                    connection.commit()
                    
                    self.myTextSaved2 = tk.StringVar()
                    self.myLabelSaved2 = tk.Label(popup_win, textvariable = self.myTextSaved2, font = "Arial 13 bold", fg = 'green')
                
                    self.myLabelSaved2.pack(fill = 'both', expand = 1, ipadx = 25, ipady = 5)
                    self.myTextSaved2.set("Saved")
                    
                    self.date.delete(0, tk.END)
                    self.salaris.delete(0, tk.END)
                
                else:
                    self.myTextRequired2 = tk.StringVar()
                    self.myLabelRequired2 = tk.Label(popup_win, textvariable = self.myTextRequired2, font = "Arial 13 bold", fg = 'red')

                    self.myLabelRequired2.pack(fill = 'both', expand = 1, ipadx = 25, ipady = 5)
                    self.myTextRequired2.set("Input Required")

                    self.date.delete(0, tk.END)
                    self.salaris.delete(0,tk.END)

                    
                self.button_close = tk.Button(popup_win, text="Close", command=popup_win.destroy)
                self.button_close.pack(fill='x')       
            
            check_empty()
        
        self.btn = tk.Button(self, text="SAVE", font = "Arial 15 bold", activeforeground='green', command = btnPressed)
        self.btn.pack(fill = 'both', expand = 1, padx = 25, pady = 15)
        

       
        button = tk.Button(self, text="Back to Main", font = "Arial 15 bold", activeforeground='green',
                            command=lambda: controller.show_frame("Main"))
        button.pack()


class ShowExpensesData(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
    
        # def showData():
        connection = lite.connect('MyFinance.db')
        cursor = connection.cursor()


        try:
            cursor.execute('SELECT * FROM expensesData')
            records = cursor.fetchall()

            self.button = tk.Button(self, text="Back to Main", font = "Arial 15 bold", activeforeground='green',
                        command=lambda: controller.show_frame("Main"))
            self.button.pack()

            i = 0

            for row in records:
                
                i+=1
                self.myTextVar = tk.StringVar()
                self.myLabelVar = tk.Label(self, textvariable = self.myTextVar, font = "Arial 13 bold")
                self.myLabelVar.grid(row = i, column = 1,)
                self.myTextVar.set((i ,'.'))
                

                self.myTextDateData = tk.StringVar()
                self.myLabelDateData = tk.Label(self, textvariable = self.myTextDateData, font = "Arial 13 bold")
                self.myLabelDateData.grid(row = i, column = 2)
                self.myTextDateData.set(('Date:',row[0]))
                    
                
                self.myTextAmountData = tk.StringVar()
                self.myLabelAmountData = tk.Label(self, textvariable = self.myTextAmountData, font = "Arial 13 bold")
                self.myLabelAmountData.grid(row = i, column = 3)
                self.myTextAmountData.set(('Amount:',row[1]))


        except lite.IntegrityError as e:
            print('Couldn\'t load the data')
            pass

        connection.commit()  


if __name__ == "__main__":
    app = SampleApp()
    app.title("My Finances")
    app.geometry("500x500")
    app.mainloop()