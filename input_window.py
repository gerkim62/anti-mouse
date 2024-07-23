import tkinter as tk
from tkinter import font
import webbrowser

class InputWindow:
    def __init__(self, api_client):
        self.root = tk.Tk()
        self.root.withdraw()
        self.api_client = api_client
        self.input_window = None
        self.current_focus = 0
        self.focusable_widgets = []

    def show(self):
        if self.input_window is None or not self.input_window.winfo_exists():
            self.create_window()
        else:
            self.input_window.deiconify()
        self.entry.focus_set()

    def create_window(self):
        self.input_window = tk.Toplevel(self.root)
        self.input_window.title("Mouse Alternative")
        self.input_window.geometry("700x400")  # Set a default size
        self.input_window.wm_minsize(700, 400)  # Set minimum width and height

        # Configure grid to expand properly
        self.input_window.rowconfigure(1, weight=1)  # Chat frame row
        self.input_window.columnconfigure(0, weight=1)  # All content in one column

        # Message frame
        message_frame = tk.Frame(self.input_window, bg="#f0f0f0")
        message_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        message_text = "Don't use mouse, ask AI for alternative. "
        message_label = tk.Label(message_frame, text=message_text, 
                                 font=("Helvetica", 14), bg="#f0f0f0", fg="#333333")
        message_label.pack(side=tk.LEFT, pady=5)
        
        self.link_button = tk.Button(message_frame, text="Learn why (Alt+W)", 
                                     font=("Helvetica", 14), bg="#f0f0f0", fg="blue",
                                     cursor="hand2", relief=tk.FLAT, 
                                     command=self.open_link)
        self.link_button.pack(side=tk.LEFT, pady=5)
        
        esc_label = tk.Label(message_frame, text="Press Esc key to close", 
                             font=("Helvetica", 12), bg="#f0f0f0", fg="#666666")
        esc_label.pack(side=tk.RIGHT, pady=5)

        # Chat display frame
        chat_frame = tk.Frame(self.input_window, bg="white")
        chat_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        self.result_text = tk.Text(chat_frame, wrap=tk.WORD, state=tk.DISABLED, bg="white", font=("Helvetica", 14))
        self.result_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input frame
        input_frame = tk.Frame(self.input_window, bg="#f0f0f0")
        input_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        input_frame.columnconfigure(0, weight=1)
        self.entry = tk.Entry(input_frame, font=("Helvetica", 18))
        self.entry.grid(row=0, column=0, sticky="ew", padx=5, pady=10)
        
        self.submit_button = tk.Button(input_frame, text="Submit (Enter)", command=self.submit, 
                                       bg="#4CAF50", fg="white", font=("Helvetica", 18))
        self.submit_button.grid(row=0, column=1, padx=5, pady=10)

        # Set up keyboard navigation
        self.focusable_widgets = [self.link_button, self.entry, self.submit_button]
        self.input_window.bind('<Tab>', self.focus_next_widget)
        self.input_window.bind('<Shift-Tab>', self.focus_previous_widget)
        self.input_window.bind('<Alt-w>', lambda e: self.open_link())
        self.input_window.bind('<Return>', lambda event: self.submit())
        self.input_window.bind('<Escape>', self.hide_window)
        self.input_window.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.input_window.after(100, self.entry.focus_set)

    def open_link(self):
        webbrowser.open_new("https://example.com/why-use-ai")

    def focus_next_widget(self, event):
        self.current_focus = (self.current_focus + 1) % len(self.focusable_widgets)
        self.focusable_widgets[self.current_focus].focus_set()
        return "break"

    def focus_previous_widget(self, event):
        self.current_focus = (self.current_focus - 1) % len(self.focusable_widgets)
        self.focusable_widgets[self.current_focus].focus_set()
        return "break"

    def submit(self):
        query = self.entry.get()
        response = self.api_client.get_alternative(query)
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, f"You: {query}\n", "user")
        self.result_text.insert(tk.END, f"Bot: {response}\n", "bot")
        self.result_text.config(state=tk.DISABLED)
        self.result_text.see(tk.END)
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def hide_window(self, event=None):
        if self.input_window:
            self.input_window.withdraw()

    def run(self):
        self.root.mainloop()
