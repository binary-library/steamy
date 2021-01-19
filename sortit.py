import random

randomlist = {}

for i in range(0,20):
    n = random.randint(1,30)
    x = str(random.randint(1,30))
    randomlist[x] = n 

def selection_sort(l):
    sorted_l = []
    for i in range(0, len(l)):
        smallest_index = l.index(min(l))
        sorted_l.append(l[smallest_index])
        del l[smallest_index]
    return sorted_l

print(list(map(lambda x: x[0], randomlist)))
print(randomlist)
print(selection_sort(list(map(lambda x: [x[1], x[0]] , randomlist.items()))))
print(selection_sort( randomlist.items() ))