import os,settings
import json
translations={}
def gettranslationByIndex(index:str):
    rtranslations={}
    for key,value in translations.items():
        rtranslations[value]=key
    return rtranslations[index]
def gettranslation(translationName:str,From:int,to:int):
    with open(os.path.join(os.getenv('appdata'),settings.app.appName,"translations",translations[translationName]),"r",encoding="utf-8") as file:
        data=json.load(file)
    result=[]
    for ayah in data:
        index=data.index(ayah)+1
        if index>=From and index<=to:
            result.append(ayah)
    return "\n".join(result)
def settranslation():
    global translations
    with open("data/json/files/all_translater.json","r",encoding="utf-8") as file:
        translations=json.load(file)
    values=translations.copy().values()
    for value in values:
        if not os.path.exists(os.path.join(os.getenv('appdata'),settings.app.appName,"translations",value)):
            del translations[gettranslationByIndex(value)]
settranslation()