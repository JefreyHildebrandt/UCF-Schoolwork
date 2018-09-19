# Jeff Hildebrandt
# Program 3 Transition-Based Dependency Parsing
# CAP6640 Natural Language Processing

# This program can be run by using python 3 and passing the cmd argument [sentence input location]
# The corpus is hard coded to be named 'wsj-dep.txt' and must be in the same directory as this file

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
                          str(self.leftarc[pos][pos2]) + ',' +
                          endspaces[:len(endspaces) - len(str(self.rightarc[pos][pos2]))] +
                          str(self.rightarc[pos][pos2]) + ']', end=' ')
            print()

    def parsesentence(self, inputtext):
        buffer = collections.deque()
        stack = collections.deque()
        print('Input Sentence:')
        for line in inputtext:
            line = line.rstrip()
            token, pos = line.split('/')
            buffer.append(TokenPos(token, pos))
            print(line, end=' ')
        print('\n\nParsing Actions and Transitions:\n')

        while(len(stack) > 0 or len(buffer) > 0):
            self.printqueue(stack)
            print(' ', end='')
            self.printqueue(buffer)

            if len(stack) < 2 and len(buffer) >= 1:
                stack.append(buffer.popleft())
                print(' SHIFT', end='')
            elif len(stack) <= 1 and len(buffer) < 1:
                root = stack.pop()
                print(' Root --> ' + root.str())
            else:
                second = stack.pop()
                first = stack.pop()

                if first.pos[0] == 'V' and (second.pos[0] == '.' or second.pos[0] == 'R'):
                    print(' Right-Arc: ' + first.str() + ' --> ' + second.str(), end='')
                    stack.append(first)
                elif len(stack) > 0 and first.pos[0] == 'I' and second.pos[0] == '.':
                    print(' SWAP', end='')
                    stack.append(second)
                    buffer.appendleft(first)
                elif len(buffer) > 0 and ((first.pos[0] == 'V' or first.pos[0] == 'I') and
                                          (second.pos[0] == 'D' or second.pos[0] == 'I' or
                                           second.pos[0] == "J" or second.pos[0] == 'P' or
                                           second.pos[0] == 'R')):
                    stack.append(first)
                    stack.append(second)
                    stack.append(buffer.popleft())
                    print(' SHIFT', end='')
                else:
                    left = -1
                    right = -1
                    if first.pos in self.leftarc and second.pos in self.leftarc[first.pos]:
                        left = self.leftarc[first.pos][second.pos]
                    if first.pos in self.rightarc and second.pos in self.rightarc[first.pos]:
                        right = self.rightarc[first.pos][second.pos]

                    if left > right:
                        print(' Left-Arc: ' + first.str() + ' <-- ' + second.str(), end='')
                        stack.append(second)
                    elif right > left:
                        print(' Right-Arc: ' + first.str() + ' --> ' + second.str(), end='')
                        stack.append(first)
                    elif left != -1 and right != -1:
                        print(' Left-Arc: ' + first.str() + ' <-- ' + second.str(), end='')
                        stack.append(second)
                    else:
                        stack.append(first)
                        stack.append(second)
                        stack.append(buffer.popleft())
                        print(' SHIFT', end='')
            print()

    def printqueue(self, queue):
        print('[', end='')
        first = True
        for i, node in enumerate(queue):
            if first:
                first = False
            else:
                print(',', end='')
            print(' ' + node.str(), end='')
        print(']', end='')

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

class TokenPos:
    def __init__(self, token, pos):
        self.token = token
        self.pos = pos

    def str(self):
        return self.token + '/' + self.pos

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
