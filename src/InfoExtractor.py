#--coding:utf-8--
#InfoExtractor.py
import json
from __tmpl__ import cfgFile
from __tmpl__ import Extractor

class Extract(object):
    """Multiprocessing safe"""
    def __init__(self):
        """
        Load cfg File
        Use ReExtractor
        Initialize it
        """
        cfg = cfgFile.cfgFileIn()
        cfg.InitFile('ReInfoExtract.json', 'cfg', TransferredMeaning = True)
        self.Extract = Extractor.Extractor("ReExtractor",json.load(cfg))
        self.Extract.Init()

    def Extract(self, content):
        """return self.Extract.Extract(content)"""
        return self.Extract.Extract(content)

if __name__ == '__main__':
    raise EnvironmentError("DO NOT DIRECTLY RUN THIS PART!")
