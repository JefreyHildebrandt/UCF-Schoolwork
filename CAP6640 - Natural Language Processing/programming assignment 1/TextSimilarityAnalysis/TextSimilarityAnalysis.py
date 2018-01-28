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
        self.norSrcArr = []
        self.norTgtArr = []
        self.norSrc = self.tokenize(self.rawSrc, self.norSrcArr)
        self.norTgt = self.tokenize(self.rawTgt, self.norTgtArr)
        self.print()

    @staticmethod
    def tokenize(tokstr: str, nor) -> str:
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
                    for index, char in enumerate(token):
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

    def print(self):
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
    pass


if __name__ == "__main__":
    tokenized = TokenizeFiles(sys.argv[1], sys.argv[2])
