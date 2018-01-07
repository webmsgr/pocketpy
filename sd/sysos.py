
global funcs
import pyb,os,json

global name
#functions:
#err(lcd,message) <- display a error message and continue
#clear(lcd) <-clear lcd
#printlcd(lcd,x,text,Doerase) <--- erase if doerase is true then print text. (20 char on line)
def rand1d():
    return str(pyb.rng())[0]
def clear(lcd,impo):
    impo.lcd.erase()
    impo.lasty = 0
    
    
def waitforbuttonorlcd(lcd):
    d = False
    while not d:
        d = pyb.Switch().value()
        if (lcd.is_touched()):
            d = True
            return True
    return False
def waitforbutton():
    d = False
    while not d:
        d = pyb.Switch().value()
    while d:
        d = pyb.Switch().value()
def waitrelease(lcd):
    d = True
    while d:
        d = lcd.is_touched() or pyb.Switch().value()
def appmenu(lcd,funcs):
    global banana
    try:
        os.mkdir(".//app")
        applist = []
    except:
        applist = os.listdir(".//app")
    sel = 0
    appname = {}
    for app in applist:
        try:
            r = open("\\app\\"+app+"\\app.conf")
            r = json.loads(r.read())
            name = r["name"]
        except:
            name = app
        appname[app] = name 
    applist.append("exit")
    appname["exit"] = "Exit Menu"
    if (not len(applist) == 0):
        do = True
        sel = 0
        t = 0
        while do:
            funcs.printlcd(lcd,0,"App Menu",True)
            t = 0
            
            for app in applist:
                if (t == sel):
                    funcs.printlcd(lcd,0,str(t+1)+") >"+appname[app] + "<")
                else:
                    funcs.printlcd(lcd,0,str(t+1)+")"+appname[app])
                t += 1
            
            if (waitforbuttonorlcd(lcd)):
                do = False
                savesel = sel
            else:
                try:
                    print(applist[sel+1])
                    sel += 1
                except:
                    sel = 0
            waitrelease(lcd)
        d = lcd.get_touch()
        
        return applist[savesel]
                
def AppLoad(app_file):
    with open(app_file) as f:
        code = compile("import main\n"+f.read(), app_file, 'exec')
        exec(code)           
def blank():
    return ""
def settings(lcd,funcs):
    global name
    option = selectionlist(["Edit Name","Exit"],"Settings",funcs,lcd)
    if (option == "Exit"):
        return
    if (option == "Edit Name"):
        r = open("name.conf","w")
        newname = funcs.userinput("New Name:",lcd)
        r.write(newname)
        r.close()
        name = newnameb
        return
def selectionlist(items,name,funcs,lcd):
    waitrelease(lcd)
    do = True
    sel = 0
    t = 0
    while do:
        funcs.printlcd(lcd,0,name,True)
        t = 0
        
        for item in items:
            if (t == sel):
                funcs.printlcd(lcd,0,str(t+1)+") >"+ item + "<")
            else:
                funcs.printlcd(lcd,0,str(t+1)+")"+item)
            t += 1
        
        if (waitforbuttonorlcd(lcd)):
            do = False
            savesel = sel
        else:
            try:
                print(items[sel+1])
                sel += 1
            except:
                sel = 0
        waitrelease(lcd)
    d = lcd.get_touch()
    
    return items[savesel]
    
def loginscreen(lcd,funcs,name="User"):
    usermsg = "Welcome " + name
    listitems = {"Settings":settings,"App Menu":"return"}
    sellist = ["App Menu"]
    for item in listitems:
        if (not item == "App Menu"):
            sellist.append(item)
    sel = 0
    
    do = True
    while do:
        count = 0
        funcs.printlcd(lcd,0,usermsg,True)
        for item in sellist:
            if (count == sel):
                funcs.printlcd(lcd,0,str(count+1)+") >"+item+"<",False)
            else:
                funcs.printlcd(lcd,0,str(count+1)+")"+item,False)
            
            count += 1
        
        funcs.waitforlcdorbuttonnowait(lcd)
        if (lcd.is_touched()):
            if (listitems[sellist[sel]] == "return"):
                waitrelease(lcd)
                
                do = False
                return
            else:
                listitems[sellist[sel]](lcd,funcs)
        else:
            try:
                print(sellist[sel+1])
                sel += 1
            except:
                sel = 0
        waitrelease(lcd)
def loadname():
    global name
    try:
        conf = open("name.conf",'r')
        name = conf.read()
        conf.close()
    except:
        r = open("os.conf","w")
        r.write("User")
        r.close()
        name = "User"
def main(lcd,leimport):
    global funcs
    global name
    funcs = leimport
    loadname()
    while True:
        loginscreen(lcd,funcs,name)
        while True:
            
            currentapp = appmenu(lcd,funcs)
            if (currentapp == "exit"):
                break
            try:
                r = open("\\app\\"+currentapp+"\\app.conf")
                r = json.load(r)
            except:
                r = {
                    "run":"app.py"
                    }
            
            try:
                clear("",funcs)
                AppLoad("\\app\\"+currentapp+"\\"+r["run"])
                try:
                    dontwait = r["isloop"]
                    if (dontwait == "true"):
                        dontwait = True
                    else:
                        dontwait = False
                except:
                    dontwait = False
                if (not dontwait):
                    waitforbutton()
            except:
                blank()
            
        
    

            
        
        
    
    


