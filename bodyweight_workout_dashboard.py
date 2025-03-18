import random
import json
import os

SAVE_FILE = "progress.json"

#data definitions

muscle_groups = {
    "Abs": [
        {"name": "Hollow Body Hold", "progression": ["15s", "20s", "25s", "30s"]},
        {"name": "Bicycle Crunches", "progression": ["20 reps", "24 reps", "28 reps", "32 reps"]}
    ],
    "Legs": [
        {"name": "Bodyweight Squats", "progression": ["15 reps", "18 reps", "21 reps", "24 reps"]},
        {"name": "Reverse Lunges", "progression": ["10 reps/leg", "12 reps/leg", "14 reps/leg", "16 reps/leg"]}
    ],
    "Push": [
        {"name": "Push-Ups", "progression": ["12 reps", "15 reps", "18 reps", "20 reps"]},
        {"name": "Tricep Dips", "progression": ["12 reps", "15 reps", "18 reps", "20 reps"]}
    ],
    "Pull": [
        {"name": "Superman Pulls", "progression": ["12 reps", "15 reps", "18 reps", "20 reps"]},
        {
            "name": "Inverted Rows (or alternatives)",
            "progression": ["8 reps", "10 reps", "12 reps", "15 reps"],
            "alternatives": ["Doorframe Rows", "Towel Rows", "Superman T Raises", "Reverse Snow Angels"]
        }
    ]
}

#progress 

def load_progress():
    if not os.path.exists(SAVE_FILE):
        return {"current_day": 1}
    with open(SAVE_FILE, "r") as file:
        return json.load(file)

def save_progress(progress):
    with open(SAVE_FILE, "w") as file:
        json.dump(progress, file)

def reset_progress():
    progress = {"current_day": 1}
    save_progress(progress)
    print("\n Progress reset to Day 1.")
    return progress


#workout generation


def get_week_number(day):
    return min(((day - 1) // 7) + 1, 4)

def get_day_of_cycle(day):
    return ((day - 1) % 7) + 1

def generate_group_workout(groups, week_number):
    for group in groups:
        print(f"\n🏋️ {group}:")
        for ex in muscle_groups[group]:
            prog = ex['progression'][week_number - 1]
            print(f" - {ex['name']}: {prog}")
            if 'alternatives' in ex:
                alt = random.choice(ex['alternatives'])
                print(f"   (Alternative option: {alt})")

def generate_circuit_workout(week_number):
    for group in muscle_groups.keys():
        print(f"\n🏋️ {group}:")
        for ex in muscle_groups[group]:
            prog = ex['progression'][week_number - 1]
            print(f" - {ex['name']}: {prog}")
            if 'alternatives' in ex:
                alt = random.choice(ex['alternatives'])
                print(f"   (Alternative option: {alt})")

def generate_workout_by_day(day):
    if day < 1 or day > 30:
        print("Day out of range (1-30).")
        return

    day_of_cycle = get_day_of_cycle(day)
    week_number = get_week_number(day)

    print(f"\n📅 Day {day} Workout (Week {week_number})")
    print(f"Cycle Day {day_of_cycle}")

    if day_of_cycle in [1, 3]:
        print("\n Abs & Legs Day ")
        generate_group_workout(["Abs", "Legs"], week_number)

    elif day_of_cycle in [2, 4]:
        print("\n Push + Pull Day ")
        generate_group_workout(["Push", "Pull"], week_number)

    elif day_of_cycle == 5:
        print("\n Full Body Circuit Day (3 Rounds) ")
        generate_circuit_workout(week_number)

    elif day_of_cycle == 6:
        print("\n Rest Day ")
        print("Hydrate & Be Great!")

    elif day_of_cycle == 7:
        print("\nCycle Restart - Back to Day 1 format")
        generate_group_workout(["Abs", "Legs"], week_number)


# main menu


import time 

def increment_day(progress):
    print("\nSaving progress", end="")
    for i in range(3, 0, -1):
        print(f"...{i}", end="", flush=True)
        time.sleep(0.5)
    print(" ✅\n")

    if progress['current_day'] >= 30:
    
        print(" CONGRATS! ")
        print("""
            \\  __  //  /  _  \  \\  __  //
              \\//\\//  |  | |  |  \\//\\//
             \/  \/    \  _  /    \/  \/
        """)
        print("30 Days Completed... But the JOB'S NOT DONE! \n")
        print("Restarting the program at Day 1. Let's go! ")

        progress['current_day'] = 1
    else:
        progress['current_day'] += 1
        print(f" Tomorrow will be Day {progress['current_day']}. Keep showing up!\n")

    save_progress(progress)


def show_main_menu():
    print("\n==== 30-Day Bodyweight Workout Dashboard ====")
    print(f" Current Day: {progress['current_day']} / 30")
    print("1. View Exercises by Muscle Group")
    print("2. Generate Today's Workout")
    print("3. Reset Progress")
    print("4. Exit")
    return input("Choose an option (1-4): ")

def list_muscle_groups():
    print("\nSelect a muscle group:")
    for idx, group in enumerate(muscle_groups.keys(), 1):
        print(f"{idx}. {group}")
    choice = input("Choose a group number: ")
    try:
        idx = int(choice)
        if 1 <= idx <= len(muscle_groups):
            selected_group = list(muscle_groups.keys())[idx - 1]
            show_exercises(selected_group)
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input.")

def show_exercises(group):
    print(f"\n--- {group} Exercises ---")
    exercises = muscle_groups[group]
    for ex in exercises:
        print(f"\n✅ {ex['name']}")
        if 'alternatives' in ex:
            print(f"   Alternatives: {', '.join(ex['alternatives'])}")
        print("   Progression Plan:")
        for week, prog in enumerate(ex['progression'], start=1):
            print(f"/n     Week {week}: {prog}")

# -----------------------------
# MAIN PROGRAM LOOP
# -----------------------------

def main():
    while True:
        user_choice = show_main_menu()

        if user_choice == "1":
            list_muscle_groups()

        elif user_choice == "2":
            day = progress['current_day']
            generate_workout_by_day(day)

            complete = input("\n✅ Did you complete today's workout? (y/n): ").lower()
            if complete == "y":
                increment_day(progress)
                print(f"\n Progress saved! Tomorrow is Day {progress['current_day']}.")
            else:
                print("\nLock In!.")

        elif user_choice == "3":
            confirm = input("Are you sure you want to reset progress? (y/n): ").lower()
            if confirm == "y":
                reset_progress()

        elif user_choice == "4":
            print("\nExiting dashboard. Stay consistent!")
            break

        else:
            print("Invalid choice. Try again!")

# -----------------------------
# RUN THE PROGRAM
# -----------------------------

if __name__ == "__main__":
    progress = load_progress()
    main()
