import tkinter as tk
from tkinter import ttk
from tkinter import *
from Scraper.scrape import Scrape

class App(tk.Tk):
    # Constructor
    def __init__(self):
        super().__init__()
        self.geometry("1000x600+0+0")
        self.title('Amazon Scraper')
        self.resizable(True,True)

        # Configure the grid
        self.columnconfigure(0, weight=5)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=3)
        
        # Create Varibales
        self.search=tk.StringVar()
        self.filter_search= tk.StringVar()
        
        # Configure the top frame
        self.topFrame=tk.Frame(self)
        self.topFrame.columnconfigure(0,weight=3)
        self.topFrame.columnconfigure(1,weight=1)
        self.topFrame.grid(column=0,row=0,sticky='nesw')
        
        # create a tab for search and filter
        self.tabControl = ttk.Notebook(self.topFrame)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text ='Search')
        self.tabControl.add(self.tab2, text ='Filter')
        self.tabControl.grid(column=0,row=0, rowspan=8, sticky='nesw')
        
        #Progress Bar
        self.progress = Button(self.tab1, text='Searching')
        self.progress =ttk. Progressbar(self, orient=HORIZONTAL, length=100, mode='indeterminate')
        
        # Combo Box for the number of search results
        self.num = tk.StringVar()
        self.search_num = ttk.Combobox(self.tab1, width = 10,textvariable = self.num)        
        
        # Adding combobox drop down list
        self.search_num['values'] = ('5','10')
        self.search_num.grid(column = 2, row = 0)
        
        # Shows 5 as a default value
        self.search_num.current(0)  
        
        # Labels
        self.label1=tk.Label(self.tab1, text="Search", font=('arial','14')).grid(column=0,row=0, sticky='nesw', padx=2,pady=2)
        self.label2=tk.Label(self.tab2, text="Filter",font=('arial','14')).grid(column=0, row=0,sticky='nesw',padx=2,pady=2)
        
        # Entry fields
        self.entry1=tk.Entry(self.tab1, width=30, font=('arial','16'),textvariable=self.search)
        self.entry1.grid(column=1,row=0,sticky='nesw',padx=2,pady=2)
        self.entry1.focus()
        self.entry2=tk.Entry(self.tab2, width=30, font=('arial','16'),textvariable=self.filter_search)
        self.entry2.grid(column=1,row=0,sticky='nesw',padx=2,pady=2)
        
        # Buttons
        self.btn1=tk.Button(self.topFrame, text='Search',width=10, bg='light blue', command=lambda:Scrape.find_items(self.search.get(),self.num.get()))
        self.btn1.grid(column=1,row=0,sticky='ne',padx=2,pady=5)
        self.btn2=tk.Button(self.topFrame, text='Show List',width=10, bg='light blue', state='disabled')
        self.btn2.grid(column=1,row=1,sticky='ne',padx=2,pady=5)
        self.btn3=tk.Button(self.topFrame, text='Clear',width=10, bg='light blue', state='disabled')
        self.btn3.grid(column=1,row=2,sticky='ne',padx=2,pady=5)
        self.btn4=tk.Button(self.topFrame, text='Exit',width=10, bg='light blue', command=exit)
        self.btn4.grid(column=1,row=3,sticky='ne',padx=2,pady=5)
        
        # Configure the bottom frame
        self.bottomeFrame=tk.Frame(self)
        self.bottomeFrame.columnconfigure(0,weight=3)
        self.bottomeFrame.rowconfigure(0,weight=5)
        self.bottomeFrame.grid(column=0,row=1,rowspan=50,stick='nesw')
        
        # Style the treeview
        self.s=ttk.Style()
        self.s.theme_use('clam')
        self.s.configure('Treeview', background="white", foreground='black', fieldbackground="white")
        self.s.map('Treeview.Heading', background=[('selected', 'green')])
        
        # Define Treeview
        self.tree=ttk.Treeview(self.bottomeFrame, show='headings')
        self.scroll_y=Scrollbar(self.bottomeFrame, orient=VERTICAL, command=self.tree.yview)
        self.scroll_y.grid(column=0,row=0,rowspan=50,sticky='nes')
        self.tree.config(yscrollcommand=self.scroll_y.set)
        
        # Define Columns
        self.tree['columns']=('Brand','Name_of_the_product', 'number_of_ratings', 'price_of_the_item','url_of_the_page')
        
        # Format Columns
        self.tree.column('#0',width=0)
        self.tree.column('Brand',width=120, anchor=W)
        self.tree.column('Name_of_the_product',width=120, anchor=W)
        self.tree.column('number_of_ratings',width=120, anchor=W)
        self.tree.column('price_of_the_item',width=120, anchor=W)
        self.tree.column('url_of_the_page',width=120, anchor=W)
        
        # Create Headings
        self.tree.heading("#0", text="",anchor=W)
        self.tree.heading("Brand", text="Brand",anchor=W)
        self.tree.heading("Name_of_the_product", text="Product Name",anchor=W)
        self.tree.heading("number_of_ratings", text="Ratings",anchor=W)
        self.tree.heading("price_of_the_item", text="Price",anchor=W)
        self.tree.heading("url_of_the_page", text="Url",anchor=W)
        self.tree.grid(column=0,row=0, columnspan=2,rowspan=50, sticky='nesw')
        
    def exit(self):
        self.destroy()
        