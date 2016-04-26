from FileHandling import FileHandling


f = FileHandling("3_input.txt","3_output.txt")
_size = int(f.read())
for ind1 in range(_size):
    _size2 = int(f.read())
    line = f.read()
    num = line.split()
    intlist = list(map(int, num))
    intlist.insert(0,0)
    print(intlist)
    flag = [True for x in range(len(intlist))]
    flag[0] = False

    it_set = []
    final_set = []
    final = 0
    cycle_counter = 0
    #print(flag)
    #for ind2 in range((2**_size2)-1):
    ind_g = 1
    while True:
        if not flag[ind_g]:
            co=flag.count(True)
            if co == 0:
                if final < cycle_counter:
                    final_set = it_set[:]
                    it_set.clear()
                    final = cycle_counter
                #cycle_counter =0
                break;
            else:
                co = flag.index(True)
                ind_g = co
                print(final,cycle_counter)
                print(flag)
                if final < cycle_counter:
                    final_set = it_set[:]
                    it_set.clear()
                    final = cycle_counter
                    cycle_counter = 0
                else:
                    print("temp",it_set)
                    for j in it_set:
                        li1 = intlist[j]
                        li2 = intlist[intlist[j]]
                        if intlist[li1] == li2 and intlist[li2]==li1:
                            print(li1,li2)
                            final += 1
                    it_set.clear()
                    cycle_counter = 0
        flag[ind_g] = False
        it_set.append(ind_g)
        ind_g = intlist[ind_g]

        #c =intlist.count(intlist[ind_g])
        cycle_counter+=1
    #print(flag)
    print("loop",final_set)
    print(final)
    f.log_msg("case #{}: {}".format(ind1+1,final))