import os,json
with open("data/json/files/all_ahadeeth.json","r",encoding="utf-8") as file:
    ahadeeths=json.load(file)
def getahadeethByIndex(index:str):
    rahadeeths={}
    for key,value in ahadeeths.items():
        rahadeeths[value]=key
    return rahadeeths[index]
def setahadeeth():
    values=ahadeeths.copy().values()
    for value in values:
        if not os.path.exists("data/json/ahadeeth/{}".format(value)):
            del ahadeeths[getahadeethByIndex(value)]
setahadeeth()