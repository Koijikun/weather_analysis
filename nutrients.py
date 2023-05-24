import json
import requests


def getDataByQuery(query, returnType = "python"):
    response = requests.get(query)
    jsonFormat = json.dumps(response.json())
    if returnType == "python":
        return json.loads(jsonFormat)
    return jsonFormat


def generateQuery(type, query = [["query", "Cheddar Cheese"], ["pageSize", 10], ["pageNumber", 1]]):
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

def searchQuery(search, pageSize = 10, pageNumber = 1):
    return generateQuery("search", query = [["query", search], ["pageSize", pageSize], ["pageNumber", pageNumber]])

def summarySearch(search, pageSize = 10, pageNumber = 1):
    query = generateQuery("search", query = [["query", search], ["pageSize", pageSize], ["pageNumber", pageNumber]])
    data = getDataByQuery(query)
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

def getFoodById(fdcId):
    query = generateQuery("food", query = fdcId)
    return getDataByQuery(query)

def prettyPrint(variable):
    return print(json.dumps(variable, indent=4, sort_keys=True))

prettyPrint(getFoodById(summarySearch("Meat", pageSize = 10)[0]["fdcId"]))
#prettyPrint(getFoodById())