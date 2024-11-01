import os
import json
with open("data/json/files/all_tafaseers.json","r",encoding="utf-8") as file:
    tafaseers=json.load(file)
def getTafaseerByIndex(index:str):
    rtafaseers={}
    for key,value in tafaseers.items():
        rtafaseers[value]=key
    return rtafaseers[index]
def getTafaseer(tafaseerName:str,From:int,to:int):
    with open("data/json/tafaseer/{}".format(tafaseers[tafaseerName]),"r",encoding="utf-8") as file:
        data=json.load(file)
    result=[]
    for ayah in data:
        index=data.index(ayah)+1
        if index>=From and index<=to:
            result.append(ayah)
    return "\n".join(result)
def setTafaseer():
    values=tafaseers.copy().values()
    for value in values:
        if not os.path.exists("data/json/tafaseer/{}".format(value)):
            del tafaseers[getTafaseerByIndex(value)]
setTafaseer()