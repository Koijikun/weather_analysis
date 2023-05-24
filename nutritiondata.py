import datetime

class nutritiondata():

    date = datetime.date.today()

    def __init__(self, calories, fibres, protein, fat, date):
        self.calories=calories
        self.fibres=fibres
        self.protein=protein
        self.fat=fat