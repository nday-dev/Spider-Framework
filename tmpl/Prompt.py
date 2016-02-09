#--coding:utf-8--
#Platform

class BasePrompt(object):
    pass

class ErrPrompt(BasePrompt):
    """
    Define some of Err Prompts
    Usually print to sys.stderr
    """
    @staticmethod
    def PrintErr(content):
        import sys
        """
        Automous write content to sys.stderr and add '\n' to the end
        """
        sys.stderr.write(content + '\n')
        sys.stderr.flush()
    
    def Exit(self):
        self.PrintErr("Info: Terminated")

if __name__ == '__main__':
    raise EnvironmentError ("DO NOT DIRECTLY RUN THIS TEMPLATE!")
