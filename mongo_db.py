from pymongo import MongoClient

client = MongoClient("mongodb+srv://sp:N47wPDX4AZb0GYla@scientificp.xozqbzt.mongodb.net/")
db = client["workout"]