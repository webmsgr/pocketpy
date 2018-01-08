try:
    import json
except:
    import ujson as json
import base64 as base64
import os as os
import os.path,shutil


def b64encode(stri):
    return base64.b64encode(bytes(stri, 'utf-8')).decode('utf-8')
def b64decode(stri):
    return base64.b64decode(bytes(stri, 'utf-8')).decode('utf-8')
def copyfile(file1,file2):
    try:
        file1 = os.path.abspath(file1)
        file2 = os.path.abspath(file2)
        fil1 = open(file1,"r")
        fil2 = open(file2,"w")
        fil2.write(fil1.read())
        fil1.close()
        fil2.close()
        return True
    except:
        return False
def abspath(pat):
    return os.path.abspath(pat)
def fileexists(fl,path="."):
    return fl in os.listdir(abspath(path))
def pakfiles(filelist,out):
    r=open(out,"w")
    data = {}
    for item in filelist:
        print("packing item " + item,end='')
        data[os.path.basename(item)] = b64encode(open(item).read())
        print(" DONE")
    r.write(b64encode(str(data).replace("'","\"")))
    r.close()
    
def listfilesinpak(app):
    filedata = b64decode(open(app,"r").read())
    
    filedata = json.loads(filedata)
    tmp = []
    for name in filedata:
        tmp.append(name)
    return tmp

def lenpak(app):
    return len(listfilesinpak(app))

def apppak(appfile,conffile,addfiles,ver):
    pakname = appfile.split(".")[0]+".app"
    print("Copying files:",end='')
    try:
        os.mkdir("app")
    except:
        print("",end='')

    copyfile(appfile,os.path.join(abspath(".\\app"),appfile))
    appfile = os.path.join(abspath(".\\app"),appfile)
    if (not fileexists(conffile)):
        
        r = open(conffile,"w")
        data = {
            "appname":appfile,
            "appicon":"none",
            "description":"Config Autogenerated!",
            "version":str(ver)

            }
        r.write(str(data))
        r.close()
    copyfile(conffile,os.path.join(abspath(".\\app"),conffile))
    conffile = os.path.join(abspath(".\\app"),conffile)
    ite = 0
    for file in addfiles:
        copyfile(file,os.path.join(abspath(".\\app"),file))
        addfiles[ite] = os.path.join(abspath(".\\app"),file)
        ite +=1
    print("DONE")

    files = [appfile,conffile] + addfiles
    pakfiles(files,pakname)
    return abspath(pakname)




def breakpkg(pkg,path="."):
    path = os.path.abspath(path)
    base64.decode(open(pkg,'rb'), open("tmp",'wb'))
    arc = json.load(open("tmp"))
    try:
        os.mkdir("tmpex")
    except:
        osx=os
    for file in arc:
        data = arc[file]
        f = open("tmpex\\"+file.split(".")[0]+".b64","w")
        f.write(data)
        f.close()
    for file in arc:
        base64.decode(open("tmpex\\"+file.split(".")[0]+".b64",'rb'), open(os.path.join(path,file),'wb'))
    shutil.rmtree("tmpex", ignore_errors=True)
    os.remove("tmp")