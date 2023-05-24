from mongo_db import db
col = db["foods"]

class food_db:

    def add_food(self,food):
        col.insert_one(food)

    def get_foods_by_field(self,field):
        return col.find({field: {"$exists": True}})
    
    def get_foods_by_field_value(self,field, value):
        return col.find({field: value})
    
    def get_foods_by_date_range(self, start, end):
        return col.find({"date": {"$gte": start, "$lte": end}})
    
fdb = food_db()
print(list(fdb.get_food_nutrients("kcal")))
