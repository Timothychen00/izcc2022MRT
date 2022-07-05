import os,pymongo
from dotenv import load_dotenv
load_dotenv()
class DB():
    def __init__(self):
        self.client=pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@cluster0.z3vye.mongodb.net/?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
        self.db=self.client.izcc
        self.team=self.db.team
        self.games=self.db.games
    
    def load_data(self):
        result=self.team.find()
        data=[]
        for i in result:
            data.append([i['name'],i['color'],i['counts'],i['places']])
        return data

    def create_game(self,name,password):
        result=self.games.find_one({'name':name})
        err=[]
        if result:
            err.append('遊戲名稱已經存在')
        if not err:
            data={
                'name':name,
                'password':password
            }
            self.games.insert_one(data)
        return err
    
    def find_game(self,name=None):
        if name:
            filters={'name':name}
        else:
            filters={}
            
        return self.games.find(filters)
    
    def delete_games(self,name=None):
        pass

db_model=DB()