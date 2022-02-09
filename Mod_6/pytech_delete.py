import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["pytech"]
mycol = mydb["students"]

myquery = { _id : "1010" }

mycol.delete_one(myquery)
