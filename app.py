from tkinter import ttk
from tkinter import *
import sqlite3


class Product:
    def __init__(self, root):
        self.window = root
        self.window.title("Product Manager App")
        self.window.resizable(1,1)
        self.window.wm_iconbitmap("resources\\icon.ico")
        
        frame = LabelFrame(self.window, text = "Register a new product", font=('Calibri', 16, 'bold'))
        frame.grid(row=0, column=0, columnspan=3, pady=20)
        
        self.name_tag = Label(frame, text="Name: ", font=('Calibri', 13))
        self.name_tag.grid(row=1, column=0)
        
        self.name = Entry(frame, font=('Calibri', 13))
        self.name.focus()
        self.name.grid(row=1, column=1)
        
        self.name_tag = Label(frame, text="Price: ", font=('Calibri', 13))
        self.name_tag.grid(row=2, column=0)
        
        self.price = Entry(frame, font=('Calibri', 13))
        self.price.grid(row=2, column=1)
        
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.add_button = ttk.Button(frame, text="Save Product", command=self.add_product, style='my.TButton')
        self.add_button.grid(row=3, columnspan=2, sticky=W+E)
        
        self.message = Label(text="", fg="red")
        self.message.grid(row=3, column=0, columnspan=2, sticky=W+E)
        
        style = ttk.Style()
        style.configure("mystyle.Treeview", highlightthickness=0, bd=0, font=("Calibri", 11))
        style.configure("mystyle.Treeview.Heading", font=("Calibri", 13, "bold"))
        style.layout("mystyle.Treeview", [("mystyle.Treeview.treearea", {"sticky":"nswe"})])
        
        self.table = ttk.Treeview(height=20, columns=2, style="mystyle.Treeview")
        self.table.grid(row=4, column=0, columnspan=2)
        self.table.heading("#0", text="Name", anchor=CENTER)
        self.table.heading("#1", text="Price", anchor=CENTER)
        
        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        delete_button = ttk.Button(text="DELETE", command=self.del_product, style='my.TButton')
        delete_button.grid(row=5, column=0, sticky=W+E)
        
        edit_button = ttk.Button(text="EDIT", command=self.edit_product, style='my.TButton')
        edit_button.grid(row=5, column=1, sticky=W+E)
        
        self.get_products()

    db = "database\\products.db"
    
    def db_consult(self, consult, parameters = ()):
        
        with sqlite3.connect(self.db) as con:
            cursor = con.cursor()
            result = cursor.execute(consult, parameters)
            con.commit()
        
        return result
    
    def get_products(self):
        
        table_items = self.table.get_children()
        for row in table_items:
            self.table.delete(row)
            
        query = "SELECT * FROM products ORDER BY name DESC"
        items_db = self.db_consult(query)
        
        for row in items_db:
            self.table.insert("", 0, text= row[1], values=row[2])
    
    def name_validation(self):
        
        name_inserted = self.name.get()
        return len(name_inserted) != 0
    
    def price_validation(self):
        
        price_inserted = self.price.get()
        return len(price_inserted) != 0

    def add_product(self):
        
        if self.name_validation() and self.price_validation():
            query = "INSERT INTO products VALUES(NULL, ?, ?)"
            parameters = (self.name.get(), self.price.get())
            
            self.db_consult(query, parameters)
            
            self.message["text"] = f"Product {self.name.get()} added successfully."
            self.name.delete(0, END)
            self.price.delete(0, END)
        
        elif self.name_validation and self.price_validation == False:
            self.message["text"] = "The price is mandatory."
        
        elif self.name_validation == False and self.price_validation:
            self.message["text"] = "The Product's name is mandatory."
            
        else:
            self.message["text"] = "The Product's name and it's price are mandatory."
        
        self.get_products()
    
    def del_product(self):
        self.message["text"] = ""
        
        try:
            self.table.item(self.table.selection())["text"][0]
        except IndexError as e:
            self.message["text"] = "Please, choose a product."
            return
        
        self.message["text"] = ""
        name = self.table.item(self.table.selection())["text"]
        query = "DELETE FROM products WHERE name = ?"
        self.db_consult(query, (name,))
        self.message["text"] = f"Product {name} deleted."
        
        self.get_products()
            
    def edit_product(self):
        self.message["text"] = ""
        
        try:
            self.table.item(self.table.selection())["text"][0]
        except IndexError as e:
            self.message["text"] = "Please, choose a product."
            return        
    
        name = self.table.item(self.table.selection())["text"]
        old_price = self.table.item(self.table.selection())["values"][0]
        
        self.edit_window = Toplevel()
        self.edit_window.title = "Edit product"
        self.edit_window.resizable(1,1)
        self.edit_window.wm_iconbitmap("resources\\icon.ico")
        
        title = Label(self.edit_window, text="Edit product", font = ("Calibri", 16, "bold"))
        title.grid(row=0, column=0)
        
        frame_ep = LabelFrame(self.edit_window, text="Edit the following product:", font=('Calibri', 16, 'bold'))
        frame_ep.grid(row=1, column=0, columnspan=20, pady=20)
        
        self.old_name_tag = Label(frame_ep, text="Former name: ", font=('Calibri', 13))
        self.old_name_tag.grid(row=2, column=0) 
        self.input_old_name = Entry(frame_ep, textvariable=StringVar(self.edit_window, value=name), state='readonly', font=('Calibri', 13))
        self.input_old_name.grid(row=2, column=1)
        
        self.new_name_tag = Label(frame_ep, text="New name: ", font=('Calibri', 13))
        self.new_name_tag.grid(row=3, column=0)
        self.input_new_name = Entry(frame_ep, font=('Calibri', 13))
        self.input_new_name.grid(row=3, column=1)
        self.input_new_name.focus()
        
        self.old_price_tag = Label(frame_ep, text="Former price: ", font=('Calibri', 13))
        self.old_price_tag.grid(row=4, column=0)
        self.input_old_price = Entry(frame_ep, textvariable=StringVar(self.edit_window, value=old_price), state='readonly', font=('Calibri', 13))
        self.input_old_price.grid(row=4, column=1)

        self.new_price_tag = Label(frame_ep, text="New price: ", font=('Calibri', 13))
        self.new_price_tag.grid(row=5, column=0)
        self.input_new_price = Entry(frame_ep, font=('Calibri', 13))
        self.input_new_price.grid(row=5, column=1)

        s = ttk.Style()
        s.configure('my.TButton', font=('Calibri', 14, 'bold'))
        self.refresh_button = ttk.Button(frame_ep, text="Update product", style='my.TButton', command=lambda: self.update_product(self.input_new_name.get(), self.input_old_name.get(), self.input_new_price.get(), self.input_old_price.get()))
        self.refresh_button.grid(row=6, columnspan=2, sticky=W + E)
        
    def update_product(self, new_name, old_name, new_price, old_price):
        
        updated_product = False
        query = 'UPDATE products SET name = ?, price = ? WHERE name = ? AND price = ?'
        
        if new_name != '' and new_price != '':
            parameters = (new_name, new_price, old_name, old_price)
            updated_product = True
        
        elif new_name != '' and new_price == '':
            parameters = (new_name, old_price, old_name, old_price)
            updated_product = True
            
        elif new_name == '' and new_price != '':
            parametros = (old_name, new_price, old_name, old_price)
            updated_product = True 
        
        if (updated_product):
            self.db_consult(query, parameters)
            self.edit_window.destroy()
            self.message['text'] = f'The item {old_name} was updated'
            self.get_products()
        
        else:
            self.edit_window.destroy()
            self.message['text'] = f'The item {old_name} wasn\'t updated'
        
if __name__ == "__main__":
    root = Tk()
    app = Product(root)
    root.mainloop()
    
