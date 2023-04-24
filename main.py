import socket
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
from appJar import gui
import webbrowser
import threading
import json
import cgi
 

def save(btn):
    link = app.getEntry("Add Link")
    with open("/htdocs/content.html", "a") as file:
        file.write(link)
    with open("/htdocs/info.html", "a") as file:
        file.write(link)


# Function to start the server
def server(btn):
    if btn == "Start":
        host_name = socket.gethostbyname(socket.gethostname())
        port_number = 5151
        # Create an HTTP server
        httpd = HTTPServer((host_name, port_number), SimpleHTTPRequestHandler)
        # Start the server in a separate thread
        server_thread = threading.Thread(target=httpd.serve_forever)
        server_thread.start()
        app.setLabel("SL", f"Server: http://{host_name}:{port_number}")
        app.setLabel("SS", "Online")
        print("Server started at http://{}:{}/htdocs".format(*httpd.socket.getsockname()))
    if btn == "Stop":
        host_name = socket.gethostbyname(socket.gethostname())
        port_number = 5151
        httpd = HTTPServer((host_name, port_number), SimpleHTTPRequestHandler)
        server_thread = threading.Thread(target=httpd.serve_forever)
        httpd.shutdown()
        httpd.server_close()
        server_thread.join()
        app.setLabel("SL", "Server: Offline")
        app.setLabel("SS", "Server: Offline")
        print("Server stopped.")
        app.infoBox("Server stopped", "Server has been stopped successfully")
    if btn == "Kill":
        print("BYE")
        app.stop()


def openbrowser(btn):
    print(f"Opening server in browser")
    host_name = socket.gethostbyname(socket.gethostname())
    port_number = 5151
    webbrowser.open(f"http://{host_name}:{port_number}/htdocs")


def move_file(btn):
    with open("settings.json", 'r') as file:
                data = json.load(file)
                folder_path = data['folder_path']
                server_name = data['server_name']
    file_path = app.getEntry("File")
    file_name = app.getEntry("File Name")
    os.rename(file_path, f"{folder_path}/{os.path.basename(file_path)}")

    with open('htdocs/files.html', "a") as f:
        f.write(f"<div class='file'>")
        f.write(f"\n")
        f.write(f"<a class='subdiv1' href='files/{os.path.basename(file_path)}'>Download</a>")
        f.write(f"\n")
        f.write(f"<p class='subdiv2'>{file_name}</p>")
        f.write(f"\n")
        f.write(f"<p class='subdiv3'>{file_name}</p>")
        f.write(f"\n")
        f.write(f"<p class='subdiv4'>{file_name}</p>")
        f.write(f"\n")
        f.write(f"</div>")
        f.write(f"\n")
    print(f"File {file_name} has been moved to the folder location for the {server_name}")
    app.infoBox("Success", "File moved successfully.")
    
def add_page(btn):
    novo_folder_name = app.getEntry("New Folder Name")
    novo_file_name = app.getEntry("New File Name")
    with open("settings.json", 'r') as file:
            data = json.load(file)
            folder_path = data['folder_path']
    os.makedirs(f"{folder_path}/{novo_folder_name}")
    with open(f"{novo_folder_name}/{novo_file_name}.html", "w") as f:
        f.write("<html><body><h1>Hello World!</h1></body></html>")
    app.infoBox("Success", "Folder and file created successfully.")

app = gui("RSL",UseTk=True)
app.setIcon("/graphics/logo.ico")
app.setToolbarPinned(pinned=True)
# Add a button to start the server

app.startTabbedFrame("Tabs")
app.startTab("Controls")
app.startLabelFrame("Server", 1, 1)
app.addButton("Start", server)
app.addButton("Stop", server)
app.addButton("Kill", server)
app.addButton("Open In Browser", openbrowser)
app.stopLabelFrame()

# AddFiles
app.startLabelFrame("File Controls", 2, 1)
app.addFileEntry("File")
app.addLabelEntry("File Name")
app.addButton("Move File", move_file)
app.stopLabelFrame()

# Set Store Location
app.startLabelFrame("Location", 2, 2)
app.stopLabelFrame()

app.startLabelFrame("Status", 1, 2)
app.addLabel("SL", "---.---.-.--")
app.setLabelFont(20)
app.addLabel("SS", "Offline")
app.stopLabelFrame()
app.stopTab()

app.startTab("Add New Page")
app.addMessage("This will allow you to add a new folder in the files section of your server")
app.addLabelEntry("New Folder Name")
app.addLabelEntry("New File Name")
app.addButton("Create", add_page)
app.stopTab()

app.startTab("Settings")
app.startLabelFrame("Customization")
app.addLabelEntry("Server Name")
app.stopLabelFrame()
app.stopTab()



app.go()
