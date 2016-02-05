#--coding:utf-8--
#ReGenerator.py
#Create/Edit file:'../cfg/ReInfoExtract.json'
import re
import sys
import json
from __tmpl__ import cfgFile
from __tmpl__ import Prompt

class PromptClass(Prompt.ErrPrompt):
    def InitPrompt(self):
        self.PrintErr("Input the regular expressions directly\n" +
                "Use EOF to exit\n" + 
                "Use ? to ask for help\n" +
                "(Try CTRL+D for OS X/ Linux, CTRL+Z for Windows)\n")
    def HelpPrompt(self):
        self.PrintErr("Help:\n" + 
                "Usually the regular expression will only match the first matched result in the doamin.\n" + 
                "Use > to make a nested structure, narrow the domain, means search in a domain which is matched in parent range.\n" +
                "    >Name will directly enter the domain instead of input after prompt.\n" + 
                "Use | to make a parallel structure, map to parallel domains, means apply same setting for all strings matched in domain.\n" + 
                "Use : to start name of a RE match and Regular Expression for it.\n" + 
                "Use l to list all items under this domain.\n" +
                "Use s to save all input into file (continuing input mode, auto save when normal quit).\n" + 
                "Use keys to list all keys under this domain.\n" +
                "Use a empty line to ask for pwd.\n" + 
                "Use EOF to exit a nested structure or exit all input process.")

    def EndPrompt(self):
        self.PrintErr("Info: End of the input")

    def EnterDomain(self, domain):
        self.PrintErr("Info: Enter the domain %s" %domain)

    def ExistDomain(self, domain):
        self.PrintErr("Info: Domain %s already exist" %domain)

    def ExitDomain(self, domain):
        self.PrintErr("Info: Exit the domain %s" %domain)

class Generator(object):
    def __init__(self):
        self.prompt = PromptClass()
        self.main()

    def ReInput(self, Prompt = "Please input a legel Regular Expression: "):
        while True:
            try:
                Expression = raw_input(Prompt)
                re.compile(Expression)
                return Expression
            except re.sre_compile.error:
                pass

    def PrintContainer(self, container):
        if not isinstance(container, dict):
            raise TypeError("Unexpected Container Type!")
            return
        print 'Items:'
        for item in container.iteritems():
            self.prompt.PrintErr('{%r: %r}' %item)

    def PrintKeys(self, container):
        if not isinstance(container, dict):
            raise TypeError("Unexpected Container Type!")
            return
        print 'keys:'
        for keys in container.iterkeys():
            self.prompt.PrintErr('%r' %keys)

    def PrintAnyway(self, container):
        self.prompt.PrintErr('%r' %container)

    def FSM(self, domain, pwd, container = None, prompt = None): # Finite-State Machine
        """
        Args:
            domain: instance of basestring, name of the domain
            pwd: current path
            container: usually is a dict created by parent function. Or create by it self and return to parent
            prompt: Should be a object of PromptClass, but could be instance of it if want to modefy. Defaultly PromptClass() (self.prompt)
        Return:
            container type object or a dict with no container arg
        """
        if prompt == None:
            prompt = self.prompt
        pwd = pwd + "['" + domain + "']"
        try:
            if container:
                Re = container
            else:
                Re = {}

            prompt.EnterDomain(domain)
            while True:
                string = raw_input()
                if string == '?':
                    prompt.HelpPrompt()
                elif string == '':
                    prompt.PrintErr(pwd)
                elif string[0] == '>':
                    if len(string) == 1:
                        subdomain = raw_input("Name of Domain: ")
                    else:
                        subdomain = string[1:]

                    try:
                        Re[subdomain]
                        prompt.ExistDomain(subdomain)
                        self.FSM(subdomain, pwd, Re[subdomain])
                    except KeyError:
                        Re[subdomain] = {}
                        subrange = self.ReInput("Range of Domain: ")
                        Re[subdomain]["InfoRange"] = subrange
                        self.FSM(subdomain, pwd, Re[subdomain]["Pattern"])
                elif string == '|':
                    subdomain = self.ReInput("Domain for each match: ")
                    Re = []
                    Re.append(subdomain)
                    Re.append(self.FSM(domain + '<List>', pwd))
                elif string == ':':
                    name = raw_input("Name of the match: ")
                    Re[name] = self.ReInput("Regular Expression of %s:" %name)
                elif string == 'l':
                    try:
                        self.PrintContainer(Re)
                    except TypeError, Info:
                        prompt.PrintErr("%r" %Info)
                        self.PrintAnyway(Re)
                elif string == 's':
                    self.Save()
                elif string == 'keys':
                    try:
                        self.PrintKeys(Re)
                    except TypeError, Info:
                        prompt.PrintErr("%r" %Info)
                        self.PrintAnyway(Re)
                else:
                    prompt.PrintErr("Info: Ignore directly input")
        except EOFError:
            prompt.ExitDomain(domain)

        return Re

    def Save(self):
        json.dump(self.RegularExpression, self.cfgfile)
        self.cfgfile.SaveFile()


    def main(self):
        prompt = PromptClass()
        self.cfgfile = cfgFile.cfgFile()

        content = self.cfgfile.InitFile('ReInfoExtract.json', 'cfg', TransferredMeaning = True, Prompt = True)
        if content == None:
            prompt.Exit()
            sys.exit(False)
        if content == '':
            self.RegularExpression = {}
        else:
            self.RegularExpression = json.loads(content)

        prompt.InitPrompt()
        self.FSM("Golbal", '', container = self.RegularExpression)
        prompt.EndPrompt()
        self.Save()
        self.cfgfile.CloseFile()

if __name__ == '__main__':
    Generator()
else:
    raise EnvironmentError("Please do not import this script as a module!")
