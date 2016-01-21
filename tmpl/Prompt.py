#--coding:utf-8--
#Platform

class BasePrompt(object):
    pass

class ErrPrompt(BasePrompt):
    """
    Define some of Err Prompts
    Usually print to sys.stderr
    """
    def PrintErr(self, content):
        import sys
        """
        Automous write content to sys.stderr and add '\n' to the end
        """
        sys.stderr.write(content + '\n')
        sys.stderr.flush()

    def IllegalURL(self):
        """
        For URL with illegal characters
        """
        self.PrintErr("Error: URL include illegal characters!")

    def FileExist(self, File = "File"):
        """
        return True if want to replace, and False for the other
        """
        self.PrintErr("Warning: '%s' already exists, replace?(y/n)" %(Files))
        tmp = raw_input()
        if tmp == 'y' or tmp == 'Y':
            return True
        return False
    
    def Exit(self):
        self.PrintErr("Info: Terminated")

if __name__ == '__main__':
    raise EnvironmentError ("DO NOT DIRECTLY RUN THIS TEMPLATE!")
