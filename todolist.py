import customtkinter as ctk
import json
import os
from tkinter import messagebox

DATA_FILE = "tasks.json"

class TodoApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Studenta Uzdevumu Pārvaldnieks")
        self.geometry("500x600")
        ctk.set_appearance_mode("System")  
        ctk.set_default_color_theme("blue")

        
        self.tasks = []
        self.load_data()

        
        self.create_widgets()

    def create_widgets(self):
        
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(pady=20, padx=20, fill="x")

        self.task_entry = ctk.CTkEntry(self.input_frame, placeholder_text="Ieraksti jaunu uzdevumu...", width=300)
        self.task_entry.pack(side="left", padx=(10, 10), pady=10, expand=True, fill="x")

        self.add_button = ctk.CTkButton(self.input_frame, text="+ Pievienot", command=self.add_task, width=100)
        self.add_button.pack(side="right", padx=(0, 10), pady=10)

        
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text="Tavi uzdevumi")
        self.scrollable_frame.pack(pady=10, padx=20, fill="both", expand=True)

        self.render_tasks()

    def load_data(self):
        """Nolasa datus no JSON faila un apstrādā kļūdas, ja fails nepastāv."""
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as file:
                    self.tasks = json.load(file)
            except json.JSONDecodeError:
                self.tasks = [] 

    def save_data(self):
        """Saglabā uzdevumus JSON failā datu nezūdamībai."""
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(self.tasks, file, indent=4, ensure_ascii=False)

    def add_task(self):
        """Pievieno jaunu uzdevumu, veicot ievades validāciju."""
        task_text = self.task_entry.get().strip()
        
        
        if not task_text:
            messagebox.showwarning("Kļūda", "Uzdevuma teksts nevar būt tukšs!")
            return

        new_task = {"text": task_text, "completed": False}
        self.tasks.append(new_task)
        self.save_data()
        self.task_entry.delete(0, 'end') 
        self.render_tasks()

    def toggle_task(self, index):
        """Maina uzdevuma statusu (izpildīts / neizpildīts)."""
        self.tasks[index]["completed"] = not self.tasks[index]["completed"]
        self.save_data()
        self.render_tasks()

    def delete_task(self, index):
        """Izdzēš uzdevumu no saraksta drošā veidā."""
        del self.tasks[index]
        self.save_data()
        self.render_tasks()

    def render_tasks(self):
        """Izdzēš vecos GUI elementus un pārzīmē sarakstu balstoties uz aktuālajiem datiem."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        for index, task in enumerate(self.tasks):
            task_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
            task_frame.pack(fill="x", pady=5)

            
            font_style = ("Arial", 14, "overstrike") if task["completed"] else ("Arial", 14)
            
            checkbox_var = ctk.BooleanVar(value=task["completed"])
            checkbox = ctk.CTkCheckBox(task_frame, text=task["text"], variable=checkbox_var, 
                                       command=lambda i=index: self.toggle_task(i), font=font_style)
            checkbox.pack(side="left", padx=10, pady=5)

            delete_btn = ctk.CTkButton(task_frame, text="Dzēst", fg_color="#d9534f", hover_color="#c9302c", 
                                       width=60, command=lambda i=index: self.delete_task(i))
            delete_btn.pack(side="right", padx=10)

if __name__ == "__main__":
    app = TodoApp()
    app.mainloop()