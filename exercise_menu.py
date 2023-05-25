import exercises as ex
import helper_functions as hf

def display_menu():
    print("\n----------------------\nWorkout Tracker\n----------------------")
    print("What are we doing today?\n[1] Training\n[2] Change Exercise\n[3] Food Tracker\n[0] Quit")

def display_training_options():
    print("What would you like to train today?\n[1] Core\n[2] Arms\n[3] Chest\n[4] Legs")

def display_change_exercise_options():
    print("What would you like to do?\n[1] Add Exercise\n[2] Edit Exercise\n[3] Change Exercise\n[4] Display all")

def display_all_exercises(col):
    all_exercises = col.find()
    for ex in all_exercises:
        print(ex)

def add_repetition_based_exercise(col):
    new_ex_name = hf.get_string_input("Exercise name: ")
    new_ex_bodypart = hf.get_string_input("What Bodypart are you training: ")
    new_ex_rep = hf.get_string_input("How many reps for this exercise: ")
    new_ex_weight = hf.get_string_input("What weight for this exercise: ")
    new_ex = ex.rep_ex(new_ex_name, new_ex_bodypart, new_ex_weight, new_ex_rep)
    col.insert_one(new_ex.to_json())

def add_duration_based_exercise(col):
    new_ex_name = hf.get_string_input("Exercise name: ")
    new_ex_bodypart = hf.get_string_input("What Bodypart are you training: ")
    new_ex_dur = hf.get_string_input("How many seconds for this exercise: ")
    new_ex = ex.dur_ex(new_ex_name, new_ex_bodypart, new_ex_dur)
    col.insert_one(new_ex.to_json())

def delete_exercise(col):
    ex_name = hf.get_string_input("Enter the name of the exercise you want to delete: ")
    col.delete_one({"name": ex_name})
    print("Exercise deleted successfully!")

def edit_exercise(col):
    ex_name = hf.get_string_input("Enter the name of the exercise you want to change: ")
    ex_edit = hf.get_string_input("What would you like to change? (Enter name, bodypart, weight, dur_goal, rep_goal): ")
    new_edit = hf.get_string_input("Please enter your updated data: ")
    selection_dic = {"name": "name", "bodypart": "bodypart", "weight": "weight", "dur_goal": "dur_goal", "rep_goal": "rep_goal"}
    col.update_one({"name": ex_name}, {"$set": {selection_dic[ex_edit]: new_edit}})

def train_exercises(col):
    print("Which body part would you like to train?\n[1] Core\n[2] Arms\n[3] Chest\n[4] Legs\n[0] Go back")
    bodypart_input = hf.get_user_input("Please enter 1, 2, 3, 4, or 0: ")
    if bodypart_input == 1:
        exercises = list(col.find({"bodypart": "Core"}))
    elif bodypart_input == 2:
        exercises = list(col.find({"bodypart": "Arms"}))
    elif bodypart_input == 3:
        exercises = list(col.find({"bodypart": "Chest"}))
    elif bodypart_input == 4:
        exercises = list(col.find({"bodypart": "Legs"}))
    elif bodypart_input == 0:
        return
    else:
        print("Invalid input. Please enter a number between 0 and 4.")
        return
    
    ex_count_input = hf.get_user_input("How many exercises do you want in your workout?\n>")
    if ex_count_input > len(exercises):
        print(f"Sorry, there are only {len(exercises)} exercises for {exercises[0]['bodypart']}.")
    print(f"\nHere are {len(exercises)} exercises you can do for {exercises[0]['bodypart']}:\n")
    ex_count = 0
    for exercise in exercises:
        if ex_count == ex_count_input:
            break
        if 'weight' in exercise:
            print(f"{exercise['name']} - {exercise['weight']} kg x {exercise['rep_goal']} reps\n----------------------")
        elif 'dur_goal' in exercise:
            print(f"{exercise['name']} - {exercise['dur_goal']} seconds")
        ex_count += 1
