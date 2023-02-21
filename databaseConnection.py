import pymongo


def databaseConnection(collection):
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["Proiect_preFinal"]
    angajat = db[collection]
    return angajat
