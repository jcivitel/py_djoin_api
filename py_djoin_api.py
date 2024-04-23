import json
import subprocess
import sys
import threading

import servicemanager
import win32event
import win32service
import win32serviceutil
from flask import Flask, jsonify, request


class PythonService(win32serviceutil.ServiceFramework):
    _svc_name_ = "py_djoin_api"
    _svc_display_name_ = "Python Djoin API"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.app_process = None

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        if self.app_process:
            self.app_process.terminate()
            self.app_process.join()

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def main(self):

        app = Flask(__name__)

        def get_computer_info(computer_name):
            try:
                # PowerShell-Befehl zum Abrufen von Computerinformationen
                powershell_command = f"Get-WmiObject Win32_ComputerSystem -ComputerName {computer_name} | ConvertTo-Json"

                # PowerShell-Befehl ausführen und Ergebnis abrufen
                result = subprocess.run(['powershell', '-Command', powershell_command], capture_output=True, text=True)
                output = result.stdout.strip()

                # JSON-String in ein Python-Dictionary umwandeln
                computer_info = json.loads(output)
                return computer_info
            except Exception as e:
                return {'error': str(e)}

        @app.route('/computer_info', methods=['GET'])
        def computer_info():
            # Computername aus der Query-Parameter der GET-Anfrage erhalten
            computer_name = request.args.get('computer_name')

            if not computer_name:
                return jsonify({'error': 'Missing computer_name parameter'}), 400

            # Computerinformationen abrufen
            computer_info = get_computer_info(computer_name)

            return jsonify(computer_info)

        self.app_process = threading.Thread(target=app.run, kwargs={'debug': True, 'host': '0.0.0.0', 'port': '80'})
        self.app_process.start()
        self.app_process.join()


if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(PythonService)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(PythonService)
