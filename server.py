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
        #print ("Got a request of: %s\n" % self.data)
        #self.request.sendall(bytearray("OK",'utf-8'))

        #Establish useful variables such as allowed extentions, http 200 ok response, etc
        directory = "/www"
        allowedExtensions = [".html", ".css", ".js"]
        
        ok200 = "200 OK"
        error404 = "404 Not FOUND"
        error405 = "405 Method Not Allowed"
        error301 = "301 Moved Permanently"


        #Split the lines of the data and get the HTTP command, the HTTP path and the HTTP version
        dataList = self.data.decode('utf-8')
        data = dataList.splitlines()
        
        requestData = data[0].split(" ")

        #Assign request data to designated variables
        cmd = requestData[0] #GET
        httpPath = requestData[1] #/
        httpVersion = requestData[2] #HTTP/1.1

        #Check if HTTP command is GET
        if cmd == "GET": 
            #Checks if the httpPath's ends with the allowed extention
            if not httpPath.endswith(tuple(allowedExtensions)) and not httpPath.endswith("/"):
                #Give Error 303 if httpPath doesn't end with the allowed Extensions
                output = httpVersion + " " + error301 + "\r\n" + "Location: " + httpPath + "/\r\n"
                self.request.send(output.encode("utf-8"))
                return

            #establish path
            path = os.getcwd() + directory + httpPath #./www/ 

            #Checks if the path is a directory
            if os.path.isdir(path):
                ListDirectoryFiles = os.listdir(path) #list directories
                         
                #Checks if the index.html is in the Directory
                if "index.html" in ListDirectoryFiles:
                    path = os.path.join(path, 'index.html')
                
                print(path)
                #Checks if index.html is in the list directory
                if "index.html" not in ListDirectoryFiles: #Give a Error 404
                    output = httpVersion + " " + error404 + "\r\n"
                    self.request.send(output.encode("utf-8"))
                
            #Try to open and read file to get htmlData
            try:
                file = open(path, "rb")
                htmlData = file.read()
                file.close()
                    
            except FileNotFoundError: #If file not found, give 404 error
                output = httpVersion + " " + error404 + "\r\n"
                self.request.send(output.encode("utf-8"))
                return
            
            #Check if the httpPath endswith .css
            if httpPath.endswith(".css"):
                mimetype = "text/css"
                output = httpVersion + " " + ok200 + "\r\n" + "Content-Type: " + mimetype + "\r\n\r\n"
                print(output)
            else:
                mimetype = "text/html"
                output = httpVersion + " " +ok200 + "\r\n" + "Content-Type: " + mimetype + "\r\n\r\n"
                print(output)
            
            #Send encoded out put
            self.request.send(output.encode("utf-8"))
            self.request.sendall(htmlData)
        
        #Check if the HTTP Command is GET
        else: #Give Error 405 if cmd != GET
            output = httpVersion + " " + error405 + "\r\n"
            self.request.send(output.encode("utf-8"))
            return


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()