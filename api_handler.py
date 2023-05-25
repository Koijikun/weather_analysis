import json
import requests
import helper_functions as hf
from typing import Dict

class api_handler():
    #get the data of food items by the generated query
    def get_data_by_query(self, query, returnType = "python"):
        response = requests.get(query)
        jsonFormat = json.dumps(response.json())
        if returnType == "python":
            return json.loads(jsonFormat)
        return jsonFormat

    #generate a query to get data about food items
    def generate_query(self, type, query = [["query", "Cheddar Cheese"], ["pageSize", 10], ["pageNumber", 1]]):
        baseURL = "https://api.nal.usda.gov/fdc/v1/"
        queryString = ""
        apiKey = "D3OJjtrugLUL5Q7wzGadlQnF2FOjSFcW1ol3IKsu"
        if type == "search":
            baseURL += "foods/search"
        elif type == "food":
            return baseURL + "food/"+ f'{query}' + "?api_key=" + apiKey
        else:
            print("Invalid type")
            return
        baseURL += "?api_key=" + apiKey
        for i in range(len(query)):
            queryString += "&" + query[i][0] + "=" + str(query[i][1])
        return baseURL + queryString

    #generate a query to search for a food item
    def search_query(self, search, pageSize = 10, pageNumber = 1):
        return self.generate_query("search", query = [["query", search], ["pageSize", pageSize], ["pageNumber", pageNumber]])

    #simplify the search results to only the data that we need
    def summary_search(self,search, pageSize = 10, pageNumber = 1):
        query = self.generate_query("search", query = [["query", search], ["pageSize", pageSize], ["pageNumber", pageNumber]])
        data = self.get_data_by_query(query)
        #only return the data that we need
        titles = [
            "fdcId",
            "description",
            "commonNames",
            "additionalDescriptions",
            "foodCategory"
        ]
        foods = []
        for i in range(len(data["foods"])):
            foods.append({})
            for j in range(len(titles)):
                if titles[j] in data["foods"][i]:
                    foods[i][titles[j]] = data["foods"][i][titles[j]]
            #if foods doesn't contain all the titles, add them with a value of ""
            for j in range(len(titles)):
                if titles[j] not in foods[i]:
                    foods[i][titles[j]] = ""  
        return foods

    #get a food item by its fdcId
    def get_food_by_id(self,fdcId):
        query = self.generate_query("food", query = fdcId)
        return self.get_data_by_query(query)
    
    #get only the data that we need from a food item
    def get_storeable_food_data(self, fdcId):
        foodItem = self.get_food_by_id(fdcId)
        #use the following structure to store the food item in the database
        structure: Dict[str, any] = {
            "fdcId": fdcId,
            "name": foodItem.get("description", ""),
            "date": hf.get_today(),
            "per" : "",
            "nutrients": {
                "kcal": {
                    "id": 1008,
                    "name": "",
                    "unitName": "",
                    "value": 0
                },
                "fat": {
                    "id": 1004,
                    "name": "",
                    "unitName": "",
                    "value": 0
                },
                "protein": {
                    "id": 1003,
                    "name": "",
                    "unitName": "",
                    "value": 0
                },
                "fiber": {
                    "id": 1079,
                    "name": "",
                    "unitName": "",
                    "value": 0
                }
            }
        }
        #if the food item has a serving size, use that, otherwise use the household serving size
        #if the food item has neither, use "100g"
        if len(str(foodItem.get("servingSize", ""))) >= 0: 
            structure["per"] = str(foodItem.get("servingSize", "")) +""+ foodItem.get("servingSizeUnit", "")
        else:
            structure["per"] = foodItem.get("householdServingFullText", "")
        structure["per"] = ("100g", structure["per"])[len(structure["per"]) == 0]
        
        #if "foodNutrients" is not in the food item, return False
        if "foodNutrients" not in foodItem:
            return False
        
        #add the nutrients to the structure
        for nutrient in foodItem["foodNutrients"]:
            if nutrient["nutrient"]["id"] == 1008:
                self.add_nutrient(structure, foodItem, nutrient, "kcal", labelNutrient = "calories")
            elif nutrient["nutrient"]["id"] == 1004:
                self.add_nutrient(structure, foodItem, nutrient, "fat")
            elif nutrient["nutrient"]["id"] == 1003:
                self.add_nutrient(structure, foodItem, nutrient, "protein")
            elif nutrient["nutrient"]["id"] == 1079:
                self.add_nutrient(structure, foodItem, nutrient, "fiber")
        return structure
    
    #add a nutrient to the structure of a storeable food item
    def add_nutrient(self, structure, foodItem, nutrient, nutrient_name, labelNutrient = ""):
        #labelNutrient is used, when the nutrient is not in the labelNutrients list
        if labelNutrient == "":
            labelNutrient = nutrient_name
        #set a baseunit for the nutrient
        baseunit = ("kcal", "g")[labelNutrient == "calories"]
        structure["nutrients"][nutrient_name]["name"] = nutrient.get("nutrient", {}).get("name", "")
        structure["nutrients"][nutrient_name]["unitName"] = nutrient.get("nutrient", {}).get("unitName", baseunit)
        #if no amount is given, use the value from labelNutrients
        if nutrient.get("amount", 0) != 0:
            structure["nutrients"][nutrient_name]["value"] = nutrient.get("amount", 0)
        else:
            structure["nutrients"][nutrient_name]["value"] = foodItem.get("labelNutrients", {}).get(labelNutrient, {}).get("value", 0)
