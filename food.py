import helper_functions as hf
from typing import Dict

#food class to store food information, the date it was eaten, its household measurements(stored as per), its nutrients and the id of the food from the api
class food:
    def ___init___(self, fdcId, date, per, nutrients):
        self.fdcId = fdcId
        self.date = date
        self.per = per
        self.nutrients = nutrients
    
    #prints the food information
    def print(self):
        print("Food: "+self.name)
        print("Date: "+self.date)
        print("Per: "+self.per)
        print("Nutrients: "+self.data)

    #converts the food to a json object
    def to_json(self):
        return {"fdcId": self.fdcId, "date": self.date, "per": self.per, "data": self.data}
    
    #converts the food to a dictionary
    def to_dict(self):
        return {"fdcId": self.fdcId, "date": self.date, "per": self.per, "data": self.data}