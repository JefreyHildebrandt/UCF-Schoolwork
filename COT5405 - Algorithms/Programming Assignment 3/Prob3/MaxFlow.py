# author: Jeff Hildebrandt
from collections import deque
from sys import maxsize
from copy import deepcopy
class MaxFlow:
    def __init__(self, graph, s, t):
        self.graph = graph
        self.augPath = [-1] * len(self.graph)
        self.s = s
        self.t = t
        self.maxFlow = 0

    def start(self):
        self.fordFulkerson()
        self.printFlowGraph()

    def augment(self):
        # assumes the network columns and rows are even
        visitedNodes = [False] * len(self.graph)
        q = deque()
        q.append(self.s)
        visitedNodes[self.s] = True

        while q:
            y = q.popleft()

            for i, flow in enumerate(self.graph[y]):
                if visitedNodes[i] == False and flow > 0:
                    q.append(i)
                    visitedNodes[i] = True
                    self.augPath[i] =  y
        return visitedNodes[self.t]

    def fordFulkerson(self):
        while self.augment():
            capacity = maxsize / 2
            t = self.t
            while t != self.s:
                capacity = min(capacity, self.graph[self.augPath[t]][t])
                t = self.augPath[t]

            self.maxFlow += capacity

            cur = self.t
            while cur != self.s:
                self.graph[self.augPath[cur]][cur] -= capacity
                self.graph[cur][self.augPath[cur]] += capacity
                cur = self.augPath[cur]

    def printFlowGraph(self):
        print("max flow = ", self.maxFlow)
        print("Graph for max flow:")
        for i in range(len(self.graph)):
            for j in range(len(self.graph)):
                print(self.graph[i][j], " ", end="")
                if self.graph[i][j] / 10 < 1:
                    print(" ", end="")
            print()

def main():
    graph = [[0, 10, 5, 15, 0,  0,  0,  0],  # s
             [0,  0, 4,  0, 9, 15,  0,  0],  # 2
             [0,  0, 0,  4, 0,  8,  0,  0],  # 3
             [0,  0, 0,  0, 0,  0, 30,  0],  # 4
             [0,  0, 0,  0, 0, 15,  0, 10],  # 5
             [0,  0, 0,  0, 0,  0, 15, 10],  # 6
             [0,  0, 6,  0, 0,  0,  0, 10],  # 7
             [0,  0, 0,  0, 0,  0,  0,  0]]  # t
    s = 0
    t = 7

    MaxFlow(graph, s, t).start()
main()

