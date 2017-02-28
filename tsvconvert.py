from pandas import DataFrame
import os.path
import uuid
import sys
import subprocess


writeFile = "expressionInsert.sql"
readFile = "expression_subset.tsv"

try:
    df = DataFrame.from_csv(readFile, sep="\t")
except IOError:
    print "Could not open file: ", readFile
    sys.exit()

try:
    f = open(writeFile, 'w')
except IOError:
    print "Could not open file: ", writeFile
    sys.exit()


f.write("BEGIN TRANSACTION;" + os.linesep)

for i in range(0, len(df.columns)):
    for j in range(0, len(df)):
        prepareString = "INSERT INTO \"Expression\" VALUES("
        prepareString += "'" + str(uuid.uuid4()) + "', " #ID
        prepareString += "'rsem', " #RNAQuantification
        prepareString += "'" + df.index[j]  + "', " #Name
        prepareString += "'', " #FeatureID
        prepareString += str(df.iat[j, i]) + ", "  #Expression
        prepareString += "1.0, "  #isNormalized
        prepareString += "0.0, " #ReadCount
        prepareString += "0.0, " #Score
        prepareString += "2.0, " #Units
        prepareString += "0.0, " #ConfigLow
        prepareString += "0.0);" #ConfigHigh

        f.write(prepareString + os.linesep)

f.write("COMMIT;" + os.linesep)

f.close()

