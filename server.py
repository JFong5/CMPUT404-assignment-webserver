#  coding: utf-8 
import socketserver
import os 

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/



class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))

        #Establish useful variables such as mimes dictionary, http 200 ok response, etc
        directory = "./www"
        mimesDic = {".html": "text/html", ".css": "text/css"}
        
        ok200 = "200 OK"
        error404 = "404 Not FOUND"
        error405 = "405 Method Not Allowed"
        error301 = "301 Moved Permanently"


        #Split the lines of the data and get the HTTP command, the HTTP path and the HTTP version
        dataList = self.data.decode('utf-8').splitlines()
        requestData = dataList[0].split(" ")
        
        #Assign variables to designated request data
        cmd = requestData[0] #GET
        httpPath = requestData[1] #/
        httpVersion = requestData[2] #HTTP/1.1
        
        print("Command:", requestData[0])
        print("Path:", requestData[1])
        print("Version:", requestData[2])
        print("")

        #Check if the HTTP Command is GET
        if (cmd != "GET"): #Give 405 Error if cmd != GET
            response = httpVersion + " " + error405 + "\r\n"
            self.request.send(response.encode("utf-8"))
        
        else:
            
            #Checks if the path is a file (.html, .css, .js )
            path = directory + os.path.normpath(httpPath) #/.www/ 
            fileExtension = os.path.splitext(httpPath)[1]

            print(fileExtension)
            print(mimesDic.get(fileExtension))
            print("")

            #Check if the path is a file
            if os.path.isfile(path):
                print("This is a file\n")

            #Checks if the path is a directory
            elif os.path.isdir(path):
                print("Directory/Root")
                print("INDEX EXISTS", os.path.isfile(path + "index.html"))
                print(path + "index.html")

                ListDirectoryFiles = os.listdir(path)
                print(ListDirectoryFiles)
                print("HTTP PATHHH", httpPath)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()