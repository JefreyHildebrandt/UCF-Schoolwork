import sys
from collections import OrderedDict
import uuid

class HiddenMarkovModel:
    initialuuid = " "
    def __init__(self, corpusloc):
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

        previous = HiddenMarkovModel.initialuuid
        for line in f:
            ## skips blank lines
            splitline = line.split(" ")
            if len(splitline) != 2:
                word = None
                tag = HiddenMarkovModel.initialuuid
            else:
                word = splitline[0].rstrip()
                tag = splitline[1].rstrip()

            if word != None:
                word = HiddenMarkovModel.convertword(word)

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

    @staticmethod
    def convertword(word):
        word = word.rstrip().lower()
        if word.endswith("sses") or word.endswith("xes") or word.endswith("ches") or word.endswith("shes"):
            word = word[:-2]
        elif word.endswith("ses") or word.endswith("zes"):
            word = word[:-1]
        elif word.endswith("men"):
            word = word[:-2] + "an"
        elif word.endswith("ies"):
            word = word[:-3] + "y"
        return word

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
            if HiddenMarkovModel.initialuuid in values and HiddenMarkovModel.initialuuid in self.tagmapcount:
                print("start [ " + key + " |  ] " + str("{:f}".format(round(values[HiddenMarkovModel.initialuuid] / self.tagmapcount[HiddenMarkovModel.initialuuid], 6))))

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
        print(totalnum + "sentences   : " + str(self.tagmapcount[HiddenMarkovModel.initialuuid]))

class Viterbi:
    def __init__(self, hmm: HiddenMarkovModel, testdocloc: str):
        self.hmm = hmm
        self.sentences = self.parseviterbi(testdocloc)
        # self.printsentences()
        self.viterbialg()

    def parseviterbi(self, testdocloc):
        f = open(testdocloc, "r")
        sentences = []
        for line in f:
            sentence = line.split(" ")
            sentencedict = OrderedDict()
            for word in sentence:
                word = word.rstrip()
                convword = HiddenMarkovModel.convertword(word)
                sentencedict[word] = dict()
                if convword in self.hmm.emissioncount:
                    values = self.hmm.emissioncount[convword]
                    for k, v in values.items():
                        sentencedict[word][k] = v / self.hmm.tagmapcount[k]
                else:
                    sentencedict[word]["NN"] = 1
                sentencedict[word] = OrderedDict(sorted(sentencedict[word].items()))
            sentences.append(sentencedict)
        return sentences

    def viterbialg(self):
        for sent in self.sentences:
            prevtagvals = []
            prevtagvals.append(dict())
            i = 0
            prevtagvals[i][HiddenMarkovModel.initialuuid] = 1
            tagused = []
            tagused.append(dict())
            for key, values in sent.items():
                calcvals = []
                tags = []
                for k, v in values.items():
                    oneval = []
                    oneval.append(0)
                    lrgest = 0
                    lrgesttag = ""
                    for maxkey in prevtagvals[i]:
                        if k in self.hmm.tagtransition and maxkey in self.hmm.tagtransition[k]:
                            lrg = (self.hmm.tagtransition[k][maxkey] / self.hmm.tagmapcount[maxkey]) * prevtagvals[i][maxkey]
                            if lrg >= lrgest:
                                lrgest = lrg
                                if maxkey == HiddenMarkovModel.initialuuid:
                                    lrgesttag = "null"
                                else:
                                    lrgesttag = maxkey

                    tags.append(lrgesttag)
                    calcvals.append(v * lrgest)

                normvals = []
                for nums in calcvals:
                    normvals.append(nums/sum(calcvals))
                i += 1
                index = 0
                for k, v in values.items():
                    prevtagvals.append(dict())
                    prevtagvals[i][k] = normvals[index]
                    tagused.append(dict())
                    tagused[i][k] = tags[index]
                    index += 1
            self.printsentences(sent, prevtagvals, tagused)


    def printsentences(self, ordereddict, prevtagvals, tagused):
        print("\nTest Set Tokens Found in Corpus:\n")
        initspace = "                "
        tagspace = "     "
        for key, values in ordereddict.items():
            if(len(key) <= len(initspace)):
                printsent = initspace[:-len(key)] + key + " :"
            else:
                printsent = key + " :"
            for k, v in values.items():
                printsent += tagspace[:-len(k)] + k + " (" + str("{:f}".format(round(v, 6))) + ")"
            print(printsent)
        print("\n\nIntermediate Results of Viterbi Algorithm:\n")

        i = 1
        itspace = "   "
        initspace = "             "
        for key, values in ordereddict.items():
            printsent = "Iteration" + itspace[:-len(str(i))] + str(i) + " :"
            if(len(key) <= len(initspace)):
                printsent += initspace[:-len(key)] + key + " :"
            else:
                printsent += key + " :"
            for k, v in values.items():
                printsent += tagspace[:-len(k)] + k + " (" + str("{:f}".format(round(prevtagvals[i][k], 6))) + ", " + tagused[i][k] + ")"
            print(printsent)
            i += 1

if __name__== "__main__":
    print("University of Central Florida")
    print("CAP6640 Spring 2018 - Dr. Glinos\n")
    print("Viterbi Algorithm HMM Tagger by Jeff Hildebrandt\n\n")
    corpusloc = sys.argv[1]
    testdocloc = sys.argv[2]
    hmm = HiddenMarkovModel(corpusloc)
    Viterbi(hmm, testdocloc)