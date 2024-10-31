import json
with open("data/json/quran.json","r",encoding="utf-8-sig") as file:
    data=json.load(file)
def getSurahs():
    surahs={}
    for key,value in data.items():
        ayahs={}
        for ayah in value["ayahs"]:
            ayahs["{} ({})".format(ayah["text"],str(ayah["numberInSurah"]))]=ayah["numberInSurah"]
        surahs[str(value["number"])+value["name"]]=[key,"\n".join(ayahs),key]
    return surahs
def getJuz():
    juz={}
    for key,value in data.items():
        for ayah in value["ayahs"]:
            juzNumber=ayah["juz"]
            if str(juzNumber) in juz:
                List=juz[str(juzNumber)]
                List.append("{} ({})".format(ayah["text"],str(ayah["numberInSurah"])))
            else:
                List=["{} ({})".format(ayah["text"],str(ayah["numberInSurah"]))]
            juz[str(juzNumber)]=List
    for j in juz:
        content=juz[j]
        juz[j]=[j,"\n".join(content)]
    return juz
def getPage():
    juz={}
    for key,value in data.items():
        for ayah in value["ayahs"]:
            juzNumber=ayah["page"]
            if str(juzNumber) in juz:
                List=juz[str(juzNumber)]
                List.append("{} ({})".format(ayah["text"],str(ayah["numberInSurah"])))
            else:
                List=["{} ({})".format(ayah["text"],str(ayah["numberInSurah"]))]
            juz[str(juzNumber)]=List
    for j in juz:
        content=juz[j]
        juz[j]=[j,"\n".join(content)]
    return juz
def getHezb():
    juz={}
    for key,value in data.items():
        for ayah in value["ayahs"]:
            juzNumber=ayah["hizbQuarter"]
            if str(juzNumber) in juz:
                List=juz[str(juzNumber)]
                List.append("{} ({})".format(ayah["text"],str(ayah["numberInSurah"])))
            else:
                List=["{} ({})".format(ayah["text"],str(ayah["numberInSurah"]))]
            juz[str(juzNumber)]=List
    for j in juz:
        content=juz[j]
        juz[j]=[j,"\n".join(content)]
    return juz
def getHizb():
    juz={}
    times=1
    juzNumber=1
    Q=1
    for key,value in data.items():
        for ayah in value["ayahs"]:
            qNumber=ayah["hizbQuarter"]
            if Q!=qNumber:
                times+=1
                Q+=1
            if times==5:
                times=1
                juzNumber+=1

    
            if str(juzNumber) in juz:
                List=juz[str(juzNumber)]
                List.append("{} ({})".format(ayah["text"],str(ayah["numberInSurah"])))
            else:
                List=["{} ({})".format(ayah["text"],str(ayah["numberInSurah"]))]
            juz[str(juzNumber)]=List
    for j in juz:
        content=juz[j]
        juz[j]=[j,"\n".join(content)]
    return juz
def getAyah(text):
    for key,value in data.items():
        for ayah in value["ayahs"]:
            t="{} ({})".format(ayah["text"],str(ayah["numberInSurah"]))
            if t==text:
                return ayah["numberInSurah"],key,ayah["juz"],ayah["page"]
    return 1,"1","1","1"
def getQuran(from_surah,from_ayah,to_surah,to_ayah):
    result=[]
    for Surah,value in data.items():
        if from_surah==int(Surah):
            for Ayah in value["ayahs"]:
                if from_ayah<=int(Ayah["numberInSurah"]):
                    result.append(Ayah["text"])
            if to_surah==int(Surah):
                if to_ayah==int(Ayah["numberInSurah"]):
                    break
                elif from_ayah<int(Ayah["numberInSurah"]):
                    result.append(Ayah["text"])
            elif from_surah<int(Surah):
                result.append(Ayah["text"])
    return result
def searchinquran(keyword,ayah_list):
    result=[]
    for ayah in ayah_list:
        if keyword in ayah:
            result.append(ayah)
    return result