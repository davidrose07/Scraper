from tkinter import *
from tkinter import messagebox
from Scraper.scrape import Scrape
from Scraper.app import App
import csv,pymsgbox

def main():
    def insert_data(rows):
        app.btn3['state']='normal'
        app.tree.delete(*app.tree.get_children())
        for row in rows:
            try:
                app.tree.insert('',END, values=row)
            except:
                messagebox.showerror("Show Data Error", "Could not show data in treeview")
        app.tree.grid(column=0,row=0)
            
    def showData(event):    
        app.progress.grid(column=0,row=1)
        Scrape.find_items(app.search.get(),app.num.get())
        rows=Scrape.display()
        insert_data(rows)
        
    def filter_data(event):    
        mystring=app.filter_search.get()
        rows=Scrape.filter(mystring)  
        insert_data(rows)
        
    def clear_results():
        app.tree.delete(*app.tree.get_children())
        app.search.set("")
    
    def create_csv():
        # Convert string price to int
        total=0
        for row in selected_item:
            try:
                part = [int(x) for x in row[3].split(",")]
                num = int(str(part[0]) + str(part[1]))
            except:
                num=int(row[3])
            total+=int(num)
        # Append total to the end of the list
        total_list=['Total', total]
        selected_item.append(total_list)
        # Create fields and CSV file to email
        filename='/products.csv'
        fields=['Brand','Name', 'Ratings', 'Price','URL']
        with open(filename, 'w+',newline="") as csvfile:
            csvwriter=csv.writer(csvfile)
            csvwriter.writerow(fields)
            for row in selected_item:
                csvwriter.writerow(row)
            pymsgbox.alert("CSV Created")
    def delete():
        global new_app
        items = new_app.tree.selection()
        for i in range(len(selected_item)):
               if selected_item[i] == new_app.tree.item(items)['values'][0]:
                   selected_item.pop(i) # Remove the corresponding item
                   # Make sure the list is updated:
                   print('length: {}'.format(len(selected_item)))
                   break          
        new_app.tree.delete(items)        
           
    def addData(event):
        global new_app
        app.btn2['state']='normal'
        new_app=App()
        new_app.tab2.destroy()
        new_app.btn1.config(text="Create CSV", command=create_csv)
        new_app.btn2['state'] = 'normal'
        new_app.btn2.config(text="Delete", command=delete)
        new_app.withdraw()
        item=app.tree.item(app.tree.focus())
        selected_item.append(item['values'])
        
    def show_list():
        try:
            for row in selected_item:
                new_app.tree.insert('',END, values=row)
        except:
            messagebox.showerror("Open Text Error", "Could not show data in treeview")
        new_app.tree.grid(column=0,row=0)
        new_app.deiconify()
    
    app = App()
    selected_item=[]
    app.entry2.bind('<Key>', filter_data)
    app.entry1.bind('<Return>',showData )
    app.btn2.config(command=show_list)
    app.btn3.config(command=clear_results)
    app.tree.bind('<Double 1>', addData)
    app.mainloop()    
if __name__ == "__main__":
    main()
    
    