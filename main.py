import tkinter as tk
from tkinter import messagebox
from editor import read_txt_file

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My App")
        self.root.overrideredirect(True)
        width, height = 400, 300
        x = (self.root.winfo_screenwidth() / 2) - (width / 2)
        y = (self.root.winfo_screenheight() / 2) - (height / 2)
        self.root.geometry("%dx%d+%d+%d" % (width, height, x, y))
        self.root.config(bg="#212121")
        self.root.attributes('-alpha', 0.7)
        self.root.resizable(0, 0)
        self.right_click_menu = tk.Menu(self.root, tearoff=0)
        self.right_click_menu.add_command(label="Fullscreen", command=self.toggle_fullscreen)
        self.right_click_menu.add_command(label="Close", command=self.close_app)
        self.root.bind("<Button-3>", self.show_right_click_menu)
        self.frame = tk.Frame(self.root, bg="#424242")
        self.frame.pack(fill="both", expand=True)
        title_font, label_font, button_font = ("Segoe UI", 20, "bold"), ("Segoe UI", 12), ("Segoe UI", 12, "bold")
        tk.Label(self.frame, text="Trader Manager ", font=title_font, fg="#FFFFFF", bg="#424242").pack(pady=20)
        tk.Label(self.frame, text="the start of a journey..", font=label_font, fg="#FFFFFF", bg="#424242").pack(pady=10)
        self.x, self.y = None, None
        self.root.bind("<ButtonPress-1>", self.start_move)
        self.root.bind("<ButtonRelease-1>", self.stop_move)
        self.root.bind("<B1-Motion>", self.on_move)
        tk.Button(self.frame, text="Open Editor", font=button_font, command=self.open_editor).pack(pady=10)

    def open_editor(self):
        import editor
        editor.read_txt_file()

    def start_move(self, event):
        self.x, self.y = event.x, event.y

    def stop_move(self, event):
        self.x, self.y = None, None

    def on_move(self, event):
        if self.x is not None and self.y is not None:
            deltax, deltay = event.x - self.x, event.y - self.y
            x, y = self.root.winfo_x() + deltax, self.root.winfo_y() + deltay
            self.root.geometry("+%s+%s" % (x, y))

    def show_right_click_menu(self, event):
        try:
            self.right_click_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.right_click_menu.grab_release()

    def toggle_fullscreen(self):
        if self.root.attributes('-fullscreen'):
            self.root.attributes('-fullscreen', False)
            self.root.geometry("400x300+100+100")
        elif not self.root.overrideredirect():
            self.root.attributes('-fullscreen', True)
        else:
            messagebox.showwarning("Error", "Cannot set full screen mode while the window border is removed.")

    def close_app(self):
        self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = MyApp(root)
    root.mainloop()