import tkinter as tk
from tkinter import messagebox
import pandas as pd
import os
import random

CSV_FOLDER = "questions"

# Διαβάζει όλες τις ερωτήσεις από όλα τα csv του φακέλου
def load_all_questions(folder):
    questions = []
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            df = pd.read_csv(os.path.join(folder, filename), sep=";")
            questions.extend(df.to_dict(orient="records"))
    return questions

class QuizApp:
    def __init__(self, master, questions):
        self.master = master
        self.master.title("ASEP Quiz")
        self.questions = random.sample(questions, min(15, len(questions)))
        self.current = 0
        self.score = 0

        self.label_enotita = tk.Label(master, font=("Arial", 14, "bold"))
        self.label_enotita.pack(pady=5)
        self.label_q = tk.Label(master, wraplength=450, font=("Arial", 12))
        self.label_q.pack(pady=10)

        self.buttons = []
        for i in range(4):
            btn = tk.Button(master, font=("Arial", 11), width=140, command=lambda idx=i: self.check_answer(idx))
            btn.pack(pady=2)
            self.buttons.append(btn)

        self.label_feedback = tk.Label(master, font=("Arial", 11))
        self.label_feedback.pack(pady=5)

        self.next_btn = tk.Button(master, text="Επόμενη", command=self.next_question)
        self.next_btn.pack(pady=10)
        self.next_btn.config(state="disabled")

        self.show_question()

    def show_question(self):
        q = self.questions[self.current]
        enotita = q.get('Ενότητα', '')
        self.label_enotita.config(text=f"Ενότητα: {enotita}")
        self.label_q.config(text=q["Ερώτηση"])
        options = [q['Α'], q['Β'], q['Γ'], q['Δ']]
        for i, btn in enumerate(self.buttons):
            btn.config(text=f"{chr(913+i)}. {options[i]}", state="normal")
        self.label_feedback.config(text="")
        self.next_btn.config(state="disabled")

    def check_answer(self, idx):
        q = self.questions[self.current]
        correct = q["Σωστή"].strip().upper()
        answer = chr(913+idx)  # "Α", "Β", "Γ", "Δ"
        if answer == correct:
            self.score += 1
            self.label_feedback.config(text="Σωστή!", fg="green")
        else:
            self.label_feedback.config(text=f"Λάθος. Σωστή: {correct}", fg="red")
        for btn in self.buttons:
            btn.config(state="disabled")
        self.next_btn.config(state="normal")

    def next_question(self):
        self.current += 1
        if self.current < len(self.questions):
            self.show_question()
        else:
            messagebox.showinfo("Τέλος Τεστ", f"Σκορ: {self.score} / {len(self.questions)}")
            self.master.destroy()

if __name__ == "__main__":
    all_questions = load_all_questions(CSV_FOLDER)
    if not all_questions:
        print("Δεν βρέθηκαν ερωτήσεις στον φάκελο 'questions'")
    else:
        root = tk.Tk()
        app = QuizApp(root, all_questions)
        root.mainloop()
