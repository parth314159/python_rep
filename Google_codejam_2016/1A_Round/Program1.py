import itertools
import math
from FileHandling import FileHandling


f = FileHandling("1_input.txt","1_output.txt")
_size = int(f.read())
for ind in range(_size):
    line = f.read()[:-1]
    print(line)
    ans = ""
    for i in range(len(line)):
        if ans!="" and ans[0] > line[i]:
            ans += line[i]
        else:
            ans = line[i] + ans
    print(ans)

    f.log_msg("case #{}: ".format(ind+1)+ans)