import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

def read_txt_file():
    window = tk.Toplevel()
    window.title("Trader Manager Editor")
    file_path = filedialog.askopenfilename(
        title="Open Text File",
        filetypes=(("Text Files", "*.txt"), ("All Files", "*.*"))
    )
    
    if not file_path:
        return
    treeview = ttk.Treeview(window, columns=("class", "item", "buy_price", "sell_price"))
    treeview.heading("#0", text="Line #")
    treeview.heading("class", text="Class")
    treeview.heading("item", text="Item")
    treeview.heading("buy_price", text="Buy Price")
    treeview.heading("sell_price", text="Sell Price")
    treeview.pack(fill="both", expand=True)
    current_class = None
    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                # Skip empty lines
                continue
            if line.startswith("<Trader>"):
                current_class = line.split("<Trader>")[1].strip()
            else:
                try:
                    item, _, buy_price, sell_price = line.split(",")
                    treeview.insert(
                        "",
                        "end",
                        text=str(i+1),
                        values=(current_class, item.strip(), buy_price.strip(), sell_price.strip())
                    )
                except ValueError:
                    # Skip lines that can't be parsed
                    continue
    window.mainloop()
