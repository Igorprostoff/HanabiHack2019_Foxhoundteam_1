import pandas as pd
import io


d={}
file = io.open("ind.py","r", encoding="UTF-8")
df = pd.DataFrame(columns = ['name', 'var', 'count'])
countofDf=0

for line in file:
    Varfrom = line.find("from")
    Varimport = line.find("import")
    VarAs = line.find("as")
    if(Varfrom==-1 and Varimport!=-1 and VarAs==-1):
        line.replace("\n", "")
        var = line.split()
        df.loc[countofDf,"name"]=var[1]
        df.loc[countofDf,"var"]=var[1]
        df.loc[countofDf,"count"]=0
        countofDf+=1
    elif(Varfrom!=-1 and Varimport!=-1 and VarAs==-1):
        line.replace("\n", "")
        var = line.split()
        df.loc[countofDf,"name"]=var[1]
        df.loc[countofDf,"var"]=var[3]
        df.loc[countofDf,"count"]=0
        countofDf+=1
    elif(Varfrom==-1 and Varimport!=-1 and VarAs!=-1):
        line.replace("\n", "")
        var = line.split()
        df.loc[countofDf,"name"]=var[1]
        df.loc[countofDf,"var"]=var[3]
        df.loc[countofDf,"count"]=0
        countofDf+=1
    else:
        #print(line)
        for i in range(0,countofDf):
            if(line.find(df.loc[i,"var"]) !=-1  and not(line[line.find(df.loc[i,"var"])-1] >="A" and line[line.find(df.loc[i,"var"])-1] <="z") and not(line[line.find(df.loc[i,"var"])+len(df.loc[i,"var"])] >="A" and line[line.find(df.loc[i,"var"])+len(df.loc[i,"var"])] <="z") and not(line[line.find(df.loc[i,"var"])+len(df.loc[i,"var"])] >="0" and line[line.find(df.loc[i,"var"])+len(df.loc[i,"var"])] <="9")):
                if(line.find("=")!=-1 and line[line.find("=")+1]!="=" and line.find(df.loc[i,"var"]) > line.find("=") ):
                    var = line[:line.find("=")].replace(" ","")
                    if(len(df[df["var"]==var])==0):
                       #print("var="+var)
                       #if(var.find(".")):
                       df.loc[countofDf,"name"]=df.loc[i,"name"]
                       df.loc[countofDf,"var"]=var
                       df.loc[countofDf,"count"]=0
                       countofDf+=1
                df.loc[i,"count"]+=1
dt = df.pivot_table(['count'],['name'], aggfunc='sum', fill_value = 0)
dt = dt[dt["count"] >0]
print("=========")
print(dt["count"] >0)
print(dt)
dt.to_csv("main.csv")
f=open("main.csv")
for line in f:
    if not(line[0:4]=="name"):
        #print(line)
        if(d.get(line.split(",")[0])==None):
            d[line.split(",")[0]]=int(line.split(",")[1].replace("\n",""))
        else:
            d[line.split(",")[0]]=d[line.split(",")[0]]+int(line.split(",")[1].replace("\n",""))
print(d)