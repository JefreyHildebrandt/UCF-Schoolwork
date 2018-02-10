import sys
from collections import OrderedDict
import uuid

class HiddenMarkovModel:
    def __init__(self, corpusloc):
        self.initialuuid = " "
        self.trainmap = OrderedDict()
        self.trainmapcount = OrderedDict()
        self.tagtransition = OrderedDict()
        self.totalcount = 0
        self.readfile(corpusloc)
        self.printalltagsandorder()

    def readfile(self, corpusloc):
        f = open(corpusloc, "r")
        trainmap = dict()
        trainmapcount = dict()
        tagtransition = dict()
        previous = self.initialuuid
        for line in f:
            ## skips blank lines
            splitline = line.split(" ")
            if len(splitline) != 2:
                word = None
                tag = self.initialuuid
            else:
                word = splitline[0].rstrip()
                tag = splitline[1].rstrip()

            if word != None:
                word = word.lower()
                if word.endswith("sses") or word.endswith("xes") or word.endswith("ches") or word.endswith("shes"):
                    word = word[:-2]
                elif word.endswith("ses") or word.endswith("zes"):
                    word = word[:-1]
                elif word.endswith("men"):
                    word = word[:-2] + "an"
                elif word.endswith("ies"):
                    word = word[:-3] + "y"

                if not tag in trainmap:
                    trainmap[tag] = dict()
                if not word in trainmap[tag]:
                    trainmap[tag][word] = 1
                else:
                    trainmap[tag][word] += 1

            if not tag in trainmapcount:
                trainmapcount[tag] = 1
            else:
                trainmapcount[tag] += 1
            self.totalcount += 1

            if not tag in tagtransition:
                tagtransition[tag] = dict()
            if not previous in tagtransition[tag]:
                tagtransition[tag][previous] = 1
            else:
                tagtransition[tag][previous] += 1

            previous = tag

        self.trainmap = OrderedDict(sorted(trainmap.items()))
        self.trainmapcount = OrderedDict(sorted(trainmapcount.items()))
        self.tagtransition = OrderedDict(sorted(tagtransition.items()))

    def printalltagsandorder(self):
        print("All Tags Observed:\n")
        i = 0
        for key, values in self.trainmap.items():
            i += 1
            self.trainmap[key] = OrderedDict(sorted(self.trainmap[key].items()))
            print(" " + str(i) + "  " + key)
            # print(self.trainmap[key].items())
        print("\nInitialDistribution:\n")
        for key, values in self.trainmapcount.items():
            # print(key)
            # print(values)
            print("start [ " + key +" |  ] " + str(values / self.totalcount))

class Viterbi:
    def __init__(self, hmm, testdocloc):
        pass

if __name__== "__main__":
    print("University of Central Florida")
    print("CAP6640 Spring 2018 - Dr. Glinos\n")
    print("Viterbi Algorithm HMM Tagger by Jeff Hildebrandt\n\n")
    corpusloc = sys.argv[1]
    testdocloc = sys.argv[2]
    hmm = HiddenMarkovModel(corpusloc)
    Viterbi(hmm, testdocloc)