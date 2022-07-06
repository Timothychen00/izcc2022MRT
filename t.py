import random

number=3
data={
'name':1,
'password':1,
'number':number,
'pin':[],
'adminpin':[]
}
pins=[]
for i in range(1,number+1):
    for j in range(2):
        temp=''.join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',6))
        while temp in pins:
            temp=''.join(random.sample('zyxwvutsrqponmlkjihgfedcbaABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789',6))
        pins.append(temp)
    print(i-1,i*2-2,i*2-1)

    data['pin'].append(pins[i*2-2])
    data['adminpin'].append(pins[i*2-1])
print(pins)