import os,pymongo,random,sys,json
from dotenv import load_dotenv
load_dotenv()
class DB():
    def __init__(self):
        self.client=pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@cluster0.z3vye.mongodb.net/?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
        self.db=self.client.izcc
        self.settings=self.db.settings
        self.games=self.db.games
    
    def load_settings(self):
        result=self.settings.find_one({'type':'settings'})
        return result
    
    def load_data(self,name):
        result=self.games.find_one({'name':name})
        print(result['team'])
        return result['team']

    def create_game(self,name,number):
        colors=['#e6785a','#5ae6bc','#d8e65a','#5a8de6','#5a68e6','#5ae6c3']
        result=self.games.find_one({'name':name})
        pins=[]
        msg=''
        if not result:

            data={
                'name':name,
                'number':number,
                'pin':[],
                'adminpin':[],
                'team':[]
            }
            for i in range(1,number+1):
                msg+='第'+str(i-1)+'小隊:\\n'
                for j in range(2):
                    temp=''.join(random.sample('0123456789',6))
                    while temp in pins:
                        temp=''.join(random.sample('Z0123456789',6))
                    pins.append(temp)
                data['pin'].append(pins[i*2-2])
                data['adminpin'].append(pins[i*2-1])
                msg+="隊員："+pins[i*2-2]+'     隊隨：'+pins[i*2-1]+'\\n'
                data['team'].append({"color":colors[i%6],"counts":3,"places":[],'now':'','cards':[]})
            self.games.insert_one(data)
            print(msg)
            return msg
        else:
            print('name existed')
        
    def find_game(self,name=None):
        if name:
            filters={'name':name}
        else:
            filters={}
        return self.games.find(filters)
    
    def check_permission(self,name=None,pin=None):
        if name and pin:
            print(pin)
            result=self.games.find_one({'name':name})
            if result:
                if pin=='qqqq':
                    return (0,'admin')
                elif pin in result['adminpin']:
                    return (result['adminpin'].index(pin),'admin')
                elif pin in result['pin']:
                    return (result['pin'].index(pin),'normal')
        return (None,'not allowed')
    
    def delete_games(self,name=None,pin=None):
        print(name,pin)
        print(self.check_permission(name,pin))
        if self.check_permission(name,pin)[1]=='admin':
            self.games.delete_one({'name':name})
        else:
            print('permission denied')
            return 'permission denied'
    
    def edit_scores(self,name,team,increase_value):
        print(team,type(team))
        result=self.games.find_one({'name':name})
        teams=result['team']
        teams[team]['counts']+=increase_value
        self.games.update_one({'name':name},{"$set":{'team':teams}})
        
    def move(self,name,team,target):
        print('move')
        print(team)
        result=self.games.find_one({'name':name})
        teams=result['team']
        teams[team]['now']=target
        self.games.update_one({'name':name},{"$set":{'team':teams}})
        
    def have(self,name,team,target):
        result=self.games.find_one({'name':name})
        teams=result['team']
        if not target in teams[team]['places']:
            teams[team]['places'].append(target)
        self.games.update_one({'name':name},{"$set":{'team':teams}})
        
    def get_card(self,name:str,team:int,card_id:int):
        result=self.games.find_one({'name':name})
        teams=result['team']
        teams[team]['cards'].append(card_id)
        self.games.update_one({'name':name},{"$set":{'team':teams}})
        
    def delete_card(self,name:str,team:int,card_index:int):
        result=self.games.find_one({'name':name})
        teams=result['team']
        del teams[team]['cards'][card_index]
        self.games.update_one({'name':name},{"$set":{'team':teams}})
    
    def upload_tasks(self):
        result=self.settings.find_one({'type':'settings'})
        if result:
            with open('tasks.json',"r") as f1:
                data=json.load(f1)
            result.update(data)
            print(result)
            self.settings.update_one({'type':'settings'},{"$set":result})
        else:
            result={"type":'settings'}
            with open('tasks.json',"r") as f1:
                data=json.load(f1)
            result.update(data)
            print(result)
            self.settings.insert_one(result)
            

db_model=DB()