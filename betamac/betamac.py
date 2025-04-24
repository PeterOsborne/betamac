import tkinter as tk
import csv
import random
import time
import os
from datetime import datetime  # Import datetime module

# === PARAMETERS (Set these values directly) ===
ADDITION_FIRST_RANGE = (2, 100)        # Range for the first number in addition
# Range for the second number in addition
ADDITION_SECOND_RANGE = (2, 100)
# Range for the first number in multiplication
MULTIPLICATION_FIRST_RANGE = (2, 12)
# Range for the second number in multiplication
MULTIPLICATION_SECOND_RANGE = (2, 100)
DURATION = 30                          # Duration of the game in seconds

# === CSV Files ===
results_csv = "/Users/peter/Desktop/Coding/betamac/math_game_results.csv"
summary_csv = "/Users/peter/Desktop/Coding/betamac/math_game_summary.csv"

# === FUNCTIONS ===


def generate_question(question_type):
    if question_type == "addition":
        a = random.randint(*ADDITION_FIRST_RANGE)
        b = random.randint(*ADDITION_SECOND_RANGE)
        question = f"{a} + {b}"
        answer = a + b
    elif question_type == "subtraction":
        a = random.randint(*ADDITION_SECOND_RANGE)
        b = random.randint(*ADDITION_FIRST_RANGE)
        if a < b:
            a, b = b, a  # Ensure non-negative result
        question = f"{a} - {b}"
        answer = a - b
    elif question_type == "multiplication":
        a = random.randint(*MULTIPLICATION_FIRST_RANGE)
        b = random.randint(*MULTIPLICATION_SECOND_RANGE)
        question = f"{a} × {b}"
        answer = a * b
    elif question_type == "division":
        b = random.randint(*MULTIPLICATION_SECOND_RANGE)
        answer = random.randint(*MULTIPLICATION_FIRST_RANGE)
        a = answer * b
        question = f"{a} ÷ {b}"
    else:
        raise ValueError("Unknown question type.")

    return question, answer


def save_results(results):
    os.makedirs(os.path.dirname(results_csv), exist_ok=True)
    file_exists = os.path.isfile(results_csv)
    with open(results_csv, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["question", "time", "type", "datetime"])
        for result in results:
            writer.writerow(
                result + [datetime.now().strftime("%Y-%m-%d %H:%M:%S")])


def save_summary(total_correct):
    os.makedirs(os.path.dirname(summary_csv), exist_ok=True)
    file_exists = os.path.isfile(summary_csv)
    with open(summary_csv, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["datetime", "score", "addition_first_range", "addition_second_range", "multiplication_first_range", "multiplication_first_range", "duration"
                             ])
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # Record current date and time
            total_correct,
            ADDITION_FIRST_RANGE,
            ADDITION_SECOND_RANGE,
            MULTIPLICATION_FIRST_RANGE,
            MULTIPLICATION_SECOND_RANGE,
            DURATION
        ])

# === MATH GAME CLASS ===


class MathGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Math Game")

        # Center the window
        self.center_window(600, 400)

        self.start_time = None
        self.elapsed_time = 0
        self.results = []

        self.main_frame = tk.Frame(root)
        self.main_frame.pack()

        self.question_label = tk.Label(
            self.main_frame, text="Press Start to Begin!", font=("Arial", 20))
        self.question_label.pack(pady=20)

        self.input_var = tk.StringVar()
        self.input_var.trace("w", self.check_answer)

        self.entry = tk.Entry(self.main_frame, font=(
            "Arial", 20), textvariable=self.input_var)
        self.entry.pack(pady=10)

        self.timer_label = tk.Label(
            self.main_frame, text=f"Time Left: {DURATION} seconds", font=("Arial", 14))
        self.timer_label.pack(pady=10)

        self.start_button = tk.Button(self.main_frame, text="Start", font=(
            "Arial", 16), command=self.start_game)
        self.start_button.pack(pady=10)

        self.current_question = None
        self.correct_answer = None
        self.question_type = None

    def center_window(self, width, height):
        """Centers the Tkinter window on the screen."""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def start_game(self):
        self.start_time = time.time()
        self.elapsed_time = 0
        self.results = []
        self.next_question()
        self.update_timer()
        self.entry.focus_set()  # Automatically focus on the input box

    def update_timer(self):
        if self.start_time:
            self.elapsed_time = time.time() - self.start_time
            remaining_time = max(0, DURATION - int(self.elapsed_time))
            self.timer_label.config(
                text=f"Time Left: {remaining_time} seconds")
            if remaining_time > 0:
                self.root.after(1000, self.update_timer)
            else:
                self.end_game()

    def next_question(self):
        self.question_type = random.choice(
            ["addition", "subtraction", "multiplication", "division"])
        self.current_question, self.correct_answer = generate_question(
            self.question_type)
        self.question_label.config(text=self.current_question)
        self.input_var.set("")  # Clear the input box
        self.entry.focus_set()  # Automatically focus on the input box

    def check_answer(self, *args):
        try:
            user_answer = int(self.input_var.get())
            if user_answer == self.correct_answer:
                time_spent = time.time() - self.start_time - \
                    sum([result[1] for result in self.results])
                self.results.append(
                    [self.current_question, round(time_spent, 2), self.question_type])
                self.next_question()
        except ValueError:
            pass  # Ignore non-integer inputs

    def end_game(self):
        self.start_time = None
        total_correct = len(self.results)
        save_results(self.results)
        save_summary(total_correct)
        self.display_end_screen(total_correct)

    def display_end_screen(self, total_correct):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text=f"Game Over!",
                 font=("Arial", 24)).pack(pady=20)
        tk.Label(self.main_frame, text=f"You answered {total_correct} questions correctly.", font=(
            "Arial", 20)).pack(pady=10)
        tk.Button(self.main_frame, text="Start Again", font=(
            "Arial", 16), command=self.reset_game).pack(pady=20)

    def reset_game(self):
        self.main_frame.destroy()  # Properly remove the existing frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        self.question_label = tk.Label(
            self.main_frame, text="Press Start to Begin!", font=("Arial", 20))
        self.question_label.pack(pady=20)

        self.input_var = tk.StringVar()
        self.input_var.trace("w", self.check_answer)

        self.entry = tk.Entry(self.main_frame, font=(
            "Arial", 20), textvariable=self.input_var)
        self.entry.pack(pady=10)

        self.timer_label = tk.Label(
            self.main_frame, text=f"Time Left: {DURATION} seconds", font=("Arial", 14))
        self.timer_label.pack(pady=10)

        self.start_button = tk.Button(self.main_frame, text="Start", font=(
            "Arial", 16), command=self.start_game)
        self.start_button.pack(pady=10)


# === MAIN PROGRAM ===
if __name__ == "__main__":
    root = tk.Tk()
    app = MathGameApp(root)
    root.mainloop()
