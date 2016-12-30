from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from restaurant_queries import *
import cgi
import re
class webserverHandler(BaseHTTPRequestHandler):
    # get method
    def do_GET(self):
        try:
            # show all restaurants
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<h1>Restaurants : </h1>"
                restaurants = get_restaurants()
                for restaurant in restaurants :
                    output += "<h3 style='color:red;'>%s</h3>" % restaurant.name
                    output += "<a href='/restaurants/edit/%s' style='display:block; font-size:20px;'>Edit</a>" % restaurant.id
                    output += "<a href='/restaurants/delete/%s' style='display:block; font-size:20px;'>Delete</a>" % restaurant.id

                output += "<h2>Record new Restaurant <a href='/restaurants/new'>New Restaurant</a></h2>"
                output += "</body></html>"
                self.wfile.write(output)
                #print output
                return

            if self.path.endswith("/restaurants/new"):
                # 200 -> get sucesfully
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                # print html
                output += "<html><body>"
                output += "<h1>Create new Restaurant : </h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><h2>Name of the Restaurant</h2><input name="restaurant_name" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "<a href='/restaurants'>Back to Restaurants list</a></h1></body></html>"
                output += "</body></html>"
                self.wfile.write(output)
                #print output
                return

            # regular expression to search parameters
            if None != re.search('/restaurants/edit/*', self.path):
                # 200 -> get sucesfully
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                # get the id in the parameter
                id = self.path.split('/')[-1]
                restaurant = get_restaurant_byid(id) 
                output += "<html><body>"
                output += "<h1>Edit Restaurant <span style='color:red'>%s</span> </h1>" % restaurant.name
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/edit/%s'><h2>Edit Name of the Restaurant</h2><input name="restaurant_name" type="text"><input type="submit" value="Submit"></form>''' % (restaurant.id)
                output += "<a href='/restaurants'>Back to Restaurants list</a></h1></body></html>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if None != re.search('/restaurants/delete/*', self.path):
                # 200 -> get sucesfully
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                # get the id in the parameter
                id = self.path.split('/')[-1]
                restaurant = get_restaurant_byid(id) 
                output += "<html><body>"
                output += "<h1>Delete Restaurant <span style='color:red'>%s</span> </h1>" % restaurant.name
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/delete/%s'><h2>Edit Name of the Restaurant</h2><p>Seguro que desea eliminar este regitro?<input type="submit" value="Eliminar"></form>''' % (restaurant.id)
                output += "<a href='/restaurants'>Back to Restaurants list</a></h1></body></html>"
                output += "</body></html>"
                self.wfile.write(output)
                return

        except IOError:
            self.send_error(404, "File not found %s" % self.path)

    def do_POST(self):
        try:
            # http post sucessfully
            if self.path.endswith("/restaurants/new"):
                self.send_response(301)
                # redirection
                self.send_header('Location', '/restaurants')
                self.end_headers()
                # receving the data of the form
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('restaurant_name')
                insert_restaurant(messagecontent[0])

            if None != re.search('/restaurants/edit/*', self.path):
                self.send_response(301)
                # redirection
                self.send_header('Location', '/restaurants')
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    # put [0] always
                    restaurant_name = fields.get('restaurant_name')[0]
                    restaurant_id = self.path.split('/')[-1]
                    edit_restaurant(restaurant_id, restaurant_name)

            if None != re.search('/restaurants/delete/*', self.path):
                self.send_response(301)
                # redirection
                self.send_header('Location', '/restaurants')
                self.end_headers()
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    restaurant_id = self.path.split('/')[-1]
                    delete_restaurant(restaurant_id)

        except Exception as e:
            pass
    # edit restaurants/id/edit   restaurants/id/edit

        
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