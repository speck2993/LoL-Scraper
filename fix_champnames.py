import csv
from champDict import idToName

def fixData(source,dest):
    with open(source,'r') as sourceFile:
        with open(dest,'a+') as destFile:
            reader = csv.reader(sourceFile, delimiter=',')
            writer = csv.writer(destFile, delimiter=',')
            readFirst = False
            for row in reader:
                fixedRow = row
                if readFirst:
                    for i in range(4,14):
                        fixedRow[i] = idToName[str.lower(fixedRow[i])]
                    writer.writerow(fixedRow)
                else:
                    writer.writerow(fixedRow)
                    readFirst = True

if __name__ == '__main__':
    fixData('gameDataGM.csv','fixedGameDataGM.csv')
