import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
from itertools import cycle

class DietGenZ:
    def __init__(self, root):
        self.root = root
        self.root.title("NutriTok 🍔➡️🥑")
        self.root.geometry("500x700")
        self.root.configure(bg="#000000")
        self.root.resizable(False, False)

        # Gen Z color palette
        self.colors = {
            "background": "#000000",
            "accent": "#00ff88",
            "card": "#1a1a1a",
            "text": "#ffffff",
            "select": "#2a2a2a"
        }

        # Category data with emojis and items
        self.categories = {
            "Fruits": ("🍉", ["Apple", "Banana", "Mango", "Strawberry", "Watermelon"]),
            "Vegetables": ("🥦", ["Spinach", "Broccoli", "Carrot", "Cucumber", "Bell Pepper"]),
            "Pulses": ("🌱", ["Lentils", "Chickpeas", "Black Beans", "Kidney Beans", "Soybeans"]),
            "Dairy": ("🥛", ["Milk", "Cheese", "Yogurt", "Butter", "Cream"]),
            "Meat": ("🍗", ["Chicken", "Fish", "Beef", "Eggs", "Turkey"])
        }

        # Selection storage
        self.selections = {category: [] for category in self.categories}
        self.check_vars = {}

        # Create main canvas
        self.canvas = tk.Canvas(root, bg=self.colors["background"], highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        self.scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        # Main container
        self.main_frame = tk.Frame(self.canvas, bg=self.colors["background"])
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Header
        header = tk.Frame(self.main_frame, bg=self.colors["background"], pady=20)
        header.pack(fill=tk.X)
        tk.Label(header, text="🍔 NutriTok", font=("Segoe UI", 24, "bold"), 
                fg=self.colors["accent"], bg=self.colors["background"]).pack()

        # Food selection cards
        self.create_food_cards()

        # Goal selector
        self.goal_var = tk.StringVar()
        goals = ["Lose Weight 🔥", "Gain Muscle 💪", "Stay Fit 😎"]
        self.goal_menu = ttk.Combobox(self.main_frame, textvariable=self.goal_var, 
                                    values=goals, state="readonly", font=("Calibri", 12))
        self.goal_menu.pack(pady=10, padx=20, fill=tk.X)
        self.goal_menu.set("Select Goal ⬇️")

        # Generate button
        gen_button = tk.Button(self.main_frame, text="Create My Plan ✨", command=self.generate_plan,
                              bg=self.colors["accent"], fg="black", font=("Calibri", 14, "bold"),
                              borderwidth=0, relief=tk.FLAT, padx=30, pady=10)
        gen_button.pack(pady=20)

        # Loading animation
        self.loading_states = cycle(["💫", "✨", "🌟", "⚡"])
        self.loading_label = tk.Label(self.main_frame, text="", font=("Calibri", 14),
                                     bg=self.colors["background"], fg=self.colors["accent"])

        # Configure scrolling
        self.main_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def create_food_cards(self):
        """Create selectable food cards with checkboxes"""
        for category, (emoji, items) in self.categories.items():
            card = tk.Frame(self.main_frame, bg=self.colors["card"], padx=15, pady=10,
                           highlightbackground=self.colors["accent"], highlightthickness=1)
            card.pack(pady=5, padx=20, fill=tk.X)

            # Header with emoji
            header = tk.Frame(card, bg=self.colors["card"])
            header.pack(fill=tk.X)
            tk.Label(header, text=f"{emoji} {category}", font=("Segoe UI", 12, "bold"),
                    fg=self.colors["text"], bg=self.colors["card"]).pack(side=tk.LEFT)

            # Checkboxes for items
            self.check_vars[category] = {}
            item_frame = tk.Frame(card, bg=self.colors["card"])
            item_frame.pack(fill=tk.X)
            
            for idx, item in enumerate(items):
                var = tk.IntVar()
                self.check_vars[category][item] = var
                
                cb = tk.Checkbutton(
                    item_frame, 
                    text=item,
                    variable=var,
                    bg=self.colors["card"],
                    fg=self.colors["text"],
                    selectcolor=self.colors["select"],
                    activebackground=self.colors["card"],
                    activeforeground=self.colors["text"],
                    font=("Calibri", 11),
                    anchor="w"
                )
                cb.grid(row=idx//2, column=idx%2, sticky="w", padx=5, pady=2)

    def generate_plan(self):
        """Collect selections and generate plan"""
        # Get selected items
        selected_items = []
        for category in self.categories:
            for item, var in self.check_vars[category].items():
                if var.get() == 1:
                    selected_items.append(f"{category}: {item}")
        
        if not selected_items:
            messagebox.showwarning("Oops!", "Please select at least one item! 🙏")
            return

        # Show loading
        self.loading_label.pack()
        self.animate_loading()
        
        # Generate plan (mock example)
        self.root.after(2000, lambda: self.show_result(selected_items))

    def animate_loading(self):
        self.loading_label.config(text=f"Generating {next(self.loading_states)}")
        self.root.after(200, self.animate_loading)

    def show_result(self, selected_items):
        self.loading_label.pack_forget()
        
        # Create formatted plan
        plan = "Your Personalized Plan:\n\n" + "\n".join([
            f"Day {i+1}: {items} 🍽️" 
            for i, items in enumerate(chunk_list(selected_items, 3))
        ])
        
        messagebox.showinfo("Your Plan ✨", plan)

def chunk_list(lst, n):
    """Split list into chunks"""
    return [lst[i:i+n] for i in range(0, len(lst), n)]

if __name__ == "__main__":
    root = tk.Tk()
    app = DietGenZ(root)
    root.mainloop()