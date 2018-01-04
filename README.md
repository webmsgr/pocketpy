
# pocketpy
The pyphone is a pyboard smart device
It requires a pyboard with a lcd160cr


# loading apps

Apps are very simple to make:
1) make your scripts (main is imported from the start)
2) load the script in a new folder in the scripts folder
3) make a app.conf file (see app.conf)
4) find a way to give it to users. (maybe commit it as a example app?)
5) profit

# app.conf
{"name":"your app name","run":"the file your app runs","doloop":"<true/false true disables wait for USR button press after app is finished>"}
# controls
press usr to switch apps on the menu and exit apps,
touch the screen on menu to launch the app on the screen
