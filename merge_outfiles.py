### run initial -  python2 index.py  wiki-search-small.xml outfile

import heapq

fps = []
heap = []

for i in range(1, 11):
    curr_file = "outfiles/outfiles" + str(i) + ".txt"
    f = open(curr_file, 'r')
    fps.append(f)

for i, fp in enumerate(fps):
    line = fp.readline()
    if(line == ""):
        continue
    line = line.split("\n")[0]
    line = line.split(" ")
    line.insert(1, i)
    # print(line)
    heapq.heappush(heap, line)
    # print(str(i) + " "  + str(token) + " " + str(postings) )
    # fp.close()

fin_inv = open("outfiles/inv_outfile.txt", "w")

while(len(heap) > 0):
    top = heapq.heappop(heap)
    print(top , "poptop")
    line = fps[top[1]].readline()
    if line:
        line = line.split("\n")[0]
        line = line.split(" ")
        line.insert(1, top[1])        
        # print(str(top[1]) + "Here")
        heapq.heappush(heap, line)        
    while(len(heap) > 0 and heap[0][0] == top[0]):
        now = heapq.heappop(heap)
        # print(now)
        top[2] = top[2] +  now[2]
        print (now, "popback")
        line = fps[now[1]].readline()
        if line:
            line = line.split("\n")[0]
            line = line.split(" ")
            line.insert(1, now[1])        
            # print(str(top[1]) + "Here")
            heapq.heappush(heap, line)         
        # print(top)
    fin_inv.write(top[0] + " " + top[2] + "\n")
fin_inv.close()
    # print(top)

for fp in fps:
    fp.close()