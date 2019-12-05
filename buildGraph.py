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
    cnt = 0
    root = {
        "command": "DrawRect",
        "visible": True,
        "coords": [ 0, 0, 10000, 10000],
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
        minArea = 1000000000000
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
            cnt += 1
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
            print(coords1, coords2)
            if isIn(coords1, coords2):
                area = getArea(coords2)
                if area < minArea:
                    minArea = area
                    minj = j

        if minj != -1:
            cnt += 1
            edges[minj].append(i)

    return edges, cnt

def generateKernel(cmds1, cmds2):
    kernel = []
    for obj1 in cmds1:
        line = []
        for obj2 in cmds2:
            line.append(nodeComparison(obj1, obj2))
        kernel.append(line)
    return kernel
    





    

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("format error!")
        exit(0)
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    f1 = open('')
    f1 = open(filename1, 'r')
    f2 = open(filename2, 'r')
    cmds1 = json.loads(f1.read())["commands"]
    cmds2 = json.loads(f2.read())["commands"]
    edges1, len1 = buildGraph(cmds1)
    edges2, len2 = buildGraph(cmds2)
    kernel = generateKernel(cmds1, cmds2)
    print(len1 + 1, len1)
    for i in range(len1 + 1):
        for j in range(len(edges1[i])):
            print(i, edges1[i][j])
    print("\n")
    print(len2 + 1, len2)
    for i in range(len2 + 1):
        for j in range(len(edges2[i])):
            print(i, edges2[i][j])
    print("\n")
    for line in kernel:
        print(' '.join(line))
    
    # with open("layer_0.txt", 'r') as f:
    #     content = f.read()
    #     commands = json.loads(content)["commands"]
    #     edges = buildGraph(commands)
    #     print(edges)
