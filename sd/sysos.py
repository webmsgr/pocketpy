
global funcs
import pyb,os,json

global banana
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
        
    if (not len(applist) == 0):
        do = True
        while do:
            try:
                funcs.printlcd(lcd,0,str(sel+1)+")"+appname[applist[sel]],True)
            except:
                sel = 0
            if (waitforbuttonorlcd(lcd)):
                do = False
                savesel = sel
            
            d = pyb.Switch().value()
            while d:
                d = pyb.Switch().value()
            if (not sel == len(applist)-1):
                sel += 1
            else:
                sel = 0
        d = lcd.get_touch()
        
        return applist[savesel]
                
def AppLoad(app_file):
    with open(app_file) as f:
        code = compile("import main\n"+f.read(), app_file, 'exec')
        exec(code)           
def blank():
    return ""
    
    
def main(lcd,leimport):
    global funcs
    global banana
    funcs = leimport
    while True:
        currentapp = appmenu(lcd,funcs)

        try:
            r = open("\\app\\"+currentapp+"\\app.conf")
            r = json.load(r)
        except:
            r = {
                "run":"main.py"
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
            
        
    

            
        
        
    
    


