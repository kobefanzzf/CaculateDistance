import os
import sys


scriptPath = "/media/zzf/新加卷1/skia/out/Debug/skp_parser "

if __name__ == "__main__":
    dirPath = sys.argv[1]
    # outdir = sys.argv[2]
    files = os.listdir(dirPath)
    for file in files:
        file_type = os.path.splitext(file)[-1]
        if file_type != ".skp":
            continue
        filePath = dirPath + file
        outfile = dirPath + "json" + file + ".txt"
        command = scriptPath + filePath + " >> " + outfile
        os.system(command)