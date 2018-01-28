# Jeff Hildebrandt
# Program 1 Text Similarity Analysis
# CAP6640 Natural Language Processing

import sys
from collections import deque


class TokenizeFiles:
    def __init__(self, src: str, tgt: str):
        self.srcFileName = src
        self.tgtFileName = tgt
        self.rawSrc = parse(src)
        self.rawTgt = parse(tgt)
        self.norSrc = self.tokenize(self.rawSrc)
        self.norTgt = self.tokenize(self.rawTgt)
        self.norSrcArr = self.norSrc.split()
        self.norTgtArr = self.norTgt.split()
        self.print()

    @staticmethod
    def tokenize(tokstr: str) -> str:
        nor = []
        splitstring = tokstr.lower().split()

        for token in splitstring:
            if len(token) > 1:
                first = token[0]
                last = token[-1]
                lastlast = token[-2]
                lastlastlast = ""

                hasalpha = False
                for char in token:
                    if char.isalnum():
                        hasalpha = True
                        break

                if len(token) > 2:
                    lastlastlast = token[-3]
                endadd = deque()

                if lastlast == "'" and last == "s":
                    token = token[:-2]
                    endadd.append("'s")
                elif lastlastlast == "n" and lastlast == "'" and last == "t":
                    token = token[:-3]
                    endadd.append("not")
                elif lastlast == "'" and last == "m":
                    token = token[:-2]
                    endadd.append("am")
                elif hasalpha and first.isalnum() and not token[-1].isalnum():
                    while len(token) > 0 and not token[-1].isalnum():
                        endadd.appendleft(token[-1])
                        token = token[:-1]

                ntoken = ""

                if hasalpha:
                    for char in token:
                        if char.isalnum() or first.isalnum():
                            ntoken += char
                        else:
                            if ntoken != "":
                                nor.append(ntoken)
                            ntoken = ""
                            nor.append(char)
                    if ntoken != "":
                        nor.append(ntoken)
                else:
                    if len(token) > 0:
                        nor.append(token)

                if len(endadd) > 0:
                    nor = nor + list(endadd)
            else:
                nor.append(token)

        return " ".join(nor)

    def print(self) -> None:
        print("University of Central Florida")
        print("CAP6640 Spring 2018 - Dr. Glinos")
        print()
        print("Text Similarity Analysis by Jeff Hildebrandt")
        print()
        print("Source file: " + self.srcFileName)
        print("Target file: " + self.tgtFileName)
        print()
        print("Raw Tokens:")
        print("     Source > " + self.rawSrc)
        print("     Target > " + self.rawTgt)
        print()
        print("Normalized Tokens:")
        print("     Source > " + self.norSrc)
        print("     Target > " + self.norTgt)
        print()


def parse(filename: str) -> str:
    file = open(filename, 'r')
    lines = file.readlines()
    retstr = ""
    for line in lines:
        retstr += line.rstrip() + " "
    return retstr.rstrip()


class TextSimilarityAnalysis:
    def __init__(self, src: [], tgt: [], gap: int, mis: int, match: int):
        self.src = src
        self.tgt = tgt
        self.gap = gap
        self.mis = mis
        self.match = match
        self.editdist = [[None for j in range(len(src) + 1)] for i in range(len(tgt) + 1)]
        # initialize the values of the table
        for i in range(len(tgt) + 1):
            self.editdist[i][0] = 0
        for j in range(len(src) + 1):
            self.editdist[0][j] = 0
        self.populateeditdisttable()
        self.print(self.editdist)

    def populateeditdisttable(self):
        for i in range(1, len(self.tgt) + 1):
            for j in range(1, len(self.src) + 1):
                self.editdist[i][j] = self.getmax(i, j)

    def getmax(self, i, j) -> int:
        match = self.mis
        if self.tgt[i-1] == self.src[j-1]:
            match = self.match
        return max([0, self.editdist[i-1][j] + self.gap, self.editdist[i][j-1] + self.gap, self.editdist[i-1][j-1] + match])

    def print(self, arr):
        firstline = "              "
        secondline = "               #   "
        for i in range(len(self.tgt) + 1):
            if len(str(i)) == 1:
                firstline += " " + str(i) + "   "
            else:
                if len(str(i)) < 5:
                    firstline += str(i)
                    for j in range(5 - len(str(i))):
                        firstline += " "
                else:
                    firstline += ".." + str(i)[-3:]
            tgtindex = i - 1
            if tgtindex >= 0 and tgtindex < len(self.tgt):
                if len(self.tgt[tgtindex]) == 1:
                    secondline += "  " + self.tgt[tgtindex]
                elif len(self.tgt[tgtindex]) == 2:
                    secondline += " " + self.tgt[tgtindex]
                else:
                    secondline += self.tgt[tgtindex][:3]
                secondline += "  "
        print(firstline)
        print(secondline)
        for i in range(len(self.src) + 1):
            nextline = ""
            if len(str(i)) < 4:
                for k in range(4 - len(str(i))):
                    nextline += " "
                nextline += str(i)
            else:
                nextline += "." + str(i)[-3:]
            nextline += "    "
            if i == 0:
                nextline += " #    "
            else:
                srcindex = i - 1
                if srcindex >= 0 and srcindex < len(self.src):
                    if len(self.src[srcindex]) == 1:
                        nextline += "  " + self.src[srcindex]
                    elif len(self.src[srcindex]) == 2:
                        nextline += " " + self.src[srcindex]
                    else:
                        nextline += self.src[srcindex][:3]
                    nextline += "   "
            for j in range(len(self.src) + 1):
                if len(str(arr[i][j])) == 1:
                    nextline += " " + str(arr[i][j]) + "   "
                else:
                    if len(str(arr[i][j])) < 5:
                        nextline += str(arr[i][j])
                        for j in range(5 - len(str(arr[i][j]))):
                            nextline += " "
                    else:
                        nextline += ".." + str(arr[i][j])[-3:]
            print(nextline)

if __name__ == "__main__":
    tokenized = TokenizeFiles(sys.argv[1], sys.argv[2])
    TextSimilarityAnalysis(tokenized.norSrcArr, tokenized.norTgtArr, -1, -1, 2)
