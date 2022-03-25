import tkinter as tk               
from tkinter import CENTER, W, Label, font as tkfont
from tkinter import ttk
import sqlite3 as lite
from tkinter import messagebox

from numpy import record

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
        for F in (Main, IncomeData, ExpensesData):
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

        # Main menu buttons (options)
        label = tk.Label(self, text="Main", font=controller.title_font)
        label.pack(fill="both", padx=15, pady=15)

        btnIncome = tk.Button(self, text="Income", font = "Arial 15 bold", activeforeground='green', command=lambda: controller.show_frame("IncomeData"))
        btnIncome.pack(fill="both", padx=15, pady=15)
        
        btnExpenses = tk.Button(self, text="Expenses", font = "Arial 15 bold", activeforeground='green', command=lambda: controller.show_frame("ExpensesData"))
        btnExpenses.pack(fill="both", padx=15, pady=15)
        

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
                    cursor.execute('''CREATE TABLE IF NOT EXISTS incomeData(id INT NOT NULL, date DATE NOT NULL, salaris INT NOT NULL)''')
                    return cursor.fetchall()
            except lite.Error as er:
                print(er)
                return 0
        
        query_db()

        #Main menu button
        btn_main = tk.Button(self, text="<< Main", font = "Arial 10 bold", activeforeground='green',
                            command=lambda: controller.show_frame("Main"))
        btn_main.pack(pady=10)

        #Define Our Columns
        income_tree = ttk.Treeview(self)
        income_tree['columns'] = ("ID", "Date", "Salaris")
        
        #Formate Our Columns
        income_tree.column("#0", width=0, stretch='NO')
        income_tree.column("ID", anchor=W, width=30)
        income_tree.column("Date", anchor=CENTER, width=120)
        income_tree.column("Salaris", anchor=W, width=120)

        # Create Headings
        income_tree.heading("#0", text="Label", anchor=W)
        income_tree.heading("ID", text="ID", anchor=W)
        income_tree.heading("Date", text="Date", anchor=CENTER)
        income_tree.heading("Salaris", text="Salaris", anchor=W)

        income_tree.pack(pady=20)

        add_frame = ttk.Frame(self)
        add_frame.pack(pady=20)

        #Labels
        id_lbl = Label(add_frame, text="ID")
        id_lbl.grid(row=0, column=0)

        date_lbl = Label(add_frame, text="Date")
        date_lbl.grid(row=0, column=1)

        salaris_lbl = Label(add_frame, text= "Salaris")
        salaris_lbl.grid(row=0, column=2)

        #Entry boxes
        id_box = ttk.Entry(add_frame)
        id_box.grid(row=1, column=0)

        date_box = ttk.Entry(add_frame)
        date_box.grid(row=1, column=1)

        salaris_box = ttk.Entry(add_frame)
        salaris_box.grid(row=1, column=2)
        
        def view_incomeData():

            try:
                connection = lite.connect('MyFinance.db')
                with connection:
                    cursor = connection.cursor()
                    cursor.execute('''SELECT * FROM  incomeData''')
                    records =  cursor.fetchall()
                    for record in records:
                        income_tree.insert("", tk.END, values=record)
            except lite.Error as er:
                print(er)
                return 0

        view_incomeData()
        global count
        count = 0

        #Clear the entry boxes
        def clear_boxes():
            id_box.delete(0, tk.END)
            date_box.delete(0, tk.END)
            salaris_box.delete(0,tk.END)

        #Add_Record Function
        def add_record():
            
            global count   
            if ((len(id_box.get()) != 0) & (len(date_box.get()) != 0) & (len(salaris_box.get()) !=0)):
              
                income_tree.insert(parent='', index='end', iid=count, text="", values=(id_box.get(), date_box.get(), salaris_box.get()))
                count += 1
                        
            connection = lite.connect('MyFinance.db')
            cursor = connection.cursor()

            #Checking if all fields are not empty    
            def check_empty():

                popup_win = tk.Toplevel()

                if ((len(id_box.get()) != 0) & (len(date_box.get()) != 0) & (len(salaris_box.get()) !=0)):
                    incomedata = (id_box.get(), date_box.get(), salaris_box.get())
                    query_db()
                    try:
                        cursor.execute('INSERT INTO incomeData VALUES(?,?,?)', incomedata)
                    except lite.IntegrityError as e:
                        print("Couldn't insert data {}:\n {}".format(incomedata, e))
                        pass
                    connection.commit()
                    self.myLabelSaved2 = tk.Label(popup_win, text = "Saved", font = "Arial 13 bold", fg = 'green')
                    self.myLabelSaved2.pack(fill = 'both', expand = 1, ipadx = 25, ipady = 5)
                    
                    clear_boxes()
                    
                else:

                    self.myLabelRequired = tk.Label(popup_win, text = "Input Required", font = "Arial 13 bold", fg = 'red')
                    self.myLabelRequired.pack(fill = 'both', expand = 1, ipadx = 25, ipady = 5)
                    clear_boxes()

                self.button_close = tk.Button(popup_win, text="Close", command=popup_win.destroy)
                self.button_close.pack(fill='x')
                
            check_empty()
        
        #Select a record
        def select_record():
            
            # Clear entry boxes
            id_box.delete(0, tk.END)
            date_box.delete(0, tk.END)
            salaris_box.delete(0, tk.END)

            # Grab record Number
            selected = income_tree.focus()
            # Grab record values
            values = income_tree.item(selected, 'values')

            # output to entry boxes
            id_box.insert(0, values[0])
            date_box.insert(0, values[1])
            salaris_box.insert(0, values[2])
            
        #Update a record
        def update_record():
            selected_item = income_tree.focus()
            response = messagebox.askyesnocancel("Update Record","Do you want to update this record?")
            
            if response == 1:
                try:
                    connection = lite.connect('MyFinance.db')
                    with connection:
                        cursor = connection.cursor()
                        for selected_item in income_tree.selection():
                            cursor.execute("UPDATE incomeData SET id = ?, date = ?, salaris = ? WHERE id=?", (id_box.get(),date_box.get(),salaris_box.get(),income_tree.set(selected_item, '#1'),))
                            connection.commit()
                            income_tree.item(selected_item, text = "", values = (id_box.get(), date_box.get(), salaris_box.get()))
                    connection.close()
                    # Clear entry boxes
                    id_box.delete(0, tk.END)
                    date_box.delete(0, tk.END)
                    salaris_box.delete(0, tk.END)

                except lite.Error as er:
                    print(er)
                    return 0
        
        #Remove one selected
        def remove_one():
            
            response = messagebox.askyesnocancel("Delete Record","Do you want to delete this record?")
            
            if response == 1:
                try:
                    connection = lite.connect('MyFinance.db')
                    with connection:
                        cursor = connection.cursor()
                        for selected_item in income_tree.selection():
                            cursor.execute("DELETE FROM incomeData WHERE id=?", (income_tree.set(selected_item, '#1'),))
                            connection.commit()
                            income_tree.delete(selected_item)
                    connection.close()

                except lite.Error as er:
                    print(er)
                    return 0

        #Remove all records
        def remove_all():
            response = messagebox.askyesnocancel("Delete Records","Do you want to delete all the records?")
            if response == 1:
            
                for record in income_tree.get_children():
                    income_tree.delete(record)
                
                try:
                    connection = lite.connect('MyFinance.db')
                    with connection:
                        cursor = connection.cursor()
                        cursor.execute('''DROP TABLE incomeData''')
                        connection.commit()
                        connection.close()

                except lite.Error as er:
                    print(er)
                    return 0

        #Buttons
        #Add Record
        add_record = ttk.Button(self, text = "Add Record", command = add_record)
        add_record.pack(pady = 5)

        #Select Record
        select_record = ttk.Button(self, text = "Select Record", command = select_record)
        select_record.pack(pady = 5)

        #Update Record
        update_record = ttk.Button(self, text = "Update Record", command = update_record)
        update_record.pack(pady = 5)

        #Remove One
        remove_one = ttk.Button(self, text="Remove One Selected", command = remove_one)
        remove_one.pack(pady = 5)

        #Remove all
        remove_all = ttk.Button(self, text = "Remove All Records", command = remove_all)
        remove_all.pack(pady = 5)

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
                    cursor.execute('''CREATE TABLE IF NOT EXISTS expensesData(id INT NOT NULL, date DATE NOT NULL, amount INT NOT NULL)''')
                    return cursor.fetchall()
            except lite.Error as er:
                print(er)
                return 0
        
        query_db()

        #Main menu button
        btn_main = tk.Button(self, text="<< Main", font = "Arial 10 bold", activeforeground='green',
                            command=lambda: controller.show_frame("Main"))
        btn_main.pack(pady=10)

        #Define Our Columns
        expenses_tree = ttk.Treeview(self)
        expenses_tree['columns'] = ("ID", "Date", "Amount")
        
        #Formate Our Columns
        expenses_tree.column("#0", width=0, stretch='NO')
        expenses_tree.column("ID", anchor=W, width=30)
        expenses_tree.column("Date", anchor=CENTER, width=120)
        expenses_tree.column("Amount", anchor=W, width=120)

        # Create Headings
        expenses_tree.heading("#0", text="Label", anchor=W)
        expenses_tree.heading("ID", text="ID", anchor=W)
        expenses_tree.heading("Date", text="Date", anchor=CENTER)
        expenses_tree.heading("Amount", text="Amount", anchor=W)

        expenses_tree.pack(pady=20)

        add_frame = ttk.Frame(self)
        add_frame.pack(pady=20)

        #Labels
        id_lbl = Label(add_frame, text="ID")
        id_lbl.grid(row=0, column=0)

        date_lbl = Label(add_frame, text="Date")
        date_lbl.grid(row=0, column=1)

        amount_lbl = Label(add_frame, text= "Amount")
        amount_lbl.grid(row=0, column=2)

        #Entry boxes
        id_box = ttk.Entry(add_frame)
        id_box.grid(row=1, column=0)

        date_box = ttk.Entry(add_frame)
        date_box.grid(row=1, column=1)

        amount_box = ttk.Entry(add_frame)
        amount_box.grid(row=1, column=2)
        
        def view_expensesData():

            try:
                connection = lite.connect('MyFinance.db')
                with connection:
                    cursor = connection.cursor()
                    cursor.execute('''SELECT * FROM  expensesData''')
                    records =  cursor.fetchall()
                    for record in records:
                        expenses_tree.insert("", tk.END, values=record)
            except lite.Error as er:
                print(er)
                return 0

        view_expensesData()

        global count
        count = 0

        #Clear the entry boxes
        def clear_boxes():
            id_box.delete(0, tk.END)
            date_box.delete(0, tk.END)
            amount_box.delete(0,tk.END)

        #Add_Record Function
        def add_record():
            
            global count   
            if ((len(id_box.get()) != 0) & (len(date_box.get()) != 0) & (len(amount_box.get()) !=0)):
              
                expenses_tree.insert(parent='', index='end', iid=count, text="", values=(id_box.get(), date_box.get(), amount_box.get()))
                count += 1
                        
            connection = lite.connect('MyFinance.db')
            cursor = connection.cursor()

            def check_empty() :

                popup_win = tk.Toplevel()

                if ((len(id_box.get()) != 0) & (len(date_box.get()) != 0) & (len(amount_box.get()) !=0)):
                    expensesdata = (id_box.get(), date_box.get(), amount_box.get())
                    query_db()
                    try:
                        cursor.execute('INSERT INTO expensesData VALUES(?,?,?)', expensesdata)
                    except lite.IntegrityError as e:
                        print("Couldn't insert data {}:\n {}".format(expensesdata, e))
                        pass
                    connection.commit()
                    self.myLabelSaved2 = tk.Label(popup_win, text = "Saved", font = "Arial 13 bold", fg = 'green')
                    self.myLabelSaved2.pack(fill = 'both', expand = 1, ipadx = 25, ipady = 5)
                    
                    clear_boxes()
                    
                else:

                    self.myLabelRequired = tk.Label(popup_win, text = "Input Required", font = "Arial 13 bold", fg = 'red')
                    self.myLabelRequired.pack(fill = 'both', expand = 1, ipadx = 25, ipady = 5)
                    clear_boxes()

                self.button_close = tk.Button(popup_win, text="Close", command=popup_win.destroy)
                self.button_close.pack(fill='x')
                
            check_empty()
        
        #Select a record
        def select_record():
            
            # Clear entry boxes
            id_box.delete(0, tk.END)
            date_box.delete(0, tk.END)
            amount_box.delete(0, tk.END)

            # Grab record Number
            selected = expenses_tree.focus()
            # Grab record values
            values = expenses_tree.item(selected, 'values')

            # output to entry boxes
            id_box.insert(0, values[0])
            date_box.insert(0, values[1])
            amount_box.insert(0, values[2])       

        #Update a record
        def update_record():
            selected_item = expenses_tree.focus()
            response = messagebox.askyesnocancel("Update Record","Do you want to update this record?")
            
            if response == 1:
                try:
                    connection = lite.connect('MyFinance.db')
                    with connection:
                        cursor = connection.cursor()
                        for selected_item in expenses_tree.selection():
                            cursor.execute("UPDATE expensesData SET id = ?, date = ?, amount = ? WHERE id=?", (id_box.get(),date_box.get(),amount_box.get(), expenses_tree.set(selected_item, '#1'),))
                            connection.commit()
                            expenses_tree.item(selected_item, text = "", values = (id_box.get(), date_box.get(), amount_box.get()))
                    connection.close()
                    # Clear entry boxes
                    id_box.delete(0, tk.END)
                    date_box.delete(0, tk.END)
                    amount_box.delete(0, tk.END)

                except lite.Error as er:
                    print(er)
                    return 0

        #Remove one selected
        def remove_one():

            response = messagebox.askyesnocancel("Delete Record","Do you want to delete this record?")
            
            if response == 1:
                try:
                    connection = lite.connect('MyFinance.db')
                    with connection:
                        cursor = connection.cursor()
                        for selected_item in expenses_tree.selection():
                            cursor.execute("DELETE FROM expensesData WHERE id=?", (expenses_tree.set(selected_item, '#1'),))
                            connection.commit()
                            expenses_tree.delete(selected_item)
                    connection.close()

                except lite.Error as er:
                    print(er)
                    return 0

        #Remove all records
        def remove_all():
            response = messagebox.askyesnocancel("Delete Records","Do you want to delete all the records?")
            if response == 1:
            
                for record in expenses_tree.get_children():
                    expenses_tree.delete(record)
                
                try:
                    connection = lite.connect('MyFinance.db')
                    with connection:
                        cursor = connection.cursor()
                        cursor.execute('''DROP TABLE expensesData''')
                        connection.commit()
                        connection.close()

                except lite.Error as er:
                    print(er)
                    return 0

        #Buttons
        add_record = ttk.Button(self, text= "Add Record", command = add_record)
        add_record.pack(pady = 10)

        #Select Record
        select_record = ttk.Button(self, text = "Select Record", command = select_record)
        select_record.pack(pady = 5)

        #Update Record
        update_record = ttk.Button(self, text = "Update Record", command = update_record)
        update_record.pack(pady = 5)

        #Remove One
        remove_one = ttk.Button(self, text="Remove One Selected", command=remove_one)
        remove_one.pack(pady=5)

        #Remove all
        remove_all = ttk.Button(self, text = "Remove All Records", command = remove_all)
        remove_all.pack(pady = 5)

if __name__ == "__main__":
    app = SampleApp()
    app.title("My Finances")
    app.geometry("500x600")
    app.mainloop()