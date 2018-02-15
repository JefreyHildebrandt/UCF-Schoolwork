import sys
from collections import OrderedDict
import uuid

class HiddenMarkovModel:
    def __init__(self, corpusloc):
        self.initialuuid = " "
        self.tagmap = OrderedDict()
        self.tagmapcount = OrderedDict()
        self.tagtransition = OrderedDict()
        self.emissioncount = OrderedDict()
        # self.emissionprob = OrderedDict()
        self.totalcount = 0
        self.readfile(corpusloc)
        self.printalltagsandorder()

    def readfile(self, corpusloc):
        f = open(corpusloc, "r")
        tagmap = dict()
        tagmapcount = dict()
        tagtransition = dict()
        emissioncount = dict()

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

                if not word in emissioncount:
                    emissioncount[word] = dict()
                if not tag in emissioncount[word]:
                    emissioncount[word][tag] = 1
                else:
                    emissioncount[word][tag] += 1

                if not tag in tagmap:
                    tagmap[tag] = dict()
                if not word in tagmap[tag]:
                    tagmap[tag][word] = 1
                else:
                    tagmap[tag][word] += 1

            if not tag in tagmapcount:
                tagmapcount[tag] = 1
            else:
                tagmapcount[tag] += 1
            self.totalcount += 1

            if not tag in tagtransition:
                tagtransition[tag] = dict()
            if not previous in tagtransition[tag]:
                tagtransition[tag][previous] = 1
            else:
                tagtransition[tag][previous] += 1

            previous = tag

        self.tagmap = OrderedDict(sorted(tagmap.items()))
        self.tagmapcount = OrderedDict(sorted(tagmapcount.items()))
        self.tagtransition = OrderedDict(sorted(tagtransition.items()))
        self.emissioncount = OrderedDict(sorted(emissioncount.items()))

    def printalltagsandorder(self):
        print("All Tags Observed:\n")
        i = 0
        for key, values in self.tagmap.items():
            i += 1
            self.tagmap[key] = OrderedDict(sorted(self.tagmap[key].items()))
            print(" " + str(i) + "  " + key)

        print("\nInitialDistribution:\n")
        for key, values in self.tagtransition.items():
            self.tagtransition[key] = OrderedDict(sorted(self.tagtransition[key].items()))
            if self.initialuuid in values and self.initialuuid in self.tagmapcount:
                print("start [ " + key + " |  ] " + str("{:f}".format(round(values[self.initialuuid] / self.tagmapcount[self.initialuuid], 6))))

        print("\nEmission Probabilites:\n")
        # emissionprob = dict()
        wordspaces = "                "
        tagspaces = "     "
        for key, values in self.emissioncount.items():
            wordline = ""
            if len(key) <= len(wordspaces):
                wordline += wordspaces[:-len(key)]
            wordline += key
            for k, v in values.items():
                tagline = ""
                if len(k) <= len(tagspaces):
                    tagline += tagspaces[:-len(k)]
                printline = wordline + tagline + str(k) + " " + str("{:f}".format(round(v / self.tagmapcount[k], 6)))
                print(printline)

        print("\nTransition Probabilities:\n")
        bigramcount = 0
        for k, v in self.tagmapcount.items():
            totalpercentage = 0
            probline = ""
            for key, values in self.tagtransition.items():
                if k in values and k in self.tagmapcount:
                    prob = values[k] / self.tagmapcount[k]
                    totalpercentage += prob
                    probline += "[" + key + "|" + k + "] " + str("{:f}".format(round(prob, 6))) + "  "
                    bigramcount += 1
            probline = "[ " + "{:f}".format(round(totalpercentage, 6)) + " ]   " + probline
            print(probline)

        print("\nCorpus Features:\n")
        totalnum = "Total # "
        print(totalnum + "tags        : " + str(len(self.tagmap)))
        print(totalnum + "bigrams     : " + str(bigramcount))
        print(totalnum + "lexicals    : " + str(len(self.emissioncount)))
        print(totalnum + "sentences   : " + str(self.tagmapcount[self.initialuuid]))

class Viterbi:
    def __init__(self, hmm, testdocloc):
        self.sentences = self.parseviterbi(testdocloc)
        print()

    def parseviterbi(self, testdocloc):
        f = open(testdocloc, "r")
        sentences = []
        for line in f:
            sentence = line.split(" ")
            sentencedict = OrderedDict()
            for word in sentence:
                sentencedict[word.rstrip().lower()] = OrderedDict()
            sentences.append(sentencedict)
        return sentences

if __name__== "__main__":
    print("University of Central Florida")
    print("CAP6640 Spring 2018 - Dr. Glinos\n")
    print("Viterbi Algorithm HMM Tagger by Jeff Hildebrandt\n\n")
    corpusloc = sys.argv[1]
    testdocloc = sys.argv[2]
    hmm = HiddenMarkovModel(corpusloc)
    Viterbi(hmm, testdocloc)