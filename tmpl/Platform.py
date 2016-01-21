#--coding:utf-8--
#Platform

class BasePlatform(object):
    """
    A template for codes which are dependent on platform, whatever shell type or system type.
    Redefine members to modify the function.
    """
    def __init__(self, shell = False):
        if shell:
            if os.name == 'posix':
                return self.Posix()
            if os.name == 'nt':
                return self.NT()
            return None
        else:
            import platform
            if platform.system()[:6] == 'Darwin':
                return self.OSX()
            if platform.system()[:5] == 'Linux':
                return self.Linux()
            if platform.system()[:7] == 'Windows':
                return self.Windows()
            if platform.system()[:6] == 'CYGWIN':
                return self.Cygwin()
            return None
        return None

    class Common(object):
        """
        Redefine members here for those which will be inherited to all shells and systems.
        """
        pass

    class Shell(Common):
        """
        Redefine members here for those which will be inherited to all shells.
        """
        pass

    class System(Common):
        """
        Redefine members here for those which will be inherited to all systems.
        """
        pass

    class Posix(Shell):
        pass

    class NT(Shell):
        pass

    class OSX(System):
        pass

    class Linux(System):
        pass

    class Windows(System):
        pass

    class Cygwin(System):
        pass

if __name__ == '__main__':
    raise EnvironmentError ("DO NOT DIRECTLY RUN THIS TEMPLATE!")
