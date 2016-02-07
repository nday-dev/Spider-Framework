#--coding:utf-8--
#Extractor
import re
import functools
import chardet # Required

class Extractor(object):
    def __init__(self, Method = None, Template = ""):
        """
        Method can be cumstomed or selected from a list of members:
        A string with its name is also allowed (using eval)
        List:
            ReExtractor(self, content)
        Template is the pattern that methods uses
        """
        self.DefaultTemplate = Template
        if isinstance(Method, basestring):
            self.Extract = eval('self.' + Method)
        else:
            self.Extract = Method

    def ChangeMethod(self, Method = None):
        """
        Use this function to reset the method of self.Extract after initialization.
        Method Default = self.Extract
        List of methods available:
            self.ReExtractor
        """
        if Method:
            self.Extract = Method

    def ChangeTemplate(self, Template = None):
        """
        Use this function to reset the value of sle.DefaultTemplate after initialization
        Template Default = self.DefaultTemplate
        """
        if Template:
            self.DefaultTemplate = Template
    
    def encode(self, content, decoding = None, encoding = None):
        try:
            if not isinstance(content, unicode):
                if decoding == None:
                    decoding = chardet.detect(content).get('encoding', 'utf-8')
                content = content.decode(decoding)
            if encoding == None:
                return content
            return content.encode(encoding)
        except ValueError:
            return content
    
    def _ReFind(self, Pattern, Content, group = 0, default = ''):
        """
        Pattern is instance of basestring, a legal regular expression
            or re._pattern_type object, generated by re.compile
        Content is instance of basingstring, the text
        group is int, the group in regular expression.
        default is what function will return when nothing is find

        Exception:
            AttributeError: pattern is not either of the legal type
        """
        try:
            if isinstance(Pattern, basestring):
                return re.search(Pattern, Content).group(group)
            elif isinstance(Pattern, re._pattern_type):
                return Pattern.search(Content).group(group)
        except AttributeError:
            return default

        raise AttributeError("Need a pattern object or a regular expression!")
    
    def ReInit(self):
        """
        Package self._ReInit.

        Compile all the regular expressions in self.DefaultTemplate to self._RePattern
        The input should be done by json.load from the file generated by script
        According to type:
            instance of basestring: re.compile(value)
            list/tuple: map(re.compile, value)
            dict: self._ReInit(value)

        Exception:
            TypeError: Format of RegularExpression illegal
        """
        self._RePattern = self._ReInit()

    def _ReInit(self, RegularExpression = None):
        """
        Practice of self.ReInit.
        Use recurrence
        RegularExpression Default = self.DefaultTemplate
        """
        if RegularExpression == None:
            RegularExpression = self.DefaultTemplate
        Pattern = {}
        for item in RegularExpression.iteritems():
            key, value = item
            if isinstance(value, basestring):
                Pattern[key] = re.compile(self.encode(value))
            elif isinstance(value, list) or isinstance(value, tuple):
                Pattern[key] = map(lambda(x): x[key], # Get the result
                        map(self._ReInit, # Recurrence to deal with multi-possible-type data
                            map(lambda(x): {key: x}, value))) # Pack the data so is iterable with .iteritems()
            elif isinstance(value, dict):
                Pattern[key] = self._ReInit(value)
            else:
                raise TypeError ("Unexpected Pattern re value type!")

        return Pattern

    def ReExtractor(self, content):
        """
        Package of self._ReExtractor.

        According to self._RePattern (Done by self.ReInit) to give all matches
        following same structure as self.ReInit.
        The input should be instance of basestring
        According to type:
            instance of re._pattern_type: self._ReFind(value, content, group = 1)
            list/tuple: map(functools.partial(self._ReExtractor, Pattern = value[1]), value[0].findall(content))
            dict: self._ReExtractor(self._ReFind(value['InfoRange'], content, group = 1), {key: value['Pattern']})[key]

        Exception:
            KeyError: Unexpected format for dict!
            TypeError: Unexpected value type!
        """
        self._ReExtractor(content)

    def _ReExtractor(self, content, Pattern = None):
        """
        Practice of self.ReExtractor.
        Use recurrence
        Pattern Default = self._RePattern
        """
        if Pattern == None:
            Pattern = self._RePattern
        Info = {}
        for item in Pattern.iteritems():
            key, value = item
            if isinstance(value, re._pattern_type):
                Info[key] = self._ReFind(value, content, group = 1)
            elif isinstance(value, list) or isinstance(value, tuple):
                Info[key] = map(lambda(x): x[key], # Get result from pack
                        map(functools.partial(self._ReExtractor, Pattern = value[1]), # Recurrence
                            map(lambda(x): {key: x}, value[0].findall(content)))) # Pack to pass '.iteritems()'
            elif isinstance(value, dict):
                try:
                    Info[key] = self._ReExtractor(self._ReFind(value['InfoRange'], content, group = 1),
                            {key: value['Pattern']})[key]
                except KeyError:
                    Info[key] = self._ReExtractor(content, value) # For Recurrence from list
            else:
                raise TypeError ("Unexpected value type!")

        return Info

if __name__ == '__main__':
    raise EnvironmentError("DO NOT DIRECTLY RUN THIS TEMPLATE!")
