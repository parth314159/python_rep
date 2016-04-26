import itertools
class FileHandling:

    def __init__(self, filename='4_input.txt', ofilename='4_output.txt'):
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

def char_or(t):
    cell = t[0]
    #print(cell)
    s = cell[1]
    ans = list('L' * len(s))
    #print(ans)
    for i in t:
        st = i[1]
        for j in range(len(s)):
            if ans[j]=="L" and st[j] == "L":
                ans[j] = "L"
            else:
                ans[j] = "G"
    return ''.join(map(str, ans))



def give_out(st,c):
    temp = st
    l = len(st)
    for i in range(c-1):
        ans = ""
        for j in range(len(st)):
            if st[j] == 'G':
                ans += 'G'*l
            else:
                ans += temp
        st = ans
    return st

f = FileHandling()
_size = int(f.read())
for ind in range(_size):
    line = f.read()
    sl = line.split(" ")
    k = int(sl[0])
    c = int(sl[1])
    s = int(sl[2])

    lst = list(itertools.product(['G', 'L'], repeat=(k)))
    in_lst = []
    out_lst = []
    n_gl = []
    comb =[[x,""] for x in range(k**c)]
    for i in range(len(lst)):
        c_s = ''.join(map(str, lst[i]))
        #print(c_s)
        in_lst.append(c_s)
        n_gl.append((c_s.count('G'),c_s.count('L')))
        ans = give_out(c_s,c)
        out_lst.append(ans)
        #print(ans)
        for k in range(len(ans)):
            cm = comb[k]
            cm[1] += ans[k]
    #print(comb)

    final_lst = list(itertools.combinations(comb, s))
    #print(final_lst)
    done = False
    write = []
    for _i in final_lst:
        exp = "G"*(len(lst)-1)+"L"
        #print(exp)
        ans_final = char_or(_i)
        #print(ans_final)
        if ans_final == exp:
            for j in _i:
                print("ans",j)
                write.append(j[0]+1)
                done = True
        if done:
            break
    if not done:
        write.append("Impossible")
    ex = ' '.join(map(str, write))
    f.log_msg("Case #{}:".format(ind+1)+ex)