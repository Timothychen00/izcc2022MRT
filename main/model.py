import os,pymongo,random
from dotenv import load_dotenv
load_dotenv()
class DB():
    def __init__(self):
        self.client=pymongo.MongoClient("mongodb+srv://"+os.environ['DB_USER']+":"+os.environ['DB_PASSWORD']+"@cluster0.z3vye.mongodb.net/?retryWrites=true&w=majority",tls=True,tlsAllowInvalidCertificates=True)
        self.db=self.client.izcc
        self.team=self.db.team
        self.games=self.db.games
    
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
                    temp=''.join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',6))
                    while temp in pins:
                        temp=''.join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',6))
                    pins.append(temp)
                data['pin'].append(pins[i*2-2])
                data['adminpin'].append(pins[i*2-1])
                msg+="隊員："+pins[i*2-2]+'     隊隨：'+pins[i*2-1]+'\\n'
                data['team'].append({"color":colors[i%6],"counts":3,"places":'','now':''})
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
                if pin in result['adminpin']:
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
        result=self.games.find_one({'name':name})
        teams=result['team'][team]['now']=target
        self.games.update_one({'name':name},{"$set":{'team':teams}})

db_model=DB()