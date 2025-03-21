from . import quranJsonControl
import json ,os,gui
from settings import app
bookMarksPath=os.path.join(os.getenv('appdata'),app.appName,"bookMarks.json")
if not os.path.exists(bookMarksPath):
    with open(bookMarksPath,"w",encoding="utf-8") as file:
        json.dump({"quran":[],"ahadeeth":[],"islamicBooks":[]},file,ensure_ascii=False,indent=4)
def openBookMarksFile():
    try:
        with open(bookMarksPath,"r",encoding="utf-8") as file:
            return json.load(file)
    except:
        return {"quran":[],"ahadeeth":[],"islamicBooks":[],"stories":[]}
def saveBookMarks(bookMarksList:dict):
    with open(bookMarksPath,"w",encoding="utf-8") as file:
        json.dump(bookMarksList,file,ensure_ascii=False,indent=4)
def addNewHadeethBookMark(bookName:str,hadeethNumber:int,bookMarkName:str):
    bookMarksList=openBookMarksFile()
    ahadeethBookMarksList=bookMarksList["ahadeeth"]
    newBookMarkData={
        "bookName":bookName,
        "number":hadeethNumber,
        "name":bookMarkName
    }
    ahadeethBookMarksList.append(newBookMarkData)
    bookMarksList["ahadeeth"]=ahadeethBookMarksList
    saveBookMarks(bookMarksList)
def removeAhadeethBookMark(bookMarkName:str):
    bookMarksList=openBookMarksFile()
    ahadeethBookMarksList=bookMarksList["ahadeeth"]
    for hadeethBookMarkData in ahadeethBookMarksList:
        if hadeethBookMarkData["name"]==bookMarkName:
            ahadeethBookMarksList.remove(hadeethBookMarkData)
            break
    bookMarksList["ahadeeth"]=ahadeethBookMarksList
    saveBookMarks(bookMarksList)
def GetHadeethBookByName(name:str):
    ahadeethBookMarks=openBookMarksFile()
    for hadeethData in ahadeethBookMarks["ahadeeth"]:
        if hadeethData["name"]==name:
            return hadeethData["bookName"],hadeethData["number"]
def addNewQuranBookMark(typeIndex:int,categoryIndex,ayahIndex:int,isPlayer:bool,bookMarkName:str):
    bookMarksList=openBookMarksFile()
    quranBookMarksList=bookMarksList["quran"]
    newQuranBookMarkData={
        "type":typeIndex,
        "category":categoryIndex,
        "ayah":ayahIndex,
        "isPlayer":isPlayer,
        "name":bookMarkName
    }
    quranBookMarksList.append(newQuranBookMarkData)
    bookMarksList["quran"]=quranBookMarksList
    saveBookMarks(bookMarksList)
def removeQuranBookMark(bookMarkName:str):
    bookMarksList=openBookMarksFile()
    ahadeethBookMarksList=bookMarksList["quran"]
    for hadeethBookMarkData in ahadeethBookMarksList:
        if hadeethBookMarkData["name"]==bookMarkName:
            ahadeethBookMarksList.remove(hadeethBookMarkData)
            break
    bookMarksList["quran"]=ahadeethBookMarksList
    saveBookMarks(bookMarksList)
def openQuranByBookMarkName(p,bookMarkName:str):
    quranBookMarksList=openBookMarksFile()["quran"]
    for bookMark in quranBookMarksList:
        if bookMark["name"]==bookMarkName:
            data=bookMark
            break
    result=""
    if data["type"]==0:
        result=quranJsonControl.getSurahs()
    elif data["type"]==1:
        result=quranJsonControl.getPage()
    elif data["type"]==2:
        result=quranJsonControl.getJuz()
    elif data["type"]==3:
        result=quranJsonControl.getHezb()
    elif data["type"]==4:
        result=quranJsonControl.getHizb()
    if data["isPlayer"]:
        gui.QuranPlayer(p,result[data["category"]][1],data["ayah"],data["type"],data["category"]).exec()
    else:
        gui.QuranViewer(p,result[data["category"]][1],data["type"],data["category"],index=data["ayah"]+1).exec()
def addNewislamicBookBookMark(bookName:str,partName:str,pageNumber:int,bookMarkName:str):
    bookMarksList=openBookMarksFile()
    try:
        islamicBookBookMarksList=bookMarksList["islamicBooks"]
    except:
        islamicBookBookMarksList=bookMarksList["islamicBooks"]=[]
    newBookMarkData={
        "bookName":bookName,
        "number":pageNumber,
        "part":partName,
        "name":bookMarkName
    }
    islamicBookBookMarksList.append(newBookMarkData)
    bookMarksList["islamicBooks"]=islamicBookBookMarksList
    saveBookMarks(bookMarksList)
def removeislamicBookBookMark(bookMarkName:str):
    bookMarksList=openBookMarksFile()
    islamicBookBookMarksList=bookMarksList["islamicBooks"]
    for islamicBookBookMarkData in islamicBookBookMarksList:
        if islamicBookBookMarkData["name"]==bookMarkName:
            islamicBookBookMarksList.remove(islamicBookBookMarkData)
            break
    bookMarksList["islamicBooks"]=islamicBookBookMarksList
    saveBookMarks(bookMarksList)
def GetislamicBookBookByName(name:str):
    islamicBookBookMarks=openBookMarksFile()
    for islamicBookData in islamicBookBookMarks["islamicBooks"]:
        if islamicBookData["name"]==name:
            return islamicBookData["bookName"],islamicBookData["number"],islamicBookData["part"]
def addNewStoriesBookMark(typeIndex:int,categoryIndex,lineIndex:int,bookMarkName:str):
    bookMarksList=openBookMarksFile()
    try:
        quranBookMarksList=bookMarksList["stories"]
    except:
        quranBookMarksList=bookMarksList["stories"]=[]
    newQuranBookMarkData={
        "type":typeIndex,
        "category":categoryIndex,
        "line":lineIndex,
        "name":bookMarkName
    }
    quranBookMarksList.append(newQuranBookMarkData)
    bookMarksList["stories"]=quranBookMarksList
    saveBookMarks(bookMarksList)
def removeStoriesBookMark(bookMarkName:str):
    bookMarksList=openBookMarksFile()
    ahadeethBookMarksList=bookMarksList["stories"]
    for hadeethBookMarkData in ahadeethBookMarksList:
        if hadeethBookMarkData["name"]==bookMarkName:
            ahadeethBookMarksList.remove(hadeethBookMarkData)
            break
    bookMarksList["stories"]=ahadeethBookMarksList
    saveBookMarks(bookMarksList)
def getStoryBookmark(p,name):
    bookMarksList=openBookMarksFile()
    storiesBookMarksList=bookMarksList["stories"]
    for bkName in storiesBookMarksList:
        if bkName["name"]==name:
            type=bkName["type"]
            category=bkName["category"]
            line=bkName["line"]
            if type==0:
                with open("data/json/prophetStories.json","r",encoding="utf-8-sig") as file:
                    stories=json.load(file)
            elif type==1:
                with open("data/json/quranStories.json","r",encoding="utf-8-sig") as file:
                    stories=json.load(file)
            story=stories[category]
            gui.StoryViewer(p,story,type,category,index=line).exec()