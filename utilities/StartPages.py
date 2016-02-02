#--coding:utf-8--
#StartPage.py
#Create/Edit file:'../cfg/StartPage.json'
import os
import re
import sys
import json
from __common__code__ import CreateFile
from __tmpl__ import Prompt

class PromptClass(Prompt.ErrPrompt):
    def InitInput(self):
        print ("Please input URL(s), use EOF to finish. \n(CTRL+D. if not work for Windows, try CTRL+Z)")

def main():
    prompt = PromptClass()
    cfgfile = CreateFile('StartPage.json', 'cfg', TransferredMeaning = True, Prompt = True)
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

