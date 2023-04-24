import subprocess
import os
from appJar import gui
import threading
import webbrowser
from http.server import HTTPServer, SimpleHTTPRequestHandler
import json
import yaml
with open ("server/mkdocs.yml","r") as f:
    config = yaml.safe_load(f)
with open ('settings.json','r') as f:
    data = json.load(f)
    s_name = data['s_name']
    s_path = data['s_path']
    print(s_name)
    os.chdir(s_path)
def cngcfg():
    #Change Name
    nname = input("Enter New Name: ")
    config["server_name"] = nname
    with open("mkdocs.yml","w")as f:
        yaml.dump(config,f)
def new():
    name=input("Enter New Name: ")
    subprocess.run(["mkdocs","new", name])
    os.chdir(name)
    print("done")
    subprocess.run(["mkdocs","serve"])
def start():
    subprocess.run(["mkdocs","serve"])
    app.setLabel("SL1","Active")
def build():
    subprocess.run(["mkdocs","build"])
def write():
    link = input("Link:")
    file_path = "index.md"
    with open(file_path, "a") as f:
        f.write("\n ### new line\n")
        f.write("\n Car Name:")
        f.write("\n Car Year:")
        f.write(f"[Download]({link})")

app = gui("RRS IV")
#Controls
app.startLabelFrame("Controls")
app.addButton("New",new)
app.addButton("start",start)
app.addButton("Write",write)
app.addButton("Build",build)
app.stopLabelFrame()
#Info
app.startLabelFrame("info")
app.addLabel("SL1","--:--:--")
app.addLabel("SL2","--:--:--")
app.addLabel("SL3","--:--:--")
app.stopLabelFrame()


app.go()
