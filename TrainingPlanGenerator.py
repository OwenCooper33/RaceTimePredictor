import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
from PIL import Image, ImageTk
import os

class TrainingPlanGenerator(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Training Plan Generator")
        self.geometry("800x900")

        self.background_image_path = "/Users/owencooper/Desktop/IdeaProjects/TrainingPlanGeneratorPython/venv/Firefly cartoon mountains 75569.jpg"
        self.file_name = "RoundTheIslandPlan.txt"

        # Load and set background image
        self.background_image = Image.open(self.background_image_path)
        self.background_image = self.background_image.resize((1500, 1600), Image.LANCZOS)
        self.background_photo = ImageTk.PhotoImage(self.background_image)
        self.background_label = tk.Label(self, image=self.background_photo)
        self.background_label.place(relwidth=1, relheight=1)

        self.goal_mileage_label = tk.Label(self, text="Enter your event length:", font=("Arial", 20, "bold"), bg='black', fg='white')
        self.goal_mileage_label.pack(pady=10)

        self.goal_mileage_entry = tk.Entry(self)
        self.goal_mileage_entry.pack(pady=10)

        self.daily_mileage_label = tk.Label(self, text="Enter your current average run length:", font=("Arial", 20, "bold"), bg='black', fg='white')
        self.daily_mileage_label.pack(pady=10)

        self.daily_mileage_entry = tk.Entry(self)
        self.daily_mileage_entry.pack(pady=10)

        self.runs_per_week = tk.Label(self, text="Runs per week:", font=("Arial", 20, "bold"), bg='black', fg='white')
        self.runs_per_week.pack(pady=10)

        self.daily_mileage_entry = tk.Entry(self)
        self.daily_mileage_entry.pack(pady=10)

        self.generate_button = tk.Button(self, text="Generate Plan", command=self.generate_plan, font=("Arial", 20, "bold"), bg='darkgray', fg='black')
        self.generate_button.pack(pady=10)

        self.plan_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, width=50, height=10)
        self.plan_area.pack(pady=10)

        self.file_link_label = tk.Label(self, text="Download your training plan", fg='blue', cursor="hand2", font=("Arial", 12, "underline"))
        self.file_link_label.pack(pady=10)
        self.file_link_label.bind("<Button-1>", self.open_file)
        self.file_link_label.pack_forget()  # Hide initially

    def generate_plan(self):
        try:
            goal_mileage = float(self.goal_mileage_entry.get())
            daily_mileage = float(self.daily_mileage_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers.")
            return

        long_run = daily_mileage * 1.7
        weeks = self.calculate_weeks(long_run, goal_mileage)
        weekly_mileage = daily_mileage * 4 + long_run

        plan = []

        for i in range(weeks):
            weekly_workouts = (f"Week: {i + 1} Total Mileage: {round(weekly_mileage * 2) / 2.0}\n"
                               f"Monday: {round(daily_mileage * 2) / 2.0} miles easy\n"
                               f"Tuesday: ~{round((daily_mileage - 0.2 * daily_mileage) * 2) / 2.0} miles hill repeats\n"
                               f"Wednesday: rest\n"
                               f"Thursday: {round((daily_mileage + 0.2 * daily_mileage) * 2) / 2.0} miles tempo\n"
                               f"Friday: {round(daily_mileage * 2) / 2.0} miles easy\n"
                               f"Saturday: {round(long_run * 2) / 2.0} miles easy\n"
                               f"Sunday: rest\n\n")
            plan.append(weekly_workouts)
            daily_mileage *= 1.15
            long_run *= 1.15
            weekly_mileage *= 1.15

        plan_text = "".join(plan)

        with open(self.file_name, 'w') as file:
            file.write(plan_text)

        self.plan_area.delete(1.0, tk.END)
        self.plan_area.insert(tk.END, plan_text)
        self.file_link_label.pack()

    def open_file(self, event):
        if os.path.exists(self.file_name):
            os.startfile(self.file_name)
        else:
            messagebox.showerror("Error", "File not found.")

    @staticmethod
    def calculate_weeks(start, end):
        weeks = 0
        while start <= end * 0.7:
            start *= 1.14
            weeks += 1
        return weeks

if __name__ == "__main__":
    app = TrainingPlanGenerator()
    app.mainloop()