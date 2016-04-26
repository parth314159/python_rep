import itertools
from FileHandling import FileHandling


f = FileHandling("2_input.txt","2_output.txt")
_size = int(f.read())
for ind1 in range(_size):
    _size2 = int(f.read())
    list2 = []
    for ind2 in range(2*_size2-1):
        line = f.read()[:-1]
        sl = line.split(" ")
        intsl = list(map(int, sl))
        if len(intsl) == _size2:
            #if list2.index()
            list2.append(intsl)
            list2.sort()
        print(list2)
    #f.log_msg(str_tp+" "+' '.join(map(str, tpans[1])))