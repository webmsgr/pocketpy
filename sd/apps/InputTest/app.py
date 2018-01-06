main.printlcd(main.lcd,0,"Press USR",True)
main.waitforbutton()
main.printlcd(main.lcd,0,"You said: " + main.userinput("Test prompt",main.lcd),True)
