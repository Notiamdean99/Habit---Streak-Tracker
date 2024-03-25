import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime, timedelta
import pickle
import os

class HabitTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Habit Tracker")
        self.root.geometry('1200x600')  # Set the window size
        self.load_data()  # Load habits, lifelines, and other data
        self.build_ui()  # Construct the UI

    def build_ui(self):
        self.root.configure(bg="#f0f0f0")
        self.header_frame = tk.Frame(self.root, bg="#4f5d75")
        self.header_frame.pack(fill=tk.X)
        
        tk.Label(self.header_frame, text="Habit Tracker", font=("Arial", 24), bg="#4f5d75", fg="white").pack(pady=20)

        self.add_habit_button = tk.Button(self.header_frame, text="➕ Add Habit", command=self.show_add_habit_ui, font=("Arial", 12), bg="#ef8354", fg="white")
        self.add_habit_button.pack(side=tk.LEFT, padx=20)

        self.lifeline_label = tk.Label(self.header_frame, text=f"Lifelines: {self.lifelines}", font=("Arial", 12), bg="#4f5d75", fg="white")
        self.lifeline_label.pack(side=tk.LEFT, padx=10)

        self.habit_list_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.habit_list_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.refresh_habits_display()

    def show_add_habit_ui(self):
        habit_name = simpledialog.askstring("Add Habit", "Habit Name:", parent=self.root)
        if habit_name:
            habit_name = habit_name.strip()
            if habit_name not in self.habits:
                self.habits[habit_name] = [0, None]  # Initialize with streak and last completion date
                self.save_data()
                self.refresh_habits_display()
            else:
                messagebox.showinfo("Duplicate", "This habit already exists.")

    def delete_habit(self, habit):
        if messagebox.askyesno("Delete Habit", f"Are you sure you want to delete '{habit}'?"):
            del self.habits[habit]
            self.save_data()
            self.refresh_habits_display()

    def mark_done(self, habit):
        today = datetime.now().date()
        streak, last_done = self.habits[habit]

        if last_done is None or last_done < today - timedelta(days=1):
            streak += 1
            if streak % self.lifeline_interval == 0:
                self.lifelines += 1
        elif last_done == today:
            messagebox.showinfo("Already Done", f"'{habit}' has already been marked as done today.")
            return
        else:
            streak = 1  # Reset streak to 1 instead of 0 to acknowledge today's completion
            self.fails += 1
            self.lifeline_interval += 5

        self.habits[habit] = [streak, today]
        self.save_data()
        self.refresh_habits_display()

    def refresh_habits_display(self):
        for widget in self.habit_list_frame.winfo_children():
            widget.destroy()

        for habit, (streak, _) in self.habits.items():
            habit_frame = tk.Frame(self.habit_list_frame, bg="#f0f0f0")
            habit_frame.pack(fill=tk.X, pady=5)

            tk.Label(habit_frame, text=habit, font=("Arial", 14), bg="#f0f0f0").pack(side=tk.LEFT, padx=10)

            stars = '★' * streak + f" ({streak})"
            tk.Label(habit_frame, text=stars, font=("Arial", 14), fg="#ffd700", bg="#f0f0f0").pack(side=tk.LEFT, padx=10)

            tk.Button(habit_frame, text="Done Today", command=lambda h=habit: self.mark_done(h), bg="#2d3142", fg="white").pack(side=tk.RIGHT, padx=10)
            tk.Button(habit_frame, text="Delete", command=lambda h=habit: self.delete_habit(h), bg="#bfc0c0", fg="black").pack(side=tk.RIGHT, padx=5)

        self.lifeline_label.config(text=f"Lifelines: {self.lifelines}")

    def load_data(self):
        if os.path.exists("data.dat"):
            with open("data.dat", "rb") as file:
                data = pickle.load(file)
                self.habits = data.get('habits', {})
                self.lifelines = data.get('lifelines', 0)
                self.fails = data.get('fails', 0)
                self.lifeline_interval = data.get('lifeline_interval', 30)
        else:
            self.habits = {}
            self.lifelines = 0
            self.fails = 0
            self.lifeline_interval = 30

    def save_data(self):
        with open("data.dat", "wb") as file:
            data = {
                'habits': self.habits,
                'lifelines': self.lifelines,
                'fails': self.fails,
                'lifeline_interval': self.lifeline_interval
            }
            pickle.dump(data, file)

if __name__ == "__main__":
    root = tk.Tk()
    app = HabitTracker(root)
    root.mainloop()
