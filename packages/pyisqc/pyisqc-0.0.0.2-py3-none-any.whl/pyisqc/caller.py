import os 
import shutil


class Caller():

    def __init__(self):
        self.isqcdir = '/home/hengyue/software/isqc'
        self.bin = os.path.join(self.isqcdir,"isqc")

    def rcmd(self,rcmd):
        cmd = f"{self.bin} {rcmd}"
        stdout = os.popen(cmd).read()
        return stdout
    
    @staticmethod
    def is_valid_isqc(binPath:str):
         cmd = f"{binPath} -V"
         stdout = os.popen(cmd).read().strip()
         return stdout[:12] == "isQ Compiler"


    
    @classmethod
    def _search_isqc_by_which(cls):
        isqc = shutil.which("isqc")
        if isqc is not None and cls.is_valid_isqc(isqc):
            return isqc 
        return None

