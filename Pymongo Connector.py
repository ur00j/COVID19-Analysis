import pymongo

def connect():
    mgconnection = pymongo.MongoClient("mongodb+srv://{login}:{password}@covid.{ID}.mongodb.net/?retryWrites=true&w=majority")
    return mgconnection

def disconnect(mgconnection):
    mgconnection.close()
