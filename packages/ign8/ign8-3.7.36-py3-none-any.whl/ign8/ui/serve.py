import os
import sys
from ..common import prettyllog
import subprocess





def main():
    prettyllog("ui", "ui", "ui", "new", "000", "ui")
    ign8_ui_port  = os.environ.get("IGN8_UI_PORT", "8000")
    ign8_ui_host = os.environ.get("IGN8_UI_HOST", "ign8.openknowit.com")
    ign8_ui_debug = os.environ.get("IGN8_UI_DEBUG", "True")


    


                          
