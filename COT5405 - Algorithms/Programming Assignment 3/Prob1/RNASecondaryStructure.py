# author: Jeff Hildebrandt
class RnaSecondaryStructure:
    def __init__(self, molecule):
        self.molecule = molecule
        self.y =  int(len(molecule) / 2)
        self.x = self.y
        self.kStart = int(len(molecule) / 2) + 1
        if len(molecule) % 2 == 0:
            self.x -= 1
        self.M = [[0 for x in range(self.x)] for y in range(self.y)]
        self.n = len(molecule)
    def start(self):
        for k in range(self.kStart, self.n):
            for i in range(self.n - k):
                j = i + k
                self.M[i][j - self.kStart] = self.computeM(i, j)
        backwards = len(self.M)
        for i in reversed(self.M):
            if backwards / 10 < 1:
                print(" ", end="")
            print(backwards, "| ", end="")
            for j in i:
                print(j, "  ", end="")
            print()
            backwards -= 1
        print("   ", end="")
        for i in range(self.kStart + 1, self.n + 1):
            print("----", end="")
        print()
        print("    ", end="")
        for i in range(self.kStart + 1, self.n + 1):
            if i / 10 < 1:
                print(" ", end="")
            print(i, " ", end="")

    def computeM(self, i, j):
        if i >= j-4:
            return 0

        max = 0
        if not self.isPair(i, j):
            max = self.OPT(i, j-1)

        for t in range(i, j-4):
            if self.isPair(t, j):
                cur = 1 + self.OPT(i, t-1) + self.OPT(t+1, j-1)
                if cur > max:
                    max = cur
        return max

    def isPair(self, i, j):
        bi = self.molecule[i]
        bj = self.molecule[j]
        return (bi == "A" and bj == "U") or (bi == "U" and bj == "A") or (bi == "C" and bj == "G") or (bi == "G" and bj == "C")

    def OPT(self, i, j):
        if (j - self.kStart < 0 or j - self.kStart >= self.x or i < 0 or i >= self.y):
            return 0
        return self.M[i][j - self.kStart]
def main():
    molecule = ["A","U","G","G","C","U","A","C","C","G","G","U","C","G","A","U","U","G","A","G","C","G","C","C","A","A","U","G","U","A","A","U","C","A","U","U"]
    rnaSecondaryStructure = RnaSecondaryStructure(molecule)
    rnaSecondaryStructure.start()
main()
#http://math.mit.edu/classes/18.417/Slides/rna-prediction-nussinov.pdf