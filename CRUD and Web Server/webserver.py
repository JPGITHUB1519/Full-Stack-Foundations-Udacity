from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
class webserverHandler(BaseHTTPRequestHandler):
    # get method
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Hello!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/hola"):
                # 200 -> get sucesfully
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body><h1>&#161Hola!<a href='/hello'>Back to Hello</a></h1></body></html>"
                # print html
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, "File not found %s" % self.path)

    def do_POST(self):
        try:
            # http post sucessfully
            self.send_response(301)
            self.end_headers()
            # receving the data of the form
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            output = ""
            output += "<html><body>"
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "<h2>Okay, how about this : </h2>"
            output += "<h1> %s </h1>" % messagecontent[0]
            output += "</body></html>"
            output += "</body></html>"
            self.wfile.write(output)
            print output
        except Exception as e:
            pass

# initialize server
def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stooping the server..."
        server.socket.close()

# running not import
if __name__ == "__main__" :
    main()