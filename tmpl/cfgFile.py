#--coding:utf-8--
#__common__code__.py
#Create a file in $cfg path
import re
import os
import shutil
import Prompt

class PromptClass(Prompt.ErrPrompt):
    def CreateFileFail(self):
        self.PrintErr ("Error: Fail to create file!")

    def FileExist(self, File = "File"):
        """
        return type: instance of basestring
        return value:
            c if user prefer createing new one
            e if user prefer editing mode
            q if user want to quit the action
        """
        self.PrintErr("Warning: '%s' already exists, please choose the action:" %(File) +
                "\n(c)over/ (e)dit/ (q)uit: ")
        tmp = raw_input()
        return tmp[0].lower()

class cfgFile(object):
    def write(self, content):
        self.File.write(content)

    def __del__(self):
        try:
            self.CloseFile()
        except AttributeError:
            pass

    def GetPath(self, name): # Name is a the name of part in this project file structure, like "cfg"
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
    
    def InitFile(self, name, path, TransferredMeaning = False, Prompt = False, Force = False):
        """
        Arguments:
            name is the name of file
            path is the $path(in project) or relative path or realpath.
            TransferredMeaning will make function treat 'path' as a special name for part in project, resolve by self.GetPath()
            Prompt is True if you want ask user to confirm Overwrite or not. return None if user deny
            Force is force create without prompt. May failed due to unexpected reason, like path error or file system error.
        Specifcaly return None if False for Prompt and Force and file exists.
        Set self.File as the file operation ID
        return file content if success, or None if failed
        """
        prompt = PromptClass()
        self.name = name
        if TransferredMeaning:
            self.path = self.GetPath(path)
        else:
            self.path = os.path.readpath(path)
        self.swp = '.' + self.name + '.swp'
        try:
            shutil.copyfile(self.path + os.path.sep + self.name, self.path + os.path.sep + self.swp)
        except IOError:
            pass

        self.FileFunction = lambda(x): open(self.path + os.path.sep + self.swp, x)
        if Force:
            self.File = self.FileFunction('wb')
            return ''

        if os.path.exists(self.path + os.path.sep + self.name):
            if not Prompt:
                return None
            mode = prompt.FileExist()
            if mode == 'c':
                self.File = self.FileFunction('wb')
                return ''
            elif mode == 'e':
                File = self.FileFunction('rb')
                content = File.read()
                File.close()
                self.File = self.FileFunction('wb')
                return content
            elif mode == 'q':
                prompt.CreateFileFail()
                return None
            else:
                prompt.PrintErr("Error: Cannot identify the choice, action failed")
                return None
        else:
            self.File = self.FileFunction('wb')
            return ''

    def SaveFile(self):
        self.File.flush()
        shutil.copyfile(self.path + os.path.sep + self.swp, self.path + os.path.sep + self.name)

    def CloseFile(self):
        self.File.close()
        os.rename(self.path + os.path.sep + self.swp, self.path + os.path.sep + self.name)

if __name__ == '__main__':
    raise EnvironmentError("DO NOT DIRECTLY RUN THIS SCRIPT!")

