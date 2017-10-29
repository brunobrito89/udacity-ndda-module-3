from pymongo import MongoClient
import pprint

# Auxiliary module used to perform sql queries on MongoDB to answer the questions of the final report.

client = MongoClient("mongodb://localhost:27017")
db = client.openstreetmap


# result = db.campinas.aggregate([
#     {"$match":{"amenity":{"$exists":1}}},
#     {"$group":{"_id":"$amenity", "count":{"$sum":1}}},
#     {"$sort": {"count": -1}},
#     {"$limit": 10}
# ])
# pprint.pprint(list(result))

result = db.campinas.aggregate([
    {"$match": {"amenity": {"$exists": 1}, "amenity": "place_of_worship"}},
    {"$group": {"_id": "$religion", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}},
    #{"$limit": 1}
])
pprint.pprint(list(result))

# result = db.campinas.aggregate([
    # {"$match": {"amenity": {"$exists": 1}, "amenity": "school"}}
    # {"$limit": 1}
# ])
#pprint.pprint(list(result))

# print db.campinas.distinct("created.user").length()

