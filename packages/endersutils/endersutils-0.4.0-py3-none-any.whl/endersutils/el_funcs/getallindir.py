import json
import os

files = []

def getFilesInDir(dir: str):
    for f in os.listdir(dir):
        try:
            if not os.listdir(dir + "/" + f) == []:
                getFilesInDir(dir + "/" + f)
        except:
            path = dir + "/" + f
            files.append(path)
    return json.dumps(files)