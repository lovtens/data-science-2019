#2014000082 구희강

import itertools
import sys


def scanData(data,minSup):
    level = 1
    # value to return 
    ret = []
    lenData = len(data)
    candidates = []

    # create level 1 candidates  
    for transaction in data:
        for item in transaction:
            if [item] not in candidates:
                candidates.append([item])
    candidates.sort()
    # calculate support value
    count = []
    for i in candidates:
        count.append(counts(i,data))
    for i in range(len(count)):
        count[i] = count[i]/lenData*100
        # pruning marking
        if count[i]<minSup:
            candidates[i] = []
    # pruning
    candidates = list(filter(lambda a: a != [], candidates))

    while True:        
        # create new candidates of upper level
        tmp = candidates
        candidates = []
        for i in range(len(tmp)):
            for j in range(i+1,len(tmp)):
                l1 = tmp[i]
                l2 = tmp[j]
                if matchK(level-1,l1,l2):
                    rule = list(set(l1 + l2))
                    rule.sort()
                    candidates.append(rule)
        # calculate support value
        count = []
        for i in candidates:
            count.append(counts(i,data))
        for i in range(len(count)):
            count[i] = count[i]/lenData*100
            # pruning marking
            if count[i]<minSup:
                candidates[i] = []
        # pruning
        candidates = list(filter(lambda a: a != [], candidates))
    
        if len(candidates) == 0 :
            break
        level = level + 1
        ret.append(write(candidates,data))
    
    # return output data
    return ret


def matchK(k,l1,l2):
    if k==0:
        return True
    for i in range(k):
        if l1[i] != l2[i]:
            return False
    return True


def counts(candidates,data):
    count = 0
    for transaction in data:
        if set(candidates).issubset(set(transaction)):
            count = count + 1
    return count


def sublists(data): 
    ret = []
    for i in range(1,len(data)):
        ret = ret + list(itertools.combinations(data,i))
    for i in range(len(ret)):
        ret[i] = set(ret[i])
        
    return ret


def getSup(items,data):
    return counts(items,data)/len(data)*100


def getConf(items,x,data):
    return counts(items,data)/counts(x,data)*100


def write(candidates,data):
    line = []
    for c in candidates:
        sublist = sublists(c)
        for sub in sublist:
            item = set(sub)
            asso = set(c) - set(sub)
            sup = getSup(c,data)
            conf = getConf(c,item,data)        
            line.append(str(item)+'\t'+str(asso)+'\t'+format(sup,".2f")+'\t'+format(conf,".2f"))
    return line


def writeData(data,name_out):
    fout = open(name_out,'w+')
    tmp = []
    for i in range(len(data)):
        tmp.append('\n'.join(data[i]))
    fout.write('\n'.join(tmp))
    fout.close()


def readData(name_in):
    fin = open(name_in,'r')
    data = []
    while True:
        tmp = fin.readline()
        if not tmp : 
            break
        tmp = list(tmp.strip('\n').split('\t'))
        for i in range(len(tmp)):
            tmp[i] = int(tmp[i])
        tmp.sort()
        data.append(tmp)
    fin.close()
    return data 


if __name__ == "__main__":
    minSup = int(sys.argv[1])
    name_in = sys.argv[2]
    name_out = sys.argv[3]

    # read data from input file
    data_in = readData(name_in)
    # create data
    data_out = scanData(data_in,minSup)
    # write output file 
    writeData(data_out,name_out)

    
