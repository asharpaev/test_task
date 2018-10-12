import docker
import time
import BaseHTTPServer
from urlparse import urlparse, parse_qs
from os import environ

envs = ["HOST_NAME", "PORT_NUMBER", "DOCKER_HOST"]

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        path=urlparse(s.path).path
        if path=='/':
            """Respond to a GET request."""
            s.send_response(200)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            s.wfile.write("<html><head><title>List of services/containers in Docker Swarm</title></head>")
            s.wfile.write("<body>")

            s.wfile.write("<p>List of services/containers:</p>")
            s.wfile.write("<table border=\"1\"><tbody>")
            containers = client.containers.list()
            for container in containers:
                s.wfile.write("<tr><td>%s</td><td><a href=\"container_logs?id=%s\" target=\"_blank\">"
                              "<button>logs</button></a></td></tr>" % (container.name,container.id) )
            s.wfile.write("</tbody></table>")
            s.wfile.write("</body></html>")
        elif path=='/container_logs':
            try:
                params = parse_qs(urlparse(s.path).query)
                container_id = params["id"][0]
                s.send_response(200)
                s.send_header("Content-type", "text/plain")
                s.end_headers()
                container = client.containers.get(container_id)
                s.wfile.write( container.logs() )
            except:
                s.send_response(412)
                s.send_header("Content-type", "text/html")
                s.end_headers()
                s.wfile.write("<html><head><title>Logs of container in Docker Swarm</title></head>")
                s.wfile.write("<body>")
                s.wfile.write("<p>No given container id</p>")
                s.wfile.write("</body></html>")

        else:
            s.send_response(404)
            s.send_header("Content-type", "text/html")
            s.end_headers()
            s.wfile.write("<html><head><title>List of services/containers Docker Swarm</title></head>")
            s.wfile.write("<body>")

            s.wfile.write("<p>This service does not have page: %s </p>" % path)
            s.wfile.write("</body></html>")
if __name__ == '__main__':
    for env in envs:
        if env in environ:
            vars()[env] = environ.get(env)
    server_class = BaseHTTPServer.HTTPServer
    httpd = server_class((HOST_NAME, int(PORT_NUMBER) ), MyHandler)
    print time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER )
    try:
        client = docker.DockerClient(base_url=DOCKER_HOST)
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER)