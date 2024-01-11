import os
import shutil
import uuid

class Directory:
    DIR = 'dir'
    FILES = 'files'
    ALL = 'all'

    def __init__(self, path=None):
        self.fullpath = self.__fixPath(path)

    def list(self, type=ALL):
        all = []

        for x in os.listdir(self.fullpath):
            if type == Directory.FILES and os.path.isfile(self.resolve(x)):
                all.append(x)
            elif type == Directory.DIR and os.path.isdir(self.resolve(x)):
                all.append(x)
            elif type == Directory.ALL:
                all.append(x)

        return all

    def resolve(self, path=None):
        if path is None:
            return self.fullpath
        
        path = self.__fixPath(path)
        
        if len(path) == 0:
            return self.fullpath
        elif len(path) > 1 and path[0] == '/':
            path = path[1:]
        elif len(path) == 1 and path[0] == '/':
            return self.fullpath
        
        return "%s/%s" % (self.fullpath, path)

    def exist(self, filename):
        return os.path.exists(self.resolve(filename))

    def subdir(self, name):
        return Directory(self.resolve(name))

    def moveFile(self, filename, dir):
        os.rename(self.resolve(filename), dir)

    def remove(self):
        try:
            # os.rmdir(self.fullpath)
            shutil.rmtree(self.fullpath)
        except OSError as e:
            return False, e

        return True, ''

    def createSubDir(self, name):
        return Directory.create(self.resolve(name))

    def existSubDir(self, name):
        return self.exist(name)
    
    def __fixPath(self, path=None):
        if path is None:
            return ""
        
        if len(path) > 1 and path[len(path)-1] == '/':
            path = path[:len(path)-1]
        
        return path

    @staticmethod
    def current():
        return Directory(os.getcwd())

    @staticmethod
    def temporary(path=None):
        current = Directory(Directory.current().resolve(path))
        hex = uuid.uuid4().hex
        return Directory.create(current.resolve(hex))

    @staticmethod
    def create(path, rights=0o755):
        try:
            os.mkdir(path, rights)
        except OSError as e:
            print(e)
            return None
        
        return Directory(path)