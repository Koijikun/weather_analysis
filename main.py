import helper_functions as hf
import exercises as ex
import exercise_menu as exm
import food_db as fdb
import food_pandas as fp
from mongo_db import db
import api_handler as api
#initialize classes and variables
api = api.api_handler()
col = db["exercises"]
fdb = fdb.food_db()
fp = fp.food_pandas()
menu_input = -1

#main loop
while menu_input != 0:
    #What are we doing today?\n[1] Training\n[2] Change Exercise\n[3] Food Tracker\n[0] Quit
    exm.display_menu()
    menu_input = hf.get_user_input("Please Enter 1, 2, or 3\n>")

    if menu_input == 1:
        #What would you like to train today?\n[1] Core\n[2] Arms\n[3] Chest\n[4] Legs
        exm.train_exercises(col)
    elif menu_input == 2:
        #"What would you like to do?\n[1] Add Exercise\n[2] Delete Exercise\n[3] Change Exercise\n[4] Display all"
        exm.display_change_exercise_options()
        user_input = hf.get_user_input("Please Enter 1, 2, or 3\n>")
        if user_input == 1:
            user_input = hf.get_user_input("Please enter\n[1] for repetition based exercise or\n[2] for duration based exercise\n>")
            if user_input == 1:
                exm.add_repetition_based_exercise(col)
            elif user_input == 2:
                exm.add_duration_based_exercise(col)
            else:
                print("Oops, something went wrong")
        elif user_input == 2:
            exm.edit_exercise(col)
        elif user_input == 3:
            exm.delete_exercise(col)
        elif user_input == 4:
            exm.display_all_exercises(col)
        else:
            print("Please only enter 1, 2, or 3")
    elif menu_input == 3:
        user_input = hf.get_user_input("Please enter\n[1] to add food\n[2] to analyze your nutrition\n>")
        if user_input == 1:
            foodSearch = hf.get_string_input("Please enter the food you would like to add\n>")
            print("Searching for "+foodSearch)
            foods = api.summary_search(foodSearch, 3)
            #print a list of foods by its attributes, only print attribute if value is not empty and attribute is not fdcId
            for i in range(len(foods)):
                for key, value in foods[i].items():
                    if value != "" and key != "fdcId":
                        print("["+str(i + 1)+"] " + key+": "+value)
                print("")
            user_input = hf.get_user_input("Please enter the number of the food you would like to add\n>")
            #print the food datails
            print("You selected: ["+str(user_input)+"]" + " " + foods[user_input - 1]["description"])
            print("Adding "+foods[user_input - 1]["description"]+" to the database...")
            #add the food to the database
            stored = fdb.add_food(api.get_storeable_food_data(foods[user_input - 1]["fdcId"]))
            if stored != False:
                print("Added "+foods[user_input - 1]["description"]+" to the database")
            else:
                print("Error adding "+foods[user_input - 1]["description"]+" to the database")
        elif user_input == 2:
            user_input = hf.get_user_input("Choose a datespan to analyze your nutrition\n[1] Today\n[2] Last 7 days\n[3] Last 30 days\n[4] Last 365 days\n[5] All time\n>")
            if user_input == 1:
                foods = fdb.get_foods_by_date_range(hf.get_today(), hf.get_today())
                fp.plot_chart_by_nutrients(foods)
            elif user_input == 2:
                foods = fdb.get_last_7_days()
                fp.plot_chart_by_nutrients(foods)
            elif user_input == 3:
                foods = fdb.get_last_30_days()
                fp.plot_chart_by_nutrients(foods)
            elif user_input == 4:
                foods = fdb.get_last_365_days()
                fp.plot_chart_by_nutrients(foods)
            elif user_input == 5:
                foods = fdb.get_all_foods()
                fp.plot_chart_by_nutrients(foods)
    elif menu_input != 0:
        print("Not a valid input")
print("Thank you for using Workout Tracker see you again soon!")





