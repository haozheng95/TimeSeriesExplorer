from os import listdir
from os.path import isfile, join

y = []
with open("../dataset1/training.csv") as f:
    i = 0
    for line in f.readlines():
        if i > 0:
            y.append(line.split(',')[4])
        i += 1

mypath = "../dataset1/training/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

result = ''

j = 0
for file in onlyfiles:
    with open(join(mypath, file)) as f:
        i = 0
        for line in f.readlines():
            if i == 0:
                result += y[j]
            else:
                result += '\t' + line.replace(',', '\t')
            i += 1
    j += 1
    result += '\n\n'
    print(j)

outF = open("phm_17.data", "w")
outF.write(result)

