# 2014000082 구희강
import sys
import math
import copy
import operator


def readData(name):
    fin = open(name,'r')
    data = []
    while True:
        tmp = fin.readline()
        if not tmp:
            break
        tmp = list(tmp.strip('\n').split('\t'))
        for i in range(len(tmp)):
            tmp[i] = float(tmp[i])
        tmp.append(0)
        data.append(tmp)
    fin.close()
    return data


def sortCluster(data):
    cluster_count = {}
    for i in range(len(data)):
        if int(data[i][-1]) == -1: # outliers
            continue
        if not int(data[i][-1]) in cluster_count:
            cluster_count[int(data[i][-1])] = 1
        else:
            cluster_count[int(data[i][-1])] += 1 
    sorted_cluster = sorted(cluster_count.items(),key=operator.itemgetter(1),reverse=True)
    sorted_cluster = sorted_cluster[:n]
    return sorted_cluster


def writeCluster(data,num,name):
    tmp = []
    # ‘input#_cluster_0.txt’ 
    fout = open(name,'w+')
    for point in data:
        if point[-1] == num:
            tmp.append(str(int(point[0]))) # id
    fout.write('\n'.join(tmp))
    fout.close()


def distance(p1,p2):
    return math.sqrt((p1[1]-p2[1])**2 + (p1[2]-p2[2])**2)

    
def findNeighbors(data,point,eps):
    neighbors = []
    for x in data:
        if distance(point,x) < eps:
            neighbors.append(int(x[0])) # save id 
    return neighbors


def DBSCAN(data,eps,minPts):
    cluster_label = 0
    for i, point in enumerate(data):
        if point[-1] == 0:
            neighbors = findNeighbors(data,point,eps)
            if len(neighbors) < minPts:
                data[i][-1] = -1
            else:
                cluster_label += 1
                # cluster
                data[i][-1] = cluster_label # set cluster label
                j = 0                
                while j < len(neighbors):
                    tmp = neighbors[j] # list [id,x,y,cluster]
                    if data[tmp][-1] == -1:
                        data[tmp][-1] = cluster_label
                    elif data[tmp][-1] == 0:
                        data[tmp][-1] = cluster_label
                        tmp_neighbors = findNeighbors(data,data[tmp],eps)
                        if len(tmp_neighbors) >= minPts: # is core point 
                            for x in tmp_neighbors:
                                if x not in neighbors:
                                    neighbors.append(x)
                    j += 1
                   

if __name__ == "__main__":
    input_file = sys.argv[1]
    n = int(sys.argv[2])
    eps = int(sys.argv[3])
    minPts = int(sys.argv[4])

    data = readData(input_file)
    DBSCAN(data,eps,minPts)    
    sorted_cluster = sortCluster(data)

    for i,(num,_) in enumerate(sorted_cluster):
        # ‘input#_cluster_0.txt’ 
        name = input_file.split('.')[0] + "_cluster_{}.txt".format(i)
        writeCluster(data,num,name)
    print("done")