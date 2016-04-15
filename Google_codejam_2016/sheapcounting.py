class FileHandling:

    def __init__(self, filename='1_input.txt', ofilename='1_output.txt'):
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



f = FileHandling()
_size = int(f.read())
for i in range(_size):
    num = int(f.read())
    mul = 1
    f_l = [0 for x in range(10)]
    ans = 0
    while f_l.count(0) != 0:
        n = num * mul
        if n == 0:
            ans = "INSOMNIA"
            break
        else:
            ans = n
        #print("num:",n)
        while n:
            digit = n % 10
            # do whatever with digit
            f_l[digit] = 1
            # remove last digit from number (as integer)
            n //= 10
        mul += 1
    f.log_msg("Case #{}:".format(i+1)+" "+str(ans))