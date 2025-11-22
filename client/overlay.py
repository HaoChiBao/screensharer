import tkinter as tk

class SelectionOverlay:
    def __init__(self, on_selection_complete):
        self.root = tk.Tk()
        # Make it fullscreen and transparent
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-alpha', 0.3)
        self.root.attributes('-topmost', True) # Important for macOS
        self.root.configure(background='black') # Darker background for better contrast
        
        self.start_x = None
        self.start_y = None
        self.current_rect = None
        
        self.on_selection_complete = on_selection_complete
        
        self.canvas = tk.Canvas(self.root, cursor="cross", bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        # Add instruction text
        self.text_id = self.canvas.create_text(
            self.root.winfo_screenwidth() // 2, 
            self.root.winfo_screenheight() // 2, 
            text="Click and drag to select area\nPress Esc to cancel", 
            fill="white", font=("Arial", 24)
        )
        
        self.canvas.bind("<ButtonPress-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_move_press)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)
        
        self.root.bind("<Escape>", lambda e: self.root.destroy())
        
        # Force focus
        self.root.focus_force()

    def on_button_press(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.current_rect:
            self.canvas.delete(self.current_rect)
        self.current_rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=4
        )

    def on_move_press(self, event):
        cur_x, cur_y = (event.x, event.y)
        self.canvas.coords(self.current_rect, self.start_x, self.start_y, cur_x, cur_y)

    def on_button_release(self, event):
        end_x, end_y = (event.x, event.y)
        
        # Calculate coordinates
        x1 = min(self.start_x, end_x)
        y1 = min(self.start_y, end_y)
        x2 = max(self.start_x, end_x)
        y2 = max(self.start_y, end_y)
        
        width = x2 - x1
        height = y2 - y1
        
        # Ensure meaningful selection
        if width > 10 and height > 10:
            selection = {'top': y1, 'left': x1, 'width': width, 'height': height}
            print(f"Selected area: {selection}")
            self.root.destroy()
            self.on_selection_complete(selection)
        else:
            print("Selection too small, try again.")
            if self.current_rect:
                self.canvas.delete(self.current_rect)

    def start(self):
        print("Select an area on the screen (Esc to cancel)")
        self.root.mainloop()
