import json
from math import sqrt,pi

def loadData():
    str1 = ""
    str2 = ""
    with open('data1.json', 'r', encoding="utf-8") as f:
        str1 = f.read()
        f.close()
    with open('data2.json', 'r', encoding="utf-8") as f:
        str2 = f.read()
        f.close()
    json1 = json.loads(str1)
    json2 = json.loads(str2)
    return json1, json2

def compareShape(json1, json2):
    #check: drawRRect coords
    shape = [json1["command"], json2["command"]]
    if shape[0] == shape[1]:
        return 1
    elif "DrawRect" in shape and "DrawRRect" in shape or "DrawRRect" in shape and "DrawImageRect" in shape:
        RRect = json1 if json1["command"] == "DrawRRect" else json2
        sim = 1 - RRect["coords"][1][0]/abs(RRect["coords"][0][0] - RRect["coords"][0][1])
        return sim
    elif "DrawRect" in shape and "DrawImageRect" in shape or "DrawRect" in shape and "DrawTextBlob" in shape \
    or "DrawTextBlob" in shape and "DrawImageRect" in shape:
        sim = 0.7
        return sim
    else:
        return 0.1

def getPathLen(json1):
    points = []
    path_len = 0
    for i in range(len(json1["path"]["verbs"])):
        if "move" in json1["path"]["verbs"][i]:
            points.append(json1["path"]["verbs"][i]["move"])
        elif "line" in json1["path"]["verbs"][i]:
            points.append(json1["path"]["verbs"][i]["line"])
        else:
            continue;
    for i in range(len(points) - 1):
        dx = points[i][0] - points[i+1][0]
        dy = points[i][1] - points[i+1][1]
        path_len = path_len + sqrt(dx * dx + dy * dy)
    return path_len

def getPathPosition(json1):
    points = []
    for i in range(len(json1["path"]["verbs"])):
        if "move" in json1["path"]["verbs"][i]:
            points.append(json1["path"]["verbs"][i]["move"])
        elif "line" in json1["path"]["verbs"][i]:
            points.append(json1["path"]["verbs"][i]["line"])
        else:
            continue;
    return points


def compareSize(json1, json2):
    shape = [json1["command"], json2["command"]]
    if shape[0] == shape[1]:
        if shape[0] == "DrawPath":
            len1 = getPathLen(json1)
            len2 = getPathLen(json2)
            return min(len1,len2)/max(len1,len2)
            #todo
        elif shape[0] == "DrawRRect":
            size1 = abs(json1["coords"][0][0] - json1["coords"][0][2]) * abs(json1["coords"][0][1] - json1["coords"][0][3]) + abs(json1["coords"][1][0]*2*json1["coords"][1][0]*2 - pi*json1["coords"][1][0]*json1["coords"][1][0])
            size2 = abs(json2["coords"][0][0] - json2["coords"][0][2]) * abs(json2["coords"][0][1] - json2["coords"][0][3]) + abs(json2["coords"][1][0]*2*json2["coords"][1][0]*2 - pi*json2["coords"][1][0]*json2["coords"][1][0])
            return min(size1,size2)/max(size1,size2)
        else:
            position1 = json1["shortDesc"].strip(' []').split(" ")
            position2 = json2["shortDesc"].strip(' []').split(" ")
            size1 = abs(float(position1[0]) - float(position1[2]))*abs(float(position1[1]) - float(position1[3]))
            size2 = abs(float(position2[0]) - float(position2[2]))*abs(float(position2[1]) - float(position2[3]))
            return min(size1,size2)/max(size1,size2)
    else:
        if shape[0] == "DrawPath" or shape[1] == "DrawPath":
            return 0.1
        elif shape[0] == "DrawRRect" or shape[1] == "DrawRRect":
            RRect = json1 if json1["command"] == "DrawRRect" else json2
            noRRect = json2 if json1["command"] == "DrawRRect" else json1
            size1 = abs(RRect["coords"][0][0] - RRect["coords"][0][2]) * abs(RRect["coords"][0][1] - RRect["coords"][0][3]) + abs(RRect["coords"][1][0]*2*RRect["coords"][1][0]*2 - pi*RRect["coords"][1][0]*RRect["coords"][1][0])
            position2 = noRRect["shortDesc"].strip(' []').split(" ")
            print(noRRect)
            size2 = abs(float(noRRect[0]) - float(noRRect[2]))*abs(float(noRRect[1]) - float(noRRect[3]))
            return min(size1,size2)/max(size1,size2)
        else:
            position1 = json1["shortDesc"].strip(' []').split(" ")
            position2 = json2["shortDesc"].strip(' []').split(" ")
            size1 = abs(float(position1[0]) - float(position1[2]))*abs(float(position1[1]) - float(position1[3]))
            size2 = abs(float(position2[0]) - float(position2[2]))*abs(float(position2[1]) - float(position2[3]))
            return min(size1,size2)/max(size1,size2)
    


def comparePosition(json1, json2):
    shape = [json1["command"], json2["command"]]

    if shape[0] == shape[1] and shape[0] == "DrawPath":
        points1 = getPathPosition(json1)
        points2 = getPathPosition(json2)
        min_len = min(len(points1), len(points2))
        pos_dis = 0
        for i in range(min_len):
            pos_dis = pos_dis + sqrt((points1[i][0] - points2[i][0])*(points1[i][0] - points2[i][0]) + (points1[i][1] - points2[i][1])*(points1[i][1] - points2[i][1]))
        path_len1 = getPathLen(json1)
        path_len2 = getPathLen(json2)
        result = 1 - pos_dis/max(path_len1, path_len2)
        return result if result >= 0 else 0

    elif shape[0] == "DrawPath" or shape[1] == "DrawPath":
        path = json1 if json1["command"] == "DrawPath" else json2
        nonPath = json2 if json1["command"] == "DrawPath" else json1
        points1 = getPathPosition(path)
        x = 0
        y = 0
        for i in range(len(points1)-1):
            x = x + points1[i][0]
            y = y + points1[i][1]
        path_x = x/(len(points1)-1)
        path_y = y/(len(points1)-1)
        nonpath_x = 0
        nonpath_y = 0
        if nonPath["command"] == "DrawRRect":
            nonpath_x = (nonPath["coords"][0][0] + nonPath["coords"][0][2])/2
            nonpath_y = (nonPath["coords"][0][1] + nonPath["coords"][0][3])/2
        else:
            nonpath_pos = nonPath["shortDesc"].strip(' []').split(" ")
            nonpath_x = (float(nonpath_pos[0]) + float(nonpath_pos[2]))/2
            nonpath_y = (float(nonpath_pos[1]) + float(nonpath_pos[3]))/2
        sim = 1 - sqrt((path_x - nonpath_x)*(path_x - nonpath_x)+(path_y - nonpath_y)*(path_y - nonpath_y))/sqrt(path_x*path_x + path_y*path_y)
        return sim
    else:
        if shape[0] == "DrawRRect" or shape[1] == "DrawRRect":
            RRect = json1 if json1["command"] == "DrawRRect" else json2
            nonRRect = json2 if json1["command"] == "DrawRRect" else json1
            RRect_x = (RRect["coords"][0][0] + RRect["coords"][0][2])/2
            RRect_y = (RRect["coords"][0][1] + RRect["coords"][0][3])/2
            nonRRect_pos = nonRRect["shortDesc"].strip(' []').split(" ")
            nonRRect_x = (float(nonRRect_pos[0]) + float(nonRRect_pos[2]))/2
            nonRRect_y = (float(nonRRect_pos[1]) + float(nonRRect_pos[3]))/2
            sim = 1 - sqrt((RRect_x - nonRRect_x)*(RRect_x - nonRRect_x)+(RRect_y - nonRRect_y)*(RRect_y - nonRRect_y))/sqrt(RRect_x*RRect_x + RRect_y*RRect_y)
            return sim
        else:
            json1_pos = json1["shortDesc"].strip(' []').split(" ")
            json2_pos = json2["shortDesc"].strip(' []').split(" ")
            json1_x = (float(json1_pos[0]) + float(json1_pos[2]))/2
            json1_y = (float(json1_pos[1])+ float(json1_pos[3]))/2
            json2_x = (float(json2_pos[0]) + float(json2_pos[2]))/2
            json2_y = (float(json2_pos[1]) + float(json2_pos[3]))/2
            sim = 1 - sqrt((json1_x - json2_x)*(json1_x - json2_x)+(json1_y - json2_y)*(json1_y - json2_y))/sqrt(json1_x*json1_x + json1_y*json1_y)
            return sim



def nodeComparison(json1, json2):
    w_shape = 0.6
    w_size = 0.2
    w_position = 0.2

    sim_shape = compareShape(json1,json2)
    print("Shape Similarity: ", sim_shape)
    sim_size = compareSize(json1, json2)
    print("Size Similarity: ", sim_size)
    sim_position = comparePosition(json1, json2)
    print("Position Similarity: ", sim_position)
    sim = w_shape * sim_shape + w_size * sim_size + w_position * sim_position
    sim = 1 - sim
    return sim

if __name__ == '__main__':
    ##原始json对象
    json1, json2 = loadData()
    #调用方法
    sim = nodeComparison(json1, json2)

    print("Overall Similarity: ", sim)




