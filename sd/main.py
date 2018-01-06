import lcd160cr
import pyb
global lasty
lasty = 0
def waitforbutton():
    d = False
    while not d:
        d = pyb.Switch().value()
    while d:
        d = pyb.Switch().value()
def waitforlcd(lcd):
    d = False
    while not d:
        d = lcd.is_touched()
    while d:
        d = lcd.is_touched()
def waitforlcdorbutton(lcd):
    d = False
    while not d:
        d = lcd.is_touched() or pyb.Switch().value()
    while d:
        d = lcd.is_touched() or pyb.Switch().value()
def waitforlcdorbuttonnowait(lcd):
    d = False
    while not d:
        d = lcd.is_touched() or pyb.Switch().value()

def listfromletters(inp):
    out = []
    for letter in inp:
        out.append(letter)
    return out
def listtotext(listto):
    text = ""
    for item in listto:
        text += item
    return text
def userinput(prompt,lcd,letters="default",auto=None):
    clear(lcd)
    do = True
    sel = 0
    text = []
    if (letters == "default"):
        letters = listfromletters("abcdefghijklmnopqrstuvwxyz ")
    letters.append("GO")
    letters.append("<<")
        
    while do:
        printlcd(lcd,0,"Press USR to switch letters",True)
        printlcd(lcd,0,"Touch Screen to type letter")
        printlcd(lcd,0,"letter:'"+letters[sel]+"'")
        printlcd(lcd,0,prompt + listtotext(text))
        waitforlcdorbuttonnowait(lcd)
        if (lcd.is_touched()):
            if (letters[sel] == "<<" or letters[sel] == "GO"):
                if (letters[sel] == "<<"):
                    if (not len(text) == 0):
                        text.pop(len(text)-1)
                else:
                    do = False
            else:
                text.append(letters[sel])
            d = True
            while d:
                d = lcd.is_touched()
        else:
            try:
                tmp = letters[sel+1]
                del tmp
                sel += 1
            except:
                sel = 0
            d = True
            while d:
                d = pyb.Switch().value()
    return listtotext(text)
def err(lcd,mes="???",):
    printlcd(lcd,0,"Hello Human",True)
    printlcd(lcd,0,"This is a error screen",False)
    printlcd(lcd,0,"Error:" + mes)
def main(lcd):
    try:
        import sysos
        sysos.main(lcd,__import__("main"))
    except Exception as exc:
        if (type(exc).__name__ == "OSError"):
            err(lcd,"no sysos.py (Operating System)")
        else:
            raise
    
def clear(lcd):
    global lasty
    lcd.erase()
    lasty = 0
def printlcd(lcd,x,text,doerase=False):
    global lasty
    lastup = 10
    if (doerase):
        clear(lcd)
    lcd.set_pos(x*5,lasty) #lines
    if (len(text) > 20):
        text1 = text[0:20]
        lcd.write(text1)
        lasty += lastup
        printlcd(lcd,0,text.split(text1)[1],False)
    else:
        lcd.write(text)
        lasty += lastup
lcd = lcd160cr.LCD160CR('X')

colors = {
    "black":lcd.rgb(0, 0, 0),
    "white":lcd.rgb(255, 255, 255),
    "red":lcd.rgb(255, 0, 0),
    "blue":lcd.rgb(0, 0, 255),
    "green":lcd.rgb(0, 255, 0),
        }
lcd.set_startup_deco(lcd160cr.STARTUP_DECO_NONE)
lcd.set_orient(lcd160cr.PORTRAIT_UPSIDEDOWN)
clear(lcd)
lcd.set_text_color(colors["white"], colors["black"])
lcd.set_font(1)
printlcd(lcd,0,"Pybootloader 1.0")
printlcd(lcd,0,"Loading.")
pyb.delay(2000)
lcd.erase()
lcd.set_pen(colors["white"],colors["black"])
lasty = 0
lcd.set_pos(0, 0)




try:
    if (__name__ == "__main__"):
        main(lcd)

except Exception as ex:
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    err(lcd,message)


