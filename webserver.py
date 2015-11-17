from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = ""
                message += "<html><body>Hello!</body></html>"
                self.wfile.write(message)
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = ""
                message += "<html><body>&#161Hola <a href = '/hello' > Back to Hello</a>!</body></html>"
                self.wfile.write(message)
                return
            else:
                self.send_error(404,'File Not Found: %s' % self.path)
        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)



def main():
    try:
        port=8080
        server = HTTPServer(('',port),WebServerHandler)
        print "start server at port:%s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stop server"
        server.socket.close()
if __name__ = '__main__':
    main()