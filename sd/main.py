import lcd160cr
import pyb
global lasty
lasty = 0
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


