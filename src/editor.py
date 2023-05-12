import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from logger import Logger

class Editor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.logger = Logger("[Trader Manager]")
        self.window = tk.Toplevel()
        self.window.title("Trader Manager Editor")

        # Configure the styling of the editor
        self.window.configure(bg="#303030")

        # Configure the styling of the treeview
        style = ttk.Style()
        style.configure("Custom.Treeview", background="#303030", foreground="#FFFFFF", fieldbackground="#303030")
        style.map("Custom.Treeview", background=[("selected", "#1E90FF")])

        self.treeview = ttk.Treeview(self.window, columns=("category", "class", "buy_price", "sell_price"), style="Custom.Treeview")
        self.treeview.heading("#0", text="Line #", anchor=tk.CENTER, command=lambda: self.sort_lines())
        self.treeview.heading("category", text="Category", anchor=tk.CENTER)
        self.treeview.heading("class", text="Class", anchor=tk.CENTER, command=lambda: self.sort_by_column("class"))
        self.treeview.heading("buy_price", text="Buy Price", anchor=tk.CENTER, command=lambda: self.sort_by_column("buy_price"))
        self.treeview.heading("sell_price", text="Sell Price", anchor=tk.CENTER, command=lambda: self.sort_by_column("sell_price"))
        self.treeview.tag_configure("heading", font=("Arial", 12, "bold"))
        self.treeview.pack(fill="both", expand=True)

        # Bind the right-click event to the treeview
        self.treeview.bind("<Button-3>", self.on_right_click)

        self.populate_treeview()

        self.window.mainloop()

    def on_right_click(self, event):
        item = self.treeview.identify("item", event.x, event.y)
        if item:
            selected_values = self.treeview.item(item, "values")
            if selected_values:
                category, class_name, buy_price, sell_price = selected_values
                self.edit_dialog(item, category, class_name, buy_price, sell_price)
    def edit_dialog(self, item, category, class_name, buy_price, sell_price):
        dialog = tk.Toplevel()
        dialog.title("Edit Item")
        dialog.configure(bg="#303030")
        dialog.resizable(0, 0)
        dialog.grab_set()
        dialog.focus_set()
        label_style = ttk.Style()
        label_style.configure("Custom.TLabel", foreground="#FFFFFF", background="#303030")
        entry_style = ttk.Style()
        label_style.configure("Custom.TLabel", foreground="#FFFFFF", background="#303030")
        entry_style = ttk.Style()
        entry_style.configure("Custom.TEntry", foreground="#000000", background="#FFFFFF")

        category_label = ttk.Label(dialog, text="Category:", style="Custom.TLabel")
        category_label.grid(row=0, column=0, padx=5, pady=5)
        category_entry = ttk.Entry(dialog, width=30, style="Custom.TEntry")
        category_entry.insert(tk.END, category)
        category_entry.grid(row=0, column=1, padx=5, pady=5)

        class_label = ttk.Label(dialog, text="Class:", style="Custom.TLabel")
        class_label.grid(row=1, column=0, padx=5, pady=5)
        class_entry = ttk.Entry(dialog, width=30, style="Custom.TEntry")
        class_entry.insert(tk.END, class_name)
        class_entry.grid(row=1, column=1, padx=5, pady=5)

        buy_label = ttk.Label(dialog, text="Buy Price:", style="Custom.TLabel")
        buy_label.grid(row=2, column=0, padx=5, pady=5)
        buy_entry = ttk.Entry(dialog, width=30, style="Custom.TEntry")
        buy_entry.insert(tk.END, buy_price)
        buy_entry.grid(row=2, column=1, padx=5, pady=5)

        sell_label = ttk.Label(dialog, text="Sell Price:", style="Custom.TLabel")
        sell_label.grid(row=3, column=0, padx=5, pady=5)
        sell_entry = ttk.Entry(dialog, width=30, style="Custom.TEntry")
        sell_entry.insert(tk.END, sell_price)
        sell_entry.grid(row=3, column=1, padx=5, pady=5)

        save_button = ttk.Button(dialog, text="Save", command=lambda: self.save_edited_item(item, category_entry, class_entry, buy_entry, sell_entry))
        save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10)

        self.dialog = dialog  # Store the dialog reference in the instance variable

        dialog.mainloop()

    def populate_treeview(self):
        current_category = None
        with open(self.file_path, "r") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                if line.startswith("<Trader>"):
                    current_category = line.split("<Trader>")[1].strip()
                else:
                    try:
                        class_name, _, buy_price, sell_price = line.split(",")
                        self.treeview.insert(
                            "",
                            "end",
                            text=str(i + 1),
                            values=(current_category, class_name.strip(), buy_price.strip(), sell_price.strip())
                        )
                    except ValueError:
                        continue

    def sort_lines(self):
        # Sort the lines of the treeview by line number
        items = [(self.treeview.index(item), item) for item in self.treeview.get_children()]
        items.sort(key=lambda x: int(x[0]))
        for index, (_, item) in enumerate(items):
            self.treeview.move(item, "", index)

    def sort_by_column(self, column):
        # Sort the treeview by the specified column
        items = [(self.treeview.set(item, column), item) for item in self.treeview.get_children()]
        items.sort(key=lambda x: x[0])
        for index, (_, item) in enumerate(items):
            self.treeview.move(item, "", index)

    def save_edited_item(self, item, category, class_name, buy_price, sell_price):
        # Get the values from the entry fields
        category_value = category.get()
        class_value = class_name.get()
        buy_price_value = buy_price.get()
        sell_price_value = sell_price.get()

        # Validate the values (add your own validation logic)
        if not category_value or not class_value or not buy_price_value or not sell_price_value:
            messagebox.showwarning("Validation Error", "Please fill in all fields.")
            return

        # Get the original values
        original_values = self.treeview.item(item, "values")

        # Update the values in the treeview
        self.treeview.item(item, values=(category_value, class_value, buy_price_value, sell_price_value))

        # Generate the log message
        log_message = f"Changed line {item}:"
        changes = []

        # Check if category value changed
        if original_values[0] != category_value:
            changes.append(f"Category: {original_values[0]} -> {category_value}")
        # Check if class value changed
        if original_values[1] != class_value:
            changes.append(f"Class: {original_values[1]} -> {class_value}")
        # Check if buy price value changed
        if original_values[2] != buy_price_value:
            changes.append(f"New Buy Price: {original_values[2]} -> {buy_price_value}")
        # Check if sell price value changed
        if original_values[3] != sell_price_value:
            changes.append(f"New Sell Price: {original_values[3]} -> {sell_price_value}")

        # Log the changes
        if changes:
            log_message += "\n" + "\n".join(changes)
            self.logger.log(log_message)

        # Close the dialog
        dialog = category.winfo_toplevel()
        dialog.destroy()
