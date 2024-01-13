import os
import sys
from ..common import prettyllog
import subprocess





def main():
    prettyllog("ui", "ui", "ui", "new", "000", "ui")
    ign8_ui_port  = os.environ.get("IGN8_UI_PORT", "8000")
    ign8_ui_host = os.environ.get("IGN8_UI_HOST", "ign8.openknowit.com")
    ign8_ui_debug = os.environ.get("IGN8_UI_DEBUG", "True")

    # change to the ui directory
    VIR_ENV = os.environ.get("VIRTUAL_ENV", "/opt/ign8")
    os.chdir(VIR_ENV/ + "/lib/python3.9/site-packages/ign8/ui/project/ignite")

    # run the server
    myserver = subprocess.run(["gunicon", "--bind", ign8_ui_host + ":" + ign8_ui_port, "--workers", "3", "ignite.wsgi -c gunicorn.conf.py --log-level=debug"])
    myserver.wait()
    return 0





    


                          
