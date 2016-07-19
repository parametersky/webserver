from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant,MenuItem
import codecs

#
#this is python script to build a simple server handling GET and POST request.
#
#thins need to know: cgi module
#
#
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurant"):
                items = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ouput = ""
                ouput += "<html><body>"
                for item in items:
                    print item.name
                    ouput += item.name.encode('utf-8')
                    ouput += "</br>"
                ouput += "</body></html>"
                self.wfile.write(ouput)
                return
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ouput = ""
                ouput += "<html><body>"
                ouput += " <h1> Hello !</h1> "
                ouput += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What do you like me to say?</h2>
                <input name="message" type="text"><input type = "submit" value="Submit"></form>'''
                ouput += "</body></html>"
                self.wfile.write(ouput)
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                ouput = ""
                ouput += "<html><body>"
                ouput += " <h1>&#161 Hola !</h1> "
                ouput += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What do you like me to say?</h2><input name="message" type="text"><input type = "submit" value="Submit"></form>'''
                ouput += "</body></html>"
                self.wfile.write(ouput)
                return
            else:
                self.send_error(404,'File Not Found: %s' % self.path)
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
            ouput = ""
            ouput += "<html><body>"
            ouput += " <h2>Okey, how about this: </h2> "
            ouput += "<h1> %s </h1>" % messagecontent[0]
            ouput += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What do you like me to say?</h2><input name="message" type="text"><input type = "submit" value="Submit"></form>'''
            ouput += "</body></html>"
            self.wfile.write(ouput)

        except:
            pass



def main():
    try:
        port=8080
        server = HTTPServer(('',port),WebServerHandler)
        print "start server at port:%s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stop server"
        server.socket.close()
if __name__ == '__main__':
    main()
