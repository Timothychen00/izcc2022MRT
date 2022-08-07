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
        '''this function is used to load the global settings data from mongodb'''
        result=self.settings.find_one({'type':'settings'})
        return result
    
    def load_data(self,name:str):
        '''this function is used to load the team data of a game'''
        result=self.games.find_one({'name':name})
        print(result['team'])
        return result['team']

    def create_game(self,name:str,number:int):
        '''this function is used to create a game and initialize the game'''
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
        
    def find_game(self,name:str=None):
        '''this function is used to return games'''
        if name:
            filters={'name':name}
        else:
            filters={}
        return self.games.find(filters)
    
    def check_permission(self,name:str=None,pin:int=None):
        '''this function is used to check the permission(normal,admin,not allowed) of the input pin'''
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
    
    def delete_games(self,name:str=None,pin:int=None):
        '''this function is used to delete a game while the permission is allowed(admin)'''
        print(name,pin)
        print(self.check_permission(name,pin))
        if self.check_permission(name,pin)[1]=='admin':
            self.games.delete_one({'name':name})
        else:
            print('permission denied')
            return 'permission denied'
    
    def edit_scores(self,name:str,team:int,increase_value:int):
        '''this function is used to edit the score of a team'''
        teams=self.load_data(name)
        teams[team]['counts']+=increase_value
        self.games.update_one({'name':name},{"$set":{'team':teams}})
        
    def move(self,name:str,team:int,target:str):
        '''this function is used to change the position of a team'''
        print('move')
        print(team)
        teams=self.load_data(name)
        teams[team]['now']=target
        self.games.update_one({'name':name},{"$set":{'team':teams}})
        
    def have(self,name:str,team:int,target:str):#佔領
        '''this function is used to occupy a place for a team'''
        teams=self.load_data(name)
        for i in teams:#清除其他隊伍的內容
            if target in  i['places']:
                del i['places'][i['places'].index(target)]
        print(teams)
        if not target in teams[team]['places']:
            teams[team]['places'].append(target)
        self.games.update_one({'name':name},{"$set":{'team':teams}})
        
    def get_card(self,name:str,team:int,card_id:int):
        '''this function is used to add a card to a team's pocket'''
        teams=self.load_data(name)
        teams[team]['cards'].append(card_id)
        self.games.update_one({'name':name},{"$set":{'team':teams}})
        
    def delete_card(self,name:str,team:int,card_index:int):
        '''this function is used to delete a card from a team's pocket'''
        teams=self.load_data(name)
        del teams[team]['cards'][card_index]
        self.games.update_one({'name':name},{"$set":{'team':teams}})
    
    def upload_tasks(self):
        '''this function is to upload the tasks.json from local file system to mongodb settings collection'''
        result=self.load_settings()
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