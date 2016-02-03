#--coding:utf-8--
#__common__code__.py
#Create a file in $cfg path
import re
import os
from __tmpl__ import Prompt

class PromptClass(Prompt.ErrPrompt):
    def CreateFileFail(self):
        self.PrintErr ("Error: Fail to create file!")

def GetPath(name): # Name is a the name of part in this project file structure, like "cfg"
    """
    Return string: realpath of part in this project file structure
    Sample of name: "cfg", "$cfg"
    [\W] char will not be considered.
    """
    name = re.sub(r'[\W]', '', name)
    pwd = os.path.realpath(os.getcwd())
    os.chdir(os.path.pardir)
    os.chdir(os.path.curdir + os.path.sep + name.lower())
    path = os.path.realpath(os.getcwd())
    os.chdir(pwd)
    
    return path

def CreateFile(name, path, TransferredMeaning = False, Prompt = False, Force = False):
    """
    Arguments:
        name is the name of file
        path is the $path(in project) or relative path or realpath.
        TransferredMeaning will make function treat 'path' as a special name for part in project, resolve by GetPath()
        Prompt is True if you want ask user to confirm Overwrite or not. return None if user deny
        Force is force create without prompt. May failed due to unexpected reason, like path error or file system error.
    Specifcaly return None if False for Prompt and Force and file exists.
    return a file object if success, or None if failed
    """
    prompt = PromptClass()
    if TransferredMeaning:
        path = GetPath(path)
    else:
        path = os.path.readpath(path)

    if Force:
        return open(path + os.path.sep + name, 'wb')

    if os.path.exists(path + os.path.sep + name):
        if not Prompt:
            return None
        if not prompt.FileExist():
            prompt.CreateFileFail()
            return None
    return open(path + os.path.sep + name, 'wb')

if __name__ == '__main__':
    raise EnvironmentError("DO NOT DIRECTLY RUN THIS SCRIPT!")

