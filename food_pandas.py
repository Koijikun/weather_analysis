import food_db as fdb
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict
fdb = fdb.food_db()

class food_pandas:
    def get_nutrient_values_from_food(self, food: Dict[str, any]) -> Dict[str, float]:
        return {key: value["value"] for key, value in food["nutrients"].items()}
    
    def get_nutrient_values_from_foods(self, foods: Dict[str, any], add_date = False) -> Dict[str, float]:
        nutrients = {}
        for index, food in enumerate(foods):
            #make key unique
            key = str(index) + "_" + food["name"]
            if add_date:
                key = str(food["date"]) + "_" + str(index) + "_" + food["name"]
            nutrients[key] = self.get_nutrient_values_from_food(food)
        return nutrients
    
    def convert_food_to_dict(self, food: Dict[str, any]) -> Dict[str, any]:
        return {
            "fdcId": food["fdcId"],
            "name": food["name"],
            "date": food["date"],
            "per": food["per"],
            "nutrients": self.get_nutrient_values_from_food(food)
        }
    
    def convert_food_nutrient_values_to_df(self, foods: Dict[str, any], add_date=False) -> pd.DataFrame:
        return pd.DataFrame.from_dict(self.get_nutrient_values_from_foods(foods, add_date))
    
    def customize_plots(self, df: pd.DataFrame, **customisation):
        custom_values = {"file_name": ""}
        #for each custom key in custom_values, check if it is in customisation, if not, add it with a default value
        for key in custom_values:
            if key not in customisation:
                custom_values[key] = "default_" + key
            else:
                custom_values[key] = customisation[key]
        #remove custom keys from customisation, otherwise it will be passed to the plot function
        for key in custom_values:
            if key in customisation:
                del customisation[key]
        
        return custom_values, customisation
    
    def plot_line_chart(self, df: pd.DataFrame, **customisation):
        custom_values, customisation = self.customize_plots(df, **customisation)
        fig, axes = plt.subplots()
        fig.tight_layout(rect=[0,0,0.7,1])
        #get the mean of each column
        mean = df.mean()
        #convert the mean to a string
        mean = "Mean per day:\n" + mean.to_string()
        df.plot(kind="line",ax=axes, **customisation)
        fig.text(0.75, 0.5, str(mean))
        fig.savefig(custom_values["file_name"])
        print("a image should be saved, in the same directory as this file, called " + custom_values["file_name"])

    def plot_bar_chart(self, df: pd.DataFrame, **customisation):
        custom_values, customisation = self.customize_plots(df, **customisation)
        fig, axes = plt.subplots(nrows=1, ncols=2)
        #df only with kcal, set value label to kcal
        df_kcal = df[df["nutrient"] == "kcal"]
        df_kcal = df_kcal.rename(columns={"g": "kcal"})
        #df without kcal
        df = df[df["nutrient"] != "kcal"]
        df.plot(kind="bar",rot=0, ax=axes[0], **customisation)
        df_kcal.plot(kind="bar",rot=0, ax=axes[1], **customisation)
        fig.savefig(custom_values["file_name"])
        print("a image should be saved, in the same directory as this file, called " + custom_values["file_name"])

    def plot_chart_by_nutrients(self, foods: Dict[str, any], **customisation):
        df = self.convert_food_nutrient_values_to_df(foods, add_date=True)
        print(df)
        #overwrite columns by extracting the date from its values as date time
        df.columns = pd.to_datetime(df.columns.str.split("_").str[0])
        #if there are multiple foods with the same date, sum them
        df = df.groupby(df.columns, axis=1).sum()
        
        #if there is only one date, plot a bar chart
        if len(df.columns) == 1:
            #create suitable dataframe for bar chart
            df = df.transpose()
            indexes = df.columns.to_list()
            values = df.values.tolist()[0]
            
            df = pd.DataFrame({"nutrient" : indexes, 'g' : values}, index=indexes)
            print(df)
            self.plot_bar_chart(df, **customisation)
            return
        
        #fill in missing dates with 0, show all dates
        df = df.reindex(pd.date_range(df.columns.min(), df.columns.max(), freq='D'), axis=1).fillna(0)
        #transpose the dataframe
        df = df.transpose()
        self.plot_line_chart(df, **customisation)
    