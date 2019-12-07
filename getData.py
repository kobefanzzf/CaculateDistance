import os
import sys

dirsPath = sys.argv[1]
outDir = sys.argv[2]

if __name__ == "__main__":
    dirs = os.listdir(dirsPath)
    for dir in dirs:
        dirPath = dirsPath + dir
        outfile = dir + '.txt'
        command = "python merge.py " + dirPath + " " + outfile
        os.system(command)
