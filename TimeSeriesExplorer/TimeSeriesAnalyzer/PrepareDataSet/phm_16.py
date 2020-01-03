from os import listdir
from os.path import isfile, join

y = {}
with open("../dataset16/CMP-training-removalrate.csv") as f:
    i = 0
    for line in f.readlines():
        if i > 0:
            items = line.split(',')
            if items[0] not in y:
                y[items[0]] = {}
            y[items[0]][items[1]] = items[2]
        i += 1
print(y)

mypath = "../dataset16/CMP-data/training/"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

print(listdir(mypath))

result = ''

j = 0
previous_wafer_id = None
previous_stage = None
for file in onlyfiles:
    with open(join(mypath, file)) as f:
        i = 0
        for line in f.readlines():
            if i > 0:
                items = line.split(',')
                WAFER_ID = items[3]
                STAGE = items[4]
                if previous_wafer_id is None and previous_stage is None:
                    result += y[WAFER_ID][STAGE]
                elif (previous_wafer_id is not None and previous_stage is not None) and (previous_stage != STAGE or previous_wafer_id != WAFER_ID):
                    j += 1
                    print(j)
                    result += '\n\n' + y[WAFER_ID][STAGE]
                else:
                    result += '\t' + line.replace(',', '\t')
                previous_wafer_id = WAFER_ID
                previous_stage = STAGE

            i += 1

outF = open("phm_16.data", "w")
outF.write(result)

