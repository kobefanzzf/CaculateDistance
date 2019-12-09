import os
import sys

dirPath = sys.argv[1]
outPath = sys.argv[2]

if __name__ == "__main__":
    files = os.listdir(dirPath)
    count = len(files)
    for i in range(count):
        for j in range(i):
            file1 = files[i]
            file2 = files[j]
            filename = file1.split('.')[0] + 'vs' +  file2.split('.')[0] + '.txt'
            command = "python scripts/buildGraph.py " + dirPath  + file1 + " " + dirPath + file2 + " " + outPath + filename
            print(command)
            os.system(command) 
            