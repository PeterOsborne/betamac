import tkinter as tk
import csv
import random
import time
import os
from datetime import datetime

# === PARAMETERS ===
DURATION = 30  # Duration of the game in seconds
CSV_PATH = "/Users/peter/Desktop/Coding/betamac/odds_converter_results.csv"
SUMMARY_PATH = "/Users/peter/Desktop/Coding/betamac/odds_converter_summary.csv"


def get_random_probability():
    denominators = [2, 3, 4, 5, 6, 8, 10, 12, 20]
    denom = random.choice(denominators)
    numer = random.randint(1, denom - 1)
    return numer, denom, numer / denom


class OddsGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Odds Converter Game")
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
        self.correct_odds = None
        self.display_type = None
        self.decimal_score = 0
        self.fraction_score = 0

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def start_game(self):
        self.start_time = time.time()
        self.elapsed_time = 0
        self.results = []
        self.decimal_score = 0
        self.fraction_score = 0
        self.next_question()
        self.update_timer()
        self.entry.focus_set()

    def update_timer(self):
        if self.start_time:
            self.elapsed_time = time.time() - self.start_time
            remaining_time = max(0, DURATION - int(self.elapsed_time))
            self.timer_label.config(text=f"Time Left: {remaining_time} seconds")
            if remaining_time > 0:
                self.root.after(1000, self.update_timer)
            else:
                self.end_game()

    def next_question(self):
        numer, denom, p = get_random_probability()
        self.correct_odds = 1 / p
        self.display_type = random.choice(["fraction", "decimal"])

        if self.display_type == "fraction":
            question = f"Convert probability {numer}/{denom} to decimal odds:"
        else:
            question = f"Convert probability {p:.4f} to decimal odds:"

        self.current_question = question
        self.question_label.config(text=question)
        self.input_var.set("")
        self.entry.focus_set()

    def check_answer(self, *args):
        if not self.start_time:
            return
        try:
            user_answer = float(self.input_var.get())
            error = abs(user_answer - self.correct_odds)
            if error < 0.05:
                time_spent = time.time() - self.start_time - sum([r[1] for r in self.results])
                self.results.append([self.current_question, round(time_spent, 2), self.display_type])
                if self.display_type == "fraction":
                    self.fraction_score += 1
                else:
                    self.decimal_score += 1
                self.next_question()
        except ValueError:
            pass

    def end_game(self):
        self.start_time = None
        total_score = len(self.results)
        self.save_results()
        self.save_summary(total_score)
        self.display_end_screen(total_score)

    def save_results(self):
        os.makedirs(os.path.dirname(CSV_PATH), exist_ok=True)
        file_exists = os.path.isfile(CSV_PATH)
        with open(CSV_PATH, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["question", "time", "type", "datetime"])
            for result in self.results:
                writer.writerow(result + [datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    def save_summary(self, total_correct):
        os.makedirs(os.path.dirname(SUMMARY_PATH), exist_ok=True)
        file_exists = os.path.isfile(SUMMARY_PATH)
        with open(SUMMARY_PATH, mode="a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["datetime", "score", "decimal_score", "fraction_score", "duration"])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                total_correct,
                self.decimal_score,
                self.fraction_score,
                DURATION
            ])

    def display_end_screen(self, total_correct):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="Game Over!", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.main_frame, text=f"You answered {total_correct} questions correctly.", font=("Arial", 20)).pack(pady=10)
        tk.Button(self.main_frame, text="Start Again", font=("Arial", 16), command=self.reset_game).pack(pady=20)

    def reset_game(self):
        self.main_frame.destroy()
        self.__init__(self.root)


# === MAIN PROGRAM ===
if __name__ == "__main__":
    root = tk.Tk()
    app = OddsGameApp(root)
    root.mainloop()
