import http.client
import json

conn = http.client.HTTPSConnection("edamam-edamam-nutrition-analysis.p.rapidapi.com")

headers = {
    'X-RapidAPI-Key': "d357136464msha539dd78922eecfp14e9a3jsn5a0330d2be3a",
    'X-RapidAPI-Host': "edamam-edamam-nutrition-analysis.p.rapidapi.com"
}

conn.request("GET", "/api/nutrition-data?ingr=meat&nutrition-type=logging", headers=headers)

res = conn.getresponse()
data = res.read()

jsonData = json.loads(data.decode("utf-8"))
jsonPretty = json.dumps(jsonData, indent=2)

print(jsonPretty)