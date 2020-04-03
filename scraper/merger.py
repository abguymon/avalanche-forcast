#!/bin/python3

import csv
import sys

def main(args):
    collected = dict()

    with open(args[0], mode="r", newline='') as latLongFile:
        with open(args[1], mode="r", newline='') as oldfile:
            with open(args[2], mode="w", newline='') as newfile:
                latReader = csv.reader(latLongFile)
                oldReader = csv.reader(oldfile)
                newWriter = csv.writer(newfile)

                for row in latReader:
                    if row[0] == 'Date':
                        newWriter.writerow(row)
                        continue
                    else:
                        collected[row[1]] = row[4:-1]

                for row in oldReader:
                    if row[0] == 'Date':
                        continue
                    elif len(row) > 2 and len(row[1]) > 0:
                        if row[1] in collected:
                            newWriter.writerow(row[:-1] + collected[row[1]] + row[-1:])
                            print('.', end='')
                        else:
                            print('N',end='')
    print("\nDone\n")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise SyntaxError("Need names of files to read and file to write")
    main(sys.argv[1:])