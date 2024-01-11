import os
import shutil

class File:
    def __init__(self, filename):
        self.filename = filename

    def name(self):
        filename = os.path.basename(self.filename)
        partes = filename.rsplit('.')

        if len(partes) == 0:
            return ''
        
        return partes[0]        

    def extension(self):
        filename = os.path.basename(self.filename)
        partes = filename.rsplit('.', 1)

        if len(partes) == 0:
            return ''

        return partes[len(partes)-1]

    def dirname(self):
        return os.path.dirname(self.filename)

    def basename(self):
        return os.path.basename(self.filename)

    def move(self, to):
        shutil.move(self.filename, to)

        return self

    def remove(self):
        os.remove(self.filename)

        return self

    def open(self, mode = 'a'):
        self.h = open(self.filename, mode)

    def close(self):
        self.h.close()
        self.h = None

    def write(self, content):
        self.open()
        self.h.write(content)
        self.close()

        return self

    def readall(self):
        self.open('r')
        text = self.h.read()
        self.close()

        return text

    def clear(self):
        self.open('w')
        self.close()

    def writeLine(self, content):
        self.open()
        self.h.write(content + '\n')
        self.close()
    
    @staticmethod
    def create(filename):
        file = File(filename)
        file.clear()
        return file
