import json
import requests
import datetime
from typing import Dict

class api_handler():
    def get_data_by_query(self, query, returnType = "python"):
        response = requests.get(query)
        jsonFormat = json.dumps(response.json())
        if returnType == "python":
            return json.loads(jsonFormat)
        return jsonFormat

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
        print(queryString)
        return baseURL + queryString

    def search_query(self, search, pageSize = 10, pageNumber = 1):
        return self.generate_query("search", query = [["query", search], ["pageSize", pageSize], ["pageNumber", pageNumber]])

    def summary_search(self,search, pageSize = 10, pageNumber = 1):
        query = self.generate_query("search", query = [["query", search], ["pageSize", pageSize], ["pageNumber", pageNumber]])
        data = self.get_data_by_query(query)
        titles = [
            "fdcId",
            "description",
            "commonNames",
            "additionalDescriptions",
            "foodCategory"
        ]
        foods = {}
        for i in range(len(data["foods"])):
            foods[i] = {}
            for j in range(len(titles)):
                if titles[j] in data["foods"][i]:
                    foods[i][titles[j]] = data["foods"][i][titles[j]]
        return foods

    def get_food_by_id(self,fdcId):
        query = self.generate_query("food", query = fdcId)
        return self.get_data_by_query(query)
    
    def get_storeable_food_data(self, fdcId):
        foodItem = self.get_food_by_id(fdcId)
        dateString = json.dumps({'date': datetime.date.today()}, default=str)
        dateDict = json.loads(dateString)
        structure: Dict[str, any] = {
            "fdcId": fdcId,
            "date": f'{dateDict["date"]}',
            "per" : "",
            "data": {
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
        structure["per"] = foodItem.get("householdServingFullText", "")
        for nutrient in foodItem["foodNutrients"]:
            if nutrient["nutrient"]["id"] == 1008:
                structure["data"]["kcal"]["name"] = nutrient.get("nutrient", {}).get("name", "")
                structure["data"]["kcal"]["unitName"] = nutrient.get("nutrient", {}).get("unitName", "")
                structure["data"]["kcal"]["value"] = nutrient.get("labelNutrients", {}).get("calories", {}).get("value", 0)
            elif nutrient["nutrient"]["id"] == 1004:
                structure["data"]["fat"]["name"] = nutrient.get("nutrient", {}).get("name", "")
                structure["data"]["fat"]["unitName"] = nutrient.get("nutrient", {}).get("unitName", "")
                structure["data"]["fat"]["value"] = foodItem.get("labelNutrients", {}).get("fat", {}).get("value", 0)
            elif nutrient["nutrient"]["id"] == 1003:
                structure["data"]["protein"]["name"] = nutrient.get("nutrient", {}).get("name", "")
                structure["data"]["protein"]["unitName"] = nutrient.get("nutrient", {}).get("unitName", "")
                structure["data"]["protein"]["value"] = foodItem.get("labelNutrients", {}).get("protein", {}).get("value", 0)
            elif nutrient["nutrient"]["id"] == 1079:
                structure["data"]["fiber"]["name"] = nutrient.get("nutrient", {}).get("name", "")
                structure["data"]["fiber"]["unitName"] = nutrient.get("nutrient", {}).get("unitName", "")
                structure["data"]["fiber"]["value"] = foodItem.get("labelNutrients", {}).get("fiber", {}).get("value", 0)
        return structure

    def pretty_print(self,variable):
        return print(json.dumps(variable, indent=4, sort_keys=True))