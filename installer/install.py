import pak,requests
pakd = requests.get("https://raw.githubusercontent.com/webmsgr/pocketpy/master/build.pkg").text
open("pak.pak","w").write(pakd)

pak.breakpkg("pak.pak",input("path to install location:"))
