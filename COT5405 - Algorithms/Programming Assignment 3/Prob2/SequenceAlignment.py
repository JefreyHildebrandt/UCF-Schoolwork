# author: Jeff Hildebrandt
class SequenceAlignment:
    def __init__(self, m, n, gap, mis):
        self.m = m
        self.n = n
        self.gap = gap
        self.mis = mis
        self.choices = [[0 for x in range(len(n) + 1)] for y in range(len(m) + 1)]
        self.M = [[0 for x in range(len(n) + 1)] for y in range(len(m) + 1)]
        curgap = 0
        for x in range(len(m), -1, -1):
            self.M[x][len(n)] = curgap
            curgap += gap
        curgap = 0
        for y in range(len(n), -1, -1):
            self.M[len(m)][y] = curgap
            curgap += gap

    def start(self):
        self.populateMatrix()
        self.printSolution()

    def populateMatrix(self):
        for i in range(len(self.m) - 1, -1, -1):
            for j in range(len(self.n) - 1, -1, -1):
                self.M[i][j] = self.findMin(i, j, "min")
                self.choices[i][j] = self.findMin(i, j, "choices")

    def printSolution(self):
        x = 0
        y = 0
        choiceIndex = len(self.choices) - 1
        sol1 = ""
        sol2 = ""
        cost = 0
        while(x < len(self.m) or y < len(self.n)):
            retVal = self.choices[x][y]

            if (x >= len(self.m)):
                sol1 += "-"
                sol2 += self.n[y]
                cost += self.gap
                y += 1
                continue
            if (y >= len(self.n)):
                sol1 += self.m[x]
                sol2 += "-"
                cost += self.gap
                x += 1
                continue

            if(retVal == 0):
                if (self.m[x] != self.n[y]):
                    cost += self.mis
                    sol1 += "["
                    sol2 += "["
                sol1 += self.m[x]
                sol2 += self.n[y]
                if(self.m[x] != self.n[y]):
                    sol1 += "]"
                    sol2 += "]"
                x += 1
                y += 1
            elif(retVal == 1):
                sol1 += self.m[x]
                sol2 += "-"
                x += 1
                cost += self.gap
            elif(retVal == 2):
                sol1 += "-"
                sol2 += self.n[y]
                y += 1
                cost += self.gap
            choiceIndex -= 1
        print(sol1)
        print(sol2)
        print("cost: ", cost)

    def findMin(self, i, j, ret):
        xiyi = self.M[i + 1][j + 1]

        if self.m[i] != self.n[j]:
            xiyi += self.mis

        retop = 0
        min = xiyi
        xi = self.gap + self.M[i + 1][j]
        yi = self.gap + self.M[i][j + 1]
        if xi < min:
            min = xi
            retop = 1
        if yi < min:
            min = yi
            retop = 2

        self.choices.append(retop)

        if(ret == "min"):
            return min
        else:
            return retop

def main():
    m = ["A","G","G","C","T","A","T","C","A","C","C","T","G","A","C","C","T","C","C","A","G","G","C","C","G","A","T","G","C","C","C"]
    n = ["T","A","G","C","T","A","T","C","A","C","G","A","C","C","G","C","G","G","T","C","G","A","T","T","T","G","C","C","C","G","A","C"]
    gap = 1
    mis = 2

    sequenceAlignment = SequenceAlignment(m, n, gap, mis)
    sequenceAlignment.start()
main()