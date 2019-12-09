import os
import sys
import json
import collections
from compare import nodeComparison


def getArea(coords):
    [x1, y1, x2, y2] = coords
    return (x2 - x1) * (y2 - y1)

def isIn(c1, c2):
    [x1, y1, x2, y2] = c1
    [x3, y3, x4, y4] = c2
    if x1 >= x3 and x2 <= x4 and y1 >= y3 and y2 <= y4:
        return True
    else:
        return False

def buildGraph(commmands):
    nodes = []
    root = {
        "command": "DrawRect",
        "visible": True,
        "coords": [ 0, 0, 10000, 10000 ],
        "paint": {
        "antiAlias": True,
        "color": [ 255, 153, 153, 153 ],
        "filterQuality": "low"
        },
        "shortDesc": " [0 0 10000 10000]"
    }
    nodes.append(root)
    for command in commmands:
        if command["command"] == "DrawRect" or command["command"] == "DrawTextBlob" or command["command"] == "DrawImageRect" or command["command"] == "DrawRRect" or command["command"] == "DrawPath":
            nodes.append(command)
    edges = [[] for _ in range(len(nodes))]
    for i in range(1, len(nodes)):
        minj = -1
        minArea = 100000000000000
        if nodes[i]["command"] == "DrawRect":
            shortDesc = nodes[i]["shortDesc"]
            shortDesc = shortDesc[2:-1]
            coords1 = list(map(float, shortDesc.split(" ")))
        elif nodes[i]["command"] == "DrawImageRect":
            shortDesc = nodes[i]["shortDesc"]
            shortDesc = shortDesc[2:-1]
            coords1 = list(map(float, shortDesc.split(" ")))
        elif nodes[i]["command"] == "DrawTextBlob":
            shortDesc = nodes[i]["shortDesc"]
            shortDesc = shortDesc[2:-1]
            coords1 = list(map(float, shortDesc.split(" ")))
        elif nodes[i]["command"] == "DrawRRect":
            coords1 = nodes[i]["coords"][0]
        elif nodes[i]["command"] == "DrawPath":
            edges[0].append(i)
            continue
        else:
            continue

        for j in range(i):
            if nodes[j]["command"] == "DrawRect":
                shortDesc = nodes[j]["shortDesc"]
                shortDesc = shortDesc[2:-1]
                coords2 = list(map(float, shortDesc.split(" ")))
            elif nodes[j]["command"] == "DrawImageRect":
                shortDesc = nodes[j]["shortDesc"]
                shortDesc = shortDesc[2:-1]
                coords2 = list(map(float, shortDesc.split(" ")))
            elif nodes[j]["command"] == "DrawTextBlob":
                shortDesc = nodes[j]["shortDesc"]
                shortDesc = shortDesc[2:-1]
                coords2 = list(map(float, shortDesc.split(" ")))
            elif nodes[j]["command"] == "DrawRRect":
                coords2 = nodes[j]["coords"][0]
            else:
                continue
            if isIn(coords1, coords2):
                area = getArea(coords2)
                if area < minArea:
                    minArea = area
                    minj = j

        if minj != -1:
            edges[minj].append(i)
        

    return edges, nodes

def generateKernel(cmds1, cmds2):
    kernel = [[0 for _ in range(len(cmds2))]]
    outfile = "example.txt"
    f = open(outfile, 'w')
    for obj1 in cmds1[1:]:
        line = [0]
        for obj2 in cmds2[1:]:
            try:
                val = nodeComparison(obj1, obj2)
            except Exception as e:
                f.write(json.dumps(obj1))
                f.write('\n')
                f.write(json.dumps(obj2))
                f.write("\n")
                f.write(str(e))
                f.write('\n')
            line.append(val)
        kernel.append(line)
    f.close()
    return kernel
    


    

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("format error!")
        exit(0)
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    outfile = sys.argv[3]
    f = open(outfile, 'w')
    f1 = open(filename1, 'r')
    f2 = open(filename2, 'r')
    cmds1 = json.loads(f1.read())["commands"]
    cmds2 = json.loads(f2.read())["commands"]
    edges1, nodes1 = buildGraph(cmds1)
    edges2, nodes2 = buildGraph(cmds2)
    kernel = generateKernel(nodes1, nodes2)

    f.write(str(len(nodes1)) + ' ' + str(len(nodes1)-1))
    f.write("\n")

    for i in range(len(edges1)):
        for j in range(len(edges1[i])):
            f.write(str(i) + ' ' + str(edges1[i][j]))
            f.write('\n')
    f.write('\n')
    f.write(str(len(nodes2)) +  ' ' + str(len(nodes2)-1))
    f.write('\n')

    for i in range(len(edges2)):
        for j in range(len(edges2[i])):
            f.write(str(i) + ' ' + str(edges2[i][j]))
            f.write('\n')
    f.write('\n')
    for line in kernel:
        f.write(" ".join([str(num) for num in line]))
        f.write('\n')
    f.close()
    
