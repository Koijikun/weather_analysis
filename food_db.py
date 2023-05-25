from mongo_db import db
import helper_functions as hf
import json
col = db["foods"]

class food_db:

    def add_food(self,food):
        col.insert_one(food)

    def get_food_by_id(self,fdcId):
        return col.find_one({"fdcId": fdcId})

    def get_food_by_field(self,field):
        return col.find({field: {"$exists": True}})
    
    def get_food_by_field_value(self,field, value):
        return col.find({field: value})
    
    def get_foods_by_date_range(self, start, end):
        return col.find({"date": {"$gte": start, "$lte": end}})

    def get_last_7_days(self):
        today = hf.get_today()
        return self.get_foods_by_date_range(int(today)-7, int(today))
    
    def get_last_30_days(self):
        today = hf.get_today()
        return self.get_foods_by_date_range(int(today)-30, int(today))
    
    def get_last_365_days(self):
        today = hf.get_today()
        return self.get_foods_by_date_range(int(today)-365, int(today))
    
    def get_by_year(self, year):
        return self.get_foods_by_date_range(int(year)*10000, int(year)*10000+1231)
    
    
    def get_by_month(self, year, month):
        #handle months with 30 days and february
        if month == 2:
            if year % 4 == 0:
                return self.get_foods_by_date_range(int(year)*10000+int(month)*100, int(year)*10000+int(month)*100+29)
            else:
                return self.get_foods_by_date_range(int(year)*10000+int(month)*100, int(year)*10000+int(month)*100+28)
        elif month in [4, 6, 9, 11]:
            return self.get_foods_by_date_range(int(year)*10000+int(month)*100, int(year)*10000+int(month)*100+30)
        return self.get_foods_by_date_range(int(year)*10000+int(month)*100, int(year)*10000+int(month)*100+31)
    
    def get_all_foods(self):
        return col.find()