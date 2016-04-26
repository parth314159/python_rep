class FileHandling:

    def __init__(self, filename='input.txt', ofilename='output.txt'):
        self.filename = filename
        self.ofilename = ofilename
        self.fw = open(filename, "r")
        self.ofw = open(ofilename, "w")
        self.ofw.close()

    def log_msg(self, msg):
        with open(self.ofilename, "a") as self.ofw:
            self.ofw.write(msg + "\n")

    def read(self):
        return self.fw.readline()

    def __del__(self):
        self.fw.close()