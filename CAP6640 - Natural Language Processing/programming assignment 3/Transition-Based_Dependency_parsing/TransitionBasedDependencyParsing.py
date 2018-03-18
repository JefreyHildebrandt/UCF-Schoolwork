import os, sys, collections

class TransitionBasedDependencyParsing:
    def __init__(self):
        self.tokens = []
        self.postags = set()
        self.leftarc = dict()
        self.rightarc = dict()
        self.leftarcnum = 0
        self.rightarcnum = 0
        self.rootarcnum = 0

    def parsecorpus(self, corpus):
        sentences = 0
        sentarray = []

        for line in corpus:
            lsplit = line.split()
            if len(lsplit) != 4:
                continue
            sentnum = int(lsplit[0])
            token = lsplit[1]
            pos = lsplit[2]
            link = int(lsplit[3])

            if sentnum == 1:
                self.assignlinks(sentarray)
                sentences += 1
                sentarray = []

            sentarray.append(PosLink(sentnum, pos, link))

            self.tokens.append(token)
            if not pos in self.postags:
                self.postags.add(pos)
        self.assignlinks(sentarray)

        self.tokens.sort()
        self.postags = sorted(self.postags)

        endspaces = '      '

        print('Corpus Statistics:\n')
        print('     # sentences  :' + endspaces[:len(endspaces) - len(str(sentences))] + str(sentences))
        print('     # tokens     :' + endspaces[:len(endspaces) - len(str(len(self.tokens)))] + str(len(self.tokens)))
        print('     # POS tags   :' + endspaces[:len(endspaces) - len(str(len(self.postags)))] + str(len(self.postags)))
        print('     # Left-Arcs  :' + endspaces[:len(endspaces) - len(str(self.leftarcnum))] + str(self.leftarcnum))
        print('     # Right-Arcs :' + endspaces[:len(endspaces) - len(str(self.rightarcnum))] + str(self.rightarcnum))
        print('     # Root-Arcs  :' + endspaces[:len(endspaces) - len(str(self.rootarcnum))] + str(self.rootarcnum))
        print('\n')
        print('Left Arc Array Nonzero Counts:\n')
        endspaces = '     '
        for pos in self.postags:
            print(endspaces[:len(endspaces) - len(pos)] + pos + ' : ', end='')
            for pos2 in self.postags:
                if(pos in self.leftarc and pos2 in self.leftarc[pos]):
                    print('[' + endspaces[:len(endspaces) - len(pos2)] + pos2 + ',' +
                          endspaces[:len(endspaces) - len(str(self.leftarc[pos][pos2]))] +
                          str(self.leftarc[pos][pos2]) + ']', end=' ')
            print()
        print('\n\nRight Arc Array Nonzero Counts:\n')
        for pos in self.postags:
            print(endspaces[:len(endspaces) - len(pos)] + pos + ' : ', end='')
            for pos2 in self.postags:
                if (pos in self.rightarc and pos2 in self.rightarc[pos]):
                    print('[' + endspaces[:len(endspaces) - len(pos2)] + pos2 + ',' +
                          endspaces[:len(endspaces) - len(str(self.rightarc[pos][pos2]))] +
                          str(self.rightarc[pos][pos2]) + ']', end=' ')
            print()
        print('\n\nArc Confusion Array:\n')
        for pos in self.postags:
            print(endspaces[:len(endspaces) - len(pos)] + pos + ' : ', end='')
            for pos2 in self.postags:
                if pos in self.leftarc and pos2 in self.leftarc[pos] and pos in self.rightarc and pos2 in self.rightarc[pos]:
                    print('[' + endspaces[:len(endspaces) - len(pos2)] + pos2 + ',' +
                          endspaces[:len(endspaces) - len(str(self.leftarc[pos][pos2]))] +
                          str(self.leftarc[pos][pos2]) +
                          endspaces[:len(endspaces) - len(str(self.rightarc[pos][pos2]))] +
                          str(self.rightarc[pos][pos2]) + ']', end=' ')
            print()

    def parsesentence(self, inputtext):
        pass

    def assignlinks(self, sentarray):
        if len(sentarray) < 1:
            return
        for poslink in sentarray:
            if poslink.link == 0:
                self.rootarcnum += 1
                continue
            linkpos = sentarray[poslink.link - 1].pos
            if poslink.sentnum < poslink.link:
                self.leftarcnum += 1
                if not poslink.pos in self.leftarc:
                    self.leftarc[poslink.pos] = dict()
                if not linkpos in self.leftarc[poslink.pos]:
                    self.leftarc[poslink.pos][linkpos] = 0
                self.leftarc[poslink.pos][linkpos] += 1
            else:
                self.rightarcnum += 1
                if not poslink.pos in self.rightarc:
                    self.rightarc[poslink.pos] = dict()
                if not linkpos in self.rightarc[poslink.pos]:
                    self.rightarc[poslink.pos][linkpos] = 0
                self.rightarc[poslink.pos][linkpos] += 1


class PosLink:
    def __init__(self, sentnum, pos, link):
        self.sentnum = sentnum
        self.pos = pos
        self.link = link

if __name__== "__main__":
    print("University of Central Florida")
    print("CAP6640 Spring 2018 - Dr. Glinos")
    print("Dependency Parser by Jeff Hildebrandt\n\n")

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    corpus = open(os.path.join(__location__, 'wsj-dep.txt'), 'r')
    inputtext = open(sys.argv[1], 'r')

    transition = TransitionBasedDependencyParsing()
    transition.parsecorpus(corpus)
    transition.parsesentence(inputtext)
