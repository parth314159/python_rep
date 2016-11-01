class FileHandling:

    def __init__(self, ofilename='output.txt'):
        self.ofilename = ofilename
        self.ofw = open(ofilename, "w")
        self.ofw.close()

    def log_msg(self, msg):
        with open(self.ofilename, "a") as self.ofw:
            self.ofw.write(msg + "\n")
