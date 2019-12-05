import json
import os 

dirsPath = "/Users/zzf/Downloads/skia_data"

dirs = os.listdir(dirsPath)

nameCount = {}
total = 0


def findApi(filePath):
    f = open(filePath, 'r')
    content = f.read()
    commands = json.loads(content)['commands']
    for command in commands:
        if command['command'] == 'DrawPath':
            print('DrawPath', filePath)
        if command['command'] == 'Concat':
            print('Concat', filePath)
        



def countApi(filePath):
    f = open(filePath, 'r')
    content = f.read()
    commands = json.loads(content)['commands']
    for command in commands:
        global total 
        global nameCount
        total += 1
        if command['command'] not in nameCount:
            nameCount[command['command']] = 1
        else:
            nameCount[command['command']] += 1
    

if __name__ == '__main__':
    for dir in dirs:
        if dir == ".DS_Store":
            continue
        dirPath = dirsPath + '/' + dir
        files = os.listdir(dirPath)
        for file in files:
            filePath = dirPath + '/' + file
            file_type = os.path.splitext(file)[-1]
            if file_type == ".txt":
                print(filePath)
                countApi(filePath)
    # nameCount = sorted(nameCount.items(), key=lambda x: -x[1])
    # percentCount = [x[1]/ total for x in nameCount]
    # print(total)
    # print(nameCount)
    # print(percentCount)
    # tmp = 0
    # idx = 0
    # for n in percentCount:
    #     tmp += n
    #     idx += 1
    #     print(tmp, idx)

    



