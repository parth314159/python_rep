class FileHandling:

    def __init__(self, filename='2_input.txt', ofilename='2_output.txt'):
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

def st_inv(st):
    ans = ""
    for i in range(len(st)):
        if st[i] == "+":
            ans += "-"
        else:
            ans += "+"
    return ans

def process_flip(st):
    flip_counter =0
    if st[len(st)-1] == "-":
        if st[0] == "+":
            loc = st.find("-")
            st = "-"*loc + st[loc:]
            # flip whole bunch
            st = st_inv(st)
            flip_counter +=2
            print(st,"=",flip_counter)
        else:
            #flip whole bunch
            st = st_inv(st)
            flip_counter += 1
            print(st,"=",flip_counter)
        flip_counter += process_flip(st)
    else:
        loc = st.rfind("-")
        print("loc",loc)
        if loc != -1:
            s = st[:loc+1]
            print("str",s)
            flip_counter += process_flip(s)
    return flip_counter


f = FileHandling()
_size = int(f.read())
for i in range(_size):
    line = f.read()[:-1]
    in_st = line
    print(line,"=0")
    flip_c= process_flip(line)
    print("Final answer", flip_c)
    f.log_msg("Case #{}:".format(i+1)+" "+str(flip_c))