import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox

def read_txt_file():
    def on_right_click(event):
        item = treeview.selection()
        if item:
            category_name, class_name, buy_price, sell_price = treeview.item(item)["values"][:4]
            edit_dialog(category_name, class_name, buy_price, sell_price)
    
    def edit_dialog(category_name, class_name, buy_price, sell_price):
        dialog = tk.Toplevel()
        dialog.title("Edit Item")
        
        entries = []
        labels = ["Category", "Classname", "Buy Price", "Sell Price"]
        
        for i, label_text in enumerate(labels):
            label = tk.Label(dialog, text=label_text + ":")
            label.grid(row=i, column=0, padx=5, pady=5)
            
            entry = tk.Entry(dialog, width=30)
            entry.insert(tk.END, category_name if i == 0 else class_name if i == 1 else buy_price if i == 2 else sell_price)
            entry.grid(row=i, column=1, padx=5, pady=5)
            
            entries.append(entry)
        
        save_button = tk.Button(dialog, text="Save", command=lambda: save_edited_item(item, *map(tk.Entry.get, entries)))
        save_button.grid(row=len(labels), column=0, columnspan=2, padx=5, pady=10)
        
        dialog.mainloop()
    
    def save_edited_item(item, category_name, class_name, buy_price, sell_price):
        if item:
            treeview.item(item, values=(category_name, class_name, buy_price, sell_price))
            messagebox.showinfo("Item Updated", "The item has been updated successfully.")
    
    window = tk.Toplevel()
    window.title("Trader Manager Editor")
    file_path = filedialog.askopenfilename(title="Open Text File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
    
    if not file_path:
        return
    
    treeview = ttk.Treeview(window, columns=("category", "class_name", "buy_price", "sell_price"))
    treeview.heading("#0", text="Line #")
    treeview.heading("category", text="Category")
    treeview.heading("class_name", text="Classname")
    treeview.heading("buy_price", text="Buy Price")
    treeview.heading("sell_price", text="Sell Price")
    treeview.pack(fill="both", expand=True)
    treeview.bind("<Button-3>", on_right_click)
    
    with open(file_path, "r") as f:
        current_category = None
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            if line.startswith("<Trader>"):
                current_category = line.split("<Trader>")[1].strip()
            else:
                try:
                    class_name, _, buy_price, sell_price = line.split(",")
                    treeview.insert("", "end", text=str(i+1), values=(current_category, class_name.strip(), buy_price.strip(), sell_price.strip()))
                except ValueError:
                    continue
    
    window.mainloop()
