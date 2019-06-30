import requests
import os, sys
from getpass import getpass
import glob
import shutil
import subprocess
import pandas as pd
import io
import XML_work

    
username=input("ВАШ ЛОГИН НА ГИТХАБЕ")
#print(requests.get('https://api.github.com/users/'+username+'?username='+token).json())
password = getpass()

req = requests.get('https://api.github.com/user/repos',
                    auth=(username, password))
#print(req)

#print(req.json()[1])
links=[]
for repo in req.json():
    if not repo['private']:
        links.append(repo['html_url']+".git")

#for link in links:
#    name = "https://api.github.com/repos/"+link+"/contents"
 #   repository = requests.get(name+"client_id=03ca2f80e00559fe7157&client_secret=70f59b63bd0180a027852277376723fbf06dfb27").json()
  #  print(repository)
   # for i in repository:
    #    if(i["type"]!="file"):
     #       #print(i["path"])
      #      linker(name+i["path"])
d={}
def hack(path):
    file = io.open(path, "r", encoding="UTF-8")
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
                    print(df.loc[i,"count"]) 
    dt = df.pivot_table(['count'],['name'], aggfunc='sum', fill_value = 0)
  
    if len(dt)>0:
        dt = dt[dt["count"]>0]
    dt.to_csv("main.csv")
    f=open("main.csv")
    for line in f:
        if not(line[0:4]=="name"):
            #print(line)
            if(d.get(line.split(",")[0])==None):
                d[line.split(",")[0]]=int(line.split(",")[1].replace("\n",""))
            else:
                d[line.split(",")[0]]=d[line.split(",")[0]]+int(line.split(",")[1].replace("\n",""))
    global cout
    cout=0
def deepWatch(path):
    for obj in glob.glob(path+"/*"):
        errors = []
        if(obj.find(".cpp")!=-1 or obj.find(".py")!=-1 or obj.find(".pyc")!=-1 
        or obj.find(".h")!=-1): #тут хорошо бы указать какие файлы нам нужны, чтобы их подбирать, а ненужные не подбирать
            #print("ФАЙЛ ДЕТЕКТЕД: "+obj)
            if (obj.find(".cpp")!=-1 or obj.find(".h")!=-1):
                a=0
                
            if (obj.find(".py")!=-1 or obj.find(".pyc")!=-1):
                a=0
                
                #hack(obj)
        else:
            deepWatch(obj)
        


for link in links:
    os.system('echo "" > errors_cpp.txt')
    os.system('echo "" > errors_py.txt')
    command = "git clone "+link
    os.system(command)
    path = link.replace("https://github.com/"+username+"/", "")
    path = path.replace(".git", "")
    deepWatch('./'+path)

    error = os.system("./cppcheck.exe -q -j4 --enable=performance,portability,warning,style " + path+" 2>> errors_cpp.txt")
    cpp_errors = open("errors_cpp.txt")
    cpp_errors_number = 0
    XML_work.createXML("cpp_error_codes_"+ path +".xml")
    XML_work.addXML("Refactor", "0", "cpp_error_codes_"+ path +".xml", 1)
    XML_work.addXML("Convention", '0', "cpp_error_codes_"+ path +".xml", 2)
    XML_work.addXML("Warning", '0', "cpp_error_codes_"+ path +".xml",3 )
    XML_work.addXML("Error", '0', "cpp_error_codes_"+ path +".xml", 4)
    XML_work.addXML("Fatal", '0', "cpp_error_codes_"+ path +".xml", 5)
    for line in cpp_errors:
        
        line = line.replace(":","",1)
        err_code_pos = line.find(":")+3
        if (line.find(":")!=-1):
            #print("**** Код ошибки: "+line[err_code_pos])
            if(line[err_code_pos]=="w"):
                current_num_errors = XML_work.parseXML("Warning","cpp_error_codes_"+ path +".xml")
                cpp_errors_number+=1
                XML_work.editXML("Warning", str(int(current_num_errors)+1), "cpp_error_codes_"+ path +".xml")
            if(line[err_code_pos]=="r"):
                current_num_errors = XML_work.parseXML("Refactor","cpp_error_codes_"+ path +".xml")
                cpp_errors_number+=1
                XML_work.editXML("Refactor", str(int(current_num_errors)+1), "cpp_error_codes_"+ path +".xml")
            if(line[err_code_pos]=="e"):
                current_num_errors = XML_work.parseXML("Error","cpp_error_codes_"+ path +".xml")
                cpp_errors_number+=1
                XML_work.editXML("Error", str(int(current_num_errors)+1), "cpp_error_codes_"+ path +".xml")
            if(line[err_code_pos]=="f"):
                current_num_errors = XML_work.parseXML("Fatal","cpp_error_codes_"+ path +".xml")
                cpp_errors_number+=1
                XML_work.editXML("Fatal", str(int(current_num_errors)+1), "cpp_error_codes_"+ path +".xml")
            if(line[err_code_pos]=="c"):
                current_num_errors = XML_work.parseXML("Convention","cpp_error_codes_"+ path +".xml")
                cpp_errors_number+=1
                XML_work.editXML("Convention", str(int(current_num_errors)+1), "cpp_error_codes_"+ path +".xml")
            
    print("Количество ошибок C++ в проекте "+path+": "+str(cpp_errors_number))

    cpp_errors.close()

    os.system("pylint " +'./'+path +">>errors_py.txt")
    py_errors = open("errors_py.txt", encoding="utf8")
    py_errors_num=0
    XML_work.createXML("py_error_codes_"+ path +".xml")
    XML_work.addXML("Refactor", "0", "py_error_codes_"+ path +".xml", 1)
    XML_work.addXML("Convention", '0', "py_error_codes_"+ path +".xml", 2)
    XML_work.addXML("Warning", '0', "py_error_codes_"+ path +".xml",3 )
    XML_work.addXML("Error", '0', "py_error_codes_"+ path +".xml", 4)
    XML_work.addXML("Fatal", '0', "py_error_codes_"+ path +".xml", 5)
    for line in py_errors:
        line = line.replace(":","",1)
        line = line.replace(":","",1)
        #print(line)
        err_code_pos = line.find(":")+2
        if (line.find(":")!=-1):
            #print("**** Код ошибки: "+line[err_code_pos])
            if(line[err_code_pos]=="W"):
                current_num_errors = XML_work.parseXML("Warning","py_error_codes_"+ path +".xml")
                py_errors_num+=1
                XML_work.editXML("Warning", str(int(current_num_errors)+1), "py_error_codes_"+ path +".xml")
            if(line[err_code_pos]=="R"):
                current_num_errors = XML_work.parseXML("Refactor","py_error_codes_"+ path +".xml")
                py_errors_num+=1
                XML_work.editXML("Refactor", str(int(current_num_errors)+1), "py_error_codes_"+ path +".xml")
            if(line[err_code_pos]=="E"):
                current_num_errors = XML_work.parseXML("Error","py_error_codes_"+ path +".xml")
                py_errors_num+=1
                XML_work.editXML("Error", str(int(current_num_errors)+1), "py_error_codes_"+ path +".xml")
            if(line[err_code_pos]=="F"):
                current_num_errors = XML_work.parseXML("Fatal","py_error_codes_"+ path +".xml")
                py_errors_num+=1
                XML_work.editXML("Fatal", str(int(current_num_errors)+1), "py_error_codes_"+ path +".xml")
            if(line[err_code_pos]=="C"):
                current_num_errors = XML_work.parseXML("Convention","py_error_codes_"+ path +".xml")
                py_errors_num+=1
                XML_work.editXML("Convention", str(int(current_num_errors)+1), "py_error_codes_"+ path +".xml")
    print("Количество ошибок Python в проекте "+path+": "+str(py_errors_num))
    py_errors.close()

    #for i in d:
    #    cout+=d[i]
    #for i in d:
    #    d[i]=d[i]/cout*100
    #shutil.rmtree(path)