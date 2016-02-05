#--coding:utf-8--
#StartPage.py
#Create/Edit file:'../cfg/StartPage.json'
import re
import sys
import json
from __tmpl__ import cfgFile
from __tmpl__ import Prompt

class PromptClass(Prompt.ErrPrompt):
    def InitInput(self):
        print ("Please input URL(s), use EOF to finish. \n(CTRL+D. if not work for Windows, try CTRL+Z)")

    def IllegalURL(self):
        """
        For URL with illegal characters
        """
        self.PrintErr("Error: URL include illegal characters!")

def main():
    prompt = PromptClass()
    cfgfile = cfgFile.cfgFile()
    content = cfgfile.InitFile('StartPage.json', 'cfg', TransferredMeaning = True, Prompt = True)
    if not cfgfile:
        prompt.Exit()
        sys.exit(False)
    if content == '':
        URL = []
    else:
        prompt.PrintErr("For Edit mode, only append URLs is allowed. Delete need to be done by yourself.")
        URL = json.loads(content)
        prompt.PrintErr("URLs:")
        map(prompt.PrintErr, URL)

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
    cfgfile.SaveFile()
    cfgfile.CloseFile()

    return

if __name__ == '__main__':
    main()
else:
    raise EnvironmentError("Please do not import this script as a module!")

