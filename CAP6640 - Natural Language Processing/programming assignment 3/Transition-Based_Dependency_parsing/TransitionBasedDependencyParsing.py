import os, sys

class TransitionBasedDependencyParsing:
    def __init__(self, corpus, inputtext):
        self.corpus = corpus
        self.inputtext = inputtext

    def parsecorpus(self):
        sentences = 0
        tokens = set()
        postokens = set()
        left
        for line in corpus:
            pass


if __name__== "__main__":
    print("University of Central Florida")
    print("CAP6640 Spring 2018 - Dr. Glinos\n")
    print("Dependency Parser by Jeff Hildebrandt\n\n")

    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    corpus = open(os.path.join(__location__, 'wsj-dep.txt'), 'r')
    inputtext = open(sys.argv[1], 'r')

    transition = TransitionBasedDependencyParsing(corpus, inputtext)
