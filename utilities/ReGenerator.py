#--coding:utf-8--
#ReGenerator.py
#Create/Edit file:'../cfg/ReInfoExtract.json'
import re
import sys
import json
from __common__code__ import CreateFile
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
                "Use | to make a parallel structure, map to parallel domains, means apply same setting for all strings matched in domain.\n" + 
                "Use : to start name of a RE match and Regular Expression for it.\n" + 
                "Use a empty line to ask for pwd.\n" + 
                "Use EOF to exit a nested structure or exit all input process.\n")

    def EndPrompt(self):
        self.PrintErr("Info: End of the input")

    def EnterDomain(self, domain):
        self.PrintErr("Info: Enter the domain %s" %domain)

    def ExitDomain(self, domain):
        self.PrintErr("Info: Exit the domain %s" %domain)

def ReInput(Prompt = "Please input a legel Regular Expression: "):
    while True:
        try:
            Expression = raw_input(Prompt)
            re.compile(Expression)
            return Expression
        except re.sre_compile.error:
            pass

def Generator(domain, pwd, prompt = PromptClass()):
    pwd = pwd + "['" + domain + "']"
    try:
        prompt.EnterDomain(domain)
        Re = {}
        while True:
            string = raw_input()
            if string == '?':
                prompt.HelpPrompt()
            elif string == '>':
                subdomain = raw_input("Name of Domain: ")
                subrange = ReInput("Range of Domain: ")
                Re[subdomain] = {}
                Re[subdomain]["InfoRange"] = subrange
                Re[subdomain]["Pattern"] = Generator(subdomain, pwd)
            elif string == '|':
                subdomain = ReInput("Domain for each match: ")
                Re = []
                Re.append(subdomain)
                Re.append(Generator(domain + '<List>', pwd))
            elif string == ':':
                name = raw_input("Name of the match: ")
                Re[name] = ReInput("Regular Expression of %s:" %name)
            elif string == '':
                print pwd
            else:
                prompt.PrintErr("Info: Ignore directly input")
    except EOFError:
        prompt.ExitDomain(domain)

    return Re

def main():
    prompt = PromptClass()
    cfgfile = CreateFile('ReInfoExtract.json', 'cfg', TransferredMeaning = True, Prompt = True)
    if not cfgfile:
        prompt.Exit()
        sys.exit(False)

    RegularExpression = {}
    prompt.InitPrompt()
    RegularExpression = Generator("Golbal", '')
    prompt.EndPrompt()
    json.dump(RegularExpression, cfgfile)

if __name__ == '__main__':
    main()
else:
    raise EnvironmentError("Please do not import this script as a module!")
