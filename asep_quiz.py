
import os
import pandas as pd
import random

# Φάκελος με όλα τα CSV αρχεία ερωτήσεων
CSV_FOLDER = "questions"

def load_all_questions(folder):
    questions = []
    for filename in os.listdir(folder):
        if filename.endswith(".csv"):
            filepath = os.path.join(folder, filename)
            df = pd.read_csv(filepath, sep=";")
            questions.extend(df.to_dict(orient="records"))
    return questions

def run_quiz(questions, num_questions=10):
    selected = random.sample(questions, min(num_questions, len(questions)))
    score = 0
    for i, q in enumerate(selected, 1):
        print(f"\nΕρώτηση {i} ({q['Ερώτηση']}):")
        # print(q['Ερώτηση'])
        print(f"Α. {q['Α']}")
        print(f"Β. {q['Β']}")
        print(f"Γ. {q['Γ']}")
        print(f"Δ. {q['Δ']}")
        answer = input("Απάντηση (Α/Β/Γ/Δ): __|__").strip().upper()
        if answer == q['Σωστή']:
            print("Σωστή.")
            score += 1
        else:
            print(f"Λάθος. Σωστή απάντηση: {q['Σωστή']}")
    print(f"\nΤελικό σκορ: {score}/{len(selected)}")

if __name__ == "__main__":
    print("Φόρτωση ερωτήσεων...")
    all_questions = load_all_questions(CSV_FOLDER)
    if not all_questions:
        print("Δεν βρέθηκαν ερωτήσεις.")
    else:
        run_quiz(all_questions, num_questions=10)
