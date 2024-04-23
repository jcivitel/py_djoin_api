import base64
import json
import socket
import subprocess
import threading

import win32service
import win32serviceutil

# TODO: use dynamic login
# Username and password for Basic Authentication
USERNAME = 'user'
PASSWORD = 'password'

class WebServer(win32serviceutil.ServiceFramework):
    _svc_name_ = "py_djoin_api"
    _svc_display_name_ = "Python Djoin API"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = threading.Event()
        self.app_process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.stop_event.set()
        return 0

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        self.start_web_server()

    def start_web_server(self):
        host = '0.0.0.0'
        port = 80
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((host, port))
            server_socket.listen(5)
            print(f"Web server listening on port {port}")
            while not self.stop_event.is_set():
                client_socket, address = server_socket.accept()
                self.app_process = threading.Thread(target=self.handle_client, args=(client_socket,))
                self.app_process.start()
                self.app_process.join()

    def handle_client(self, client_socket):
        request_data = client_socket.recv(1024)
        print(request_data)
        request_lines = request_data.decode().split('\r\n')

        # Extract request method and target URL
        request_line = request_lines[0].split()
        request_method = request_line[0]
        target_url = request_line[1]

        # Extract Authorization header
        authorization_header = None
        for line in request_lines:
            if line.startswith('Authorization: Basic'):
                authorization_header = line.split(' ', 1)[1]
                break

        if authorization_header:
            # Decode and validate credentials
            decoded_credentials = base64.b64decode(authorization_header).decode()
            username, password = decoded_credentials.split(':', 1)

            if username == USERNAME and password == PASSWORD:

                if request_method == 'GET' and target_url.startswith('/join?computername='):
                    # Extract the computer name from the URL
                    computer_name = target_url.split('=')[1]
                    print(f"Current Computername {computer_name}")

                    powershell_command = f"djoin /PROVISION /REUSE /DOMAIN test /MACHINE {computer_name} /SAVEFILE /PRINTBLOB | ConvertTo-Json"

                    # PowerShell-Befehl ausführen und Ergebnis abrufen
                    result = subprocess.run(['powershell', '-Command', powershell_command], capture_output=True, text=True)
                    output = result.stdout.strip()
                    response_data = json.loads(output)
                    response = json.dumps(response_data)
                    response_headers = "HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
                    client_socket.sendall((response_headers + response).encode())
                else:
                    # Respond with a 404 error if the request is not a valid GET request for /computer
                    response_headers = "HTTP/1.1 404 Not Found\r\nContent-Length: 0\r\n\r\n"
                    client_socket.sendall(response_headers.encode())
            else:
                # Respond with a 401 Unauthorized error if the credentials are invalid
                response_headers = "HTTP/1.1 401 Unauthorized\r\nContent-Length: 0\r\nWWW-Authenticate: Basic realm=\"Restricted\"\r\n\r\n"
                client_socket.sendall(response_headers.encode())
        else:
            # Respond with a 401 Unauthorized error if the Authorization header is missing
            response_headers = "HTTP/1.1 401 Unauthorized\r\nContent-Length: 0\r\nWWW-Authenticate: Basic realm=\"Restricted\"\r\n\r\n"
            client_socket.sendall(response_headers.encode())

        client_socket.close()


if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(WebServer)
