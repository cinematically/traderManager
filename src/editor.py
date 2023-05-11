import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from logger import Logger

logger = Logger("[Trader Manager]")

def read_txt_file(file_path):
    logger.log(f"Opened a text file: {file_path}")

    def on_right_click(event):
        item = treeview.selection()
        if item:
            selected_values = treeview.item(item)["values"]
            if len(selected_values) == 4:
                category, class_name, buy_price, sell_price = selected_values
                edit_dialog(item, category, class_name, buy_price, sell_price)  # Pass 'item' to edit_dialog

    def edit_dialog(item, category, class_name, buy_price, sell_price):  # Add 'item' as a parameter
        dialog = tk.Toplevel()
        dialog.title("Edit Item")
        dialog.resizable(0, 0)
        dialog.grab_set()
        dialog.focus_set()

        category_label = tk.Label(dialog, text="Category:")
        category_label.grid(row=0, column=0, padx=5, pady=5)
        category_entry = tk.Entry(dialog, width=30)
        category_entry.insert(tk.END, category)
        category_entry.grid(row=0, column=1, padx=5, pady=5)

        class_label = tk.Label(dialog, text="Class:")
        class_label.grid(row=1, column=0, padx=5, pady=5)
        class_entry = tk.Entry(dialog, width=30)
        class_entry.insert(tk.END, class_name)
        class_entry.grid(row=1, column=1, padx=5, pady=5)

        buy_label = tk.Label(dialog, text="Buy Price:")
        buy_label.grid(row=2, column=0, padx=5, pady=5)
        buy_entry = tk.Entry(dialog, width=30)
        buy_entry.insert(tk.END, buy_price)
        buy_entry.grid(row=2, column=1, padx=5, pady=5)

        sell_label = tk.Label(dialog, text="Sell Price:")
        sell_label.grid(row=3, column=0, padx=5, pady=5)
        sell_entry = tk.Entry(dialog, width=30)
        sell_entry.insert(tk.END, sell_price)
        sell_entry.grid(row=3, column=1, padx=5, pady=5)

        save_button = tk.Button(dialog, text="Save", command=lambda: save_edited_item(item, category_entry.get(), class_entry.get(), buy_entry.get(), sell_entry.get()))  # Pass 'item' to save_edited_item
        save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

        dialog.mainloop()

    def save_edited_item(item, category, class_name, buy_price, sell_price):
        if item:
            treeview.item(item, values=(category, class_name, buy_price, sell_price))
            messagebox.showinfo("Item Updated", "The item has been updated successfully.")

            # Log the item update
            logger.log(f"Item {item} updated - Category: {category}, Class: {class_name}, Buy Price: {buy_price}, Sell Price: {sell_price}")
        else:
            messagebox.showerror("Error", "An error occurred while updating the item.")


    def on_mousewheel(event):
        if event.delta > 0:
            treeview.yview_scroll(-1, "units")
        else:
            treeview.yview_scroll(1, "units")

    window = tk.Toplevel()
    window.title("Trader Manager Editor")

    treeview = ttk.Treeview(window, columns=("category", "class", "buy_price", "sell_price"))
    treeview.heading("#0", text="Line #")
    treeview.heading("category", text="Category")
    treeview.heading("class", text="Class")
    treeview.heading("buy_price", text="Buy Price")
    treeview.heading("sell_price", text="Sell Price")
    treeview.pack(fill="both", expand=True)
    treeview.bind("<Button-3>", on_right_click)
    treeview.bind("<MouseWheel>", on_mousewheel)  # Bind MouseWheel event for scrolling

    current_category = None
    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line:
                # Skip empty lines
                continue
            if line.startswith("<Trader>"):
                current_category = line.split("<Trader>")[1].strip()
            else:
                try:
                    class_name, _, buy_price, sell_price = line.split(",")
                    treeview.insert(
                        "",
                        "end",
                        text=str(i+1),
                        values=(current_category, class_name.strip(), buy_price.strip(), sell_price.strip())
                    )
                except ValueError:
                    # Skip lines that can't be parsed
                    continue

    window.mainloop()

