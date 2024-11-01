import os
import json
def gettanzil(From:int):
    with open("data/json/tanzil.json","r",encoding="utf-8") as file:
        data=json.load(file)
    result=""
    for ayah in data:
        index=data.index(ayah)+1
        if index==From:
            result=ayah
            break
    return result
