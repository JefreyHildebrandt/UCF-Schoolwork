from sys import maxsize

class SequenceAlignment:
    def __init__(self, m, n, gap, mis):
        self.m = m
        self.n = n
        self.gap = gap
        self.min = mis
        self.M = [[gap for x in range(len(m) + 1)] for y in range(len(n) + 1)]

    def start(self):
        for i in range(len(self.m)):
            for j in range(len(self.n)):
                self.M[i][j] = self.findMin(i, j)
        print(self.M)

    def findMin(self, i, j):
        if m[i] == n[j]:
            pass
        return self.gap

def main():
    m = ["o","c","u","r","r","a","n","c","e"]
    n = ["o","c","c","u","r","r","e","n","c","e"]
    gap = 1
    mis = 2
    sequenceAlignment = SequenceAlignment(m, n, gap, mis)
    sequenceAlignment.start()
main()