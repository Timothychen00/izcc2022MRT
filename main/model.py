import os
import pymongo
from dotenv import load_dotenv
load_dotenv()
class DB():
    def __init__(self):
        self.client=pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@cluster0.z3vye.mongodb.net/?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
        self.db=self.client.izcc
        self.collection=self.db.team
    
    def load_data(self):
        result=self.collection.find()
        data=[]
        for i in result:
            data.append([i['name'],i['color'],i['counts'],i['places']])
        return data
    
    
db_model=DB()