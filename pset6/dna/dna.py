import sys
import csv
import re


def computeMaxRepetitionsOfPattern(seq, pattern):
    """ Compute the largest number of consecutive times that the STR (pattern) [substring] repeats in the given DNA sequence [string] """
    groups = re.findall(fr"(?:{pattern})+", seq)   # Or: groups = re.findall(r"(?:%s)+" % pattern, seq)
    if groups:
        largest = max(groups, key=len)
        return len(largest) // len(pattern)
    else:
        return 0


def main():
    if (len(sys.argv) != 3):
        print("Usage: python dna.py <database-csv-file> <DNA-sequence-txt-file>")
        sys.exit(1)

    # Read DNA database csv file
    with open(sys.argv[1], 'r') as csvfile:
        database_reader = csv.reader(csvfile)   # a list of strings
        for i, row in enumerate(database_reader):
            if (i == 0):
                # Read DNA sequence txt file
                with open(sys.argv[2], 'r') as txtfile:
                    seq = txtfile.read()

                    # For each of the STRs, compute the longest run of consecutive repeats of the STR (pattern) in the DNA sequence to identify
                    listOfMaxRepetitionsOfPatterns = []
                    for pattern in row[1:]:
                        n = computeMaxRepetitionsOfPattern(seq, pattern)
                        listOfMaxRepetitionsOfPatterns.append(str(n))
            else:
                # Compare against database
                database = row[1:]
                if (listOfMaxRepetitionsOfPatterns == database):
                    print(row[0])
                    return
        else:
            print("No match")


if __name__ == "__main__":
    main()