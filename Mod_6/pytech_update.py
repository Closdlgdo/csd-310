import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["pytech"]
mycol = mydb["students"]

myquery = { Name : "Charles" }
newvalues = { "$set": { Name : "Carlos" } }

mycol.update_one(myquery, newvalues)

#print "students" after the update:
for x in mycol.find():
  print(x)
