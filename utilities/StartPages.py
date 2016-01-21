#--coding:utf-8--
#StartPage.py
#Create/Edit file:'../cfg/StartPage.json'
import os
import re
import sys
import json
from __tmpl__ import *

class PromptClass(Prompt.ErrPrompt):
    def InitInput(self):
        print ("Please input URL(s), use EOF to finish. \n(CTRL+D. if not work for Windows, try CTRL+Z)")

class PlatformClass(Platform.BasePlatform):
    class OSX(Platform.BasePlatform.System):
        pass

def main():
    prompt = PromptClass()
    pwd = os.getcwd()
    os.chdir(os.path.pardir)
    os.chdir(os.path.curdir + os.path.sep + 'cfg')
    cfg = os.getcwd()
    os.chdir(pwd)

    if os.path.exists(os.path.realpath(cfg + os.path.sep + 'StartPage.json')):
        if not prompt.FileExist():
            prompt.Exit()
            sys.exit(False)
    cfgfile = open(os.path.realpath(cfg + os.path.sep + r'StartPage.json'), 'wb')
    URL = []
    IllegalChars = r"[^ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789\-\.\_\~\:\/\?\#\[\]\@\!\$\&\'\(\)\*\+\,\;\=]"
    try:
        prompt.InitInput()
        while True:
            tmp = raw_input()
            if re.search(IllegalChars, tmp):
                prompt.IllegalURL()
            URL.append(tmp)
    except EOFError:
        prompt.Exit()
    json.dump(URL, cfgfile)
    cfgfile.close()

    return

if __name__ == '__main__':
    main()
else:
    raise EnvironmentError("Please do not import this script as a module!")

