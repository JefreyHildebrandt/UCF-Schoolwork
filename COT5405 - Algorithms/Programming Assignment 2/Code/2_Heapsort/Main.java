import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.*;

public class Main {
    public static void main(String[] args) {
        boolean readableFile = false;
        int selection = 0;
        try {
            while(!readableFile) {
                if (args != null && args.length > 0) {
                    System.out.println("Processing the file " + args[0]);
                    try {
                        if(args.length > 1) {
                            selection = Integer.parseInt(args[1]);
                            if(selection == 0) {
                                System.out.println("Running Heap sort, Shortest Path, and Minimum Spanning Tree");
                            }
                            else if(selection == 1) {
                                System.out.println("Running Heap Sort");
                            }
                            else if(selection == 2) {
                                System.out.println("Running Shortest Path");
                            }
                            else if(selection == 3) {
                                System.out.println("Running Minimum Spanning Tree");
                            }
                        }
                    }
                    catch(NumberFormatException e) {
                        System.out.println("Running Heap sort, Shortest Path, and Minimum Spanning Tree");
                    }
                    ProgrammingAssignmentTwo pA = new ProgrammingAssignmentTwo(selection);
                    readableFile = pA.start(args[0]);
                }
                else {
                    Scanner reader = new Scanner(System.in);
                    System.out.println("Enter the name of a file in the directory " + Paths.get(".").toAbsolutePath().normalize().toString());
                    String fileChoice = reader.next();
                    System.out.println("Select what program to run:");
                    System.out.println("0: Run all");
                    System.out.println("1: Heap sort");
                    System.out.println("2: Shortest Path");
                    System.out.println("3: Minimum Spanning Tree");

                    while(true) {
                        String theSelection = reader.next();
                        try {
                            selection = Integer.parseInt(theSelection);
                            if(selection >= 0 && selection <= 3) {
                                break;
                            }
                        }
                        catch(NumberFormatException e) {
                            System.out.println("Please enter a number 0-3.");
                        }
                    }
                    reader.close();
                    System.out.println(fileChoice);
                    ProgrammingAssignmentTwo pA = new ProgrammingAssignmentTwo(selection);
                    readableFile = pA.start(fileChoice);
                }
            }
        }
        catch(Exception e) {
            System.out.println(e);
        }
    }
}

class ProgrammingAssignmentTwo {
    int selection;
    ProgrammingAssignmentTwo(int selection) {
        this.selection = selection;
    }
    public boolean start(String fileName) throws Exception {
        String line = null;

        // FileReader reads text files in the default encoding.
        FileReader fileReader =
                new FileReader(fileName);

        // Always wrap FileReader in BufferedReader.
        BufferedReader bufferedReader =
                new BufferedReader(fileReader);

        List<AdjNode> adjArrayList = new ArrayList<AdjNode>();
        int lineCount = 0;
        while((line = bufferedReader.readLine()) != null) {
            lineCount++;
            String[] adj = line.split(",");
            if(adj.length > 1) {
                String nodeName = adj[0].trim();
                AdjNode curNode = new AdjNode(nodeName);
                for(int i=1; i<adj.length; i++) {
                    String trimmedAdj = adj[i].trim();
                    String[] nodeInfo = trimmedAdj.split("\\s+");
                    if(nodeInfo.length == 2) {
                        try {
                            Edge edge = new Edge(nodeInfo[1], Integer.parseInt(nodeInfo[0]));
                            curNode.adjNodes.add(edge);
                        }
                        catch(java.lang.NumberFormatException e){
                            System.out.println("There was an error parsing line number: " + lineCount);
                            System.out.println("\"" + line + "\"");
                            System.out.println("=> \"" + trimmedAdj + "\"");
                            System.out.println("=> \"" + nodeInfo[0] + "\" is not an integer");
                            return true;
                        }
                    }
                    else {
                        System.out.println("There was an error parsing line number: " + lineCount);
                        System.out.println("\"" + line + "\"");
                        System.out.println("=> \"" + trimmedAdj + "\"");
                        System.out.println("=> There should only be two inputs.");
                        return true;
                    }
                }
                adjArrayList.add(curNode);
            }
            else if(adj.length == 1) {
                String nodeName = adj[0].trim();
                AdjNode curNode = new AdjNode(nodeName);
                adjArrayList.add(curNode);
            }
        }
        bufferedReader.close();
        AdjNode[] adjList = adjArrayList.toArray(new AdjNode[adjArrayList.size()]);

        boolean badAdjList = isBadAdjList(adjList);
        if(badAdjList) {
            return true;
        }
        // calls the questions for the assignment
        //Question 1
        if(selection == 1 || selection == 0) {
            heapSort(adjList);
        }

        //Question 2
        if(selection == 2 || selection == 0) {
            shortestPath(adjList);
        }

        //Question 3
        if(selection == 3 || selection == 0) {
            minimumSpanningTree(adjList);
        }

        return true;
    }

    private boolean isBadAdjList(AdjNode[] adjList) {
        HashMap<String, HashSet<String>> allNodes = new HashMap<>(adjList.length);
        // makes sure the same node isn't defined more than once
        for(AdjNode curNode: adjList) {
            if(allNodes.containsKey(curNode.nodeName)) {
                System.out.println("Error: Node " + curNode.nodeName + " is defined more than once in the input file.");
                return true;
            }
            HashSet<String> adjNodes = new HashSet<>(curNode.adjNodes.size());
            for(Edge curEdge: curNode.adjNodes) {
                adjNodes.add(curEdge.nodeName);
            }
            allNodes.put(curNode.nodeName, adjNodes);
        }

        for(AdjNode curNode: adjList) {
            for(Edge curEdge: curNode.adjNodes) {
                // makes sure every node links to a defined node
                if(!allNodes.containsKey(curEdge.nodeName)) {
                    System.out.println("Error Invalid Input: Node \"" + curEdge.nodeName + "\" does not link to defined node.");
                    System.out.println("The following nodes are okay from the given input:");
                    for(String nodeName: allNodes.keySet()) {
                        System.out.print(nodeName + " ");
                    }
                    System.out.println();
                    return true;
                }
            }
        }

        return false;
    }

    public void heapSort(AdjNode[] adjList) {
        Integer[] sortArray = adjNodeToArray(adjList);
        System.out.println("Heap Sort:");
        System.out.println("Initial Array:");
        printSortArray(sortArray);
        System.out.println();
        // this turns the array into a heap array
        // checks each parent node ensures it's larger than its children
        for(int i=sortArray.length/2 - 1; i>-1; i--) {
            heapify(sortArray, sortArray.length, i);
        }
        System.out.println("After initial heapify:");
        printSortArray(sortArray);
        System.out.println();
        for(int i=sortArray.length-1; i>-1; i--) {
            Integer swapVal = sortArray[0];
            sortArray[0] = sortArray[i];
            sortArray[i] = swapVal;

            heapify(sortArray, i, 0);
        }
        System.out.println("The final sorted array:");
        printSortArray(sortArray);
        System.out.println("\n");
    }

    private void printSortArray(Integer[] sortArray) {
        System.out.print("[");
        for(int i=0; i<sortArray.length; i++) {
            System.out.print(sortArray[i]);
            if(i != sortArray.length - 1) {
                System.out.print(", ");
            }
        }
        System.out.print("]");
    }

    private Integer[] adjNodeToArray(AdjNode[] adjList) {
        HashSet<String> seeIfExist = new HashSet<>();
        List<Integer> sortArray = new ArrayList<>();
        for(int i=0; i<adjList.length; i++) {
            String atNode = adjList[i].nodeName;
            for(Edge edge : adjList[i].adjNodes) {
                if(seeIfExist.contains(atNode + edge.nodeName) || seeIfExist.contains(edge.nodeName + atNode)) {
                    continue;
                }
                else {
                    seeIfExist.add(atNode + edge.nodeName);
                    sortArray.add(edge.weight);
                }
            }
        }
        return sortArray.toArray(new Integer[sortArray.size()]);
    }

    private void heapify(Integer[] sortArray, int size, int node) {
        // loops until the node and it's children are heapified
        while(true) {
            int curLargest = node;
            int leftChild = node * 2 + 1;
            int rightChild = node * 2 + 2;

            if(leftChild < size && sortArray[leftChild] > sortArray[curLargest]) {
                curLargest = leftChild;
            }
            if( rightChild < size && sortArray[rightChild] > sortArray[curLargest]) {
                curLargest = rightChild;
            }
            if(curLargest != node) {
                // swaps the largest node for the current node in the array
                Integer swapVal = sortArray[node];
                sortArray[node] = sortArray[curLargest];
                sortArray[curLargest] = swapVal;
                node = curLargest;
            }
            else {
                break;
            }
        }
    }

    public void shortestPath(AdjNode[] adjList) {
        class Distances {
            int distance;
            AdjNode node;
            Distances(int distance, AdjNode node) {
                this.distance = distance;
                this.node = node;
            }
        }
        // starts at the first node every time
        int startingNode = 0;

        HashMap<String, AdjNode> getAdjNode = new HashMap<>(adjList.length);
        HashMap<String, Integer> dist = new HashMap<>(adjList.length);
        HashMap<String, String> prev = new HashMap<>(adjList.length);

        PriorityQueue<Distances> distances = new PriorityQueue<Distances>(adjList.length, new Comparator<Distances>() {
            @Override
            public int compare(Distances x, Distances y) {
                return x.distance - y.distance;
            }
        });
        int maxVal = Integer.MAX_VALUE/2;
        for(int i=0; i<adjList.length; i++) {
            if(i == startingNode) {
                distances.add(new Distances(0, adjList[i]));
                dist.put(adjList[i].nodeName, 0);
                prev.put(adjList[i].nodeName, "Starting Node");
            }
            else {
                distances.add(new Distances(maxVal, adjList[i]));
                dist.put(adjList[i].nodeName, maxVal);
                prev.put(adjList[i].nodeName, "Node is unreachable");
            }
            getAdjNode.put(adjList[i].nodeName,adjList[i]);
        }
        while(!distances.isEmpty()) {
            Distances curMin = distances.remove();

            for(Edge curEdge : curMin.node.adjNodes) {
                int altDist = dist.get(curMin.node.nodeName) + curEdge.weight;
                if( altDist < dist.get(curEdge.nodeName)) {
                    dist.replace(curEdge.nodeName, altDist);
                    prev.replace(curEdge.nodeName, curMin.node.nodeName);
                    // adds new distances over the old distances.  So, this while loop runs O(2n) rather than O(n)
                    distances.add(new Distances(altDist, getAdjNode.get(curEdge.nodeName)));
                }
            }
        }
        // print output
        System.out.println("Shortest Path:");

        for(int i=0; i<adjList.length; i++) {
            String curName = adjList[i].nodeName;
            if(dist.get(curName) >= maxVal) {
                System.out.println("Destination Node " + curName + ": path value = INFINITY, path is: N/A");
                continue;
            }
            System.out.print("Destination Node " + curName + ": path value = " + dist.get(curName) + ", path is: ");
            ArrayList<String> backwardsPath = new ArrayList<>();
            while(true) {
                if(!prev.containsKey(curName)) {
                    break;
                }
                backwardsPath.add(curName);
                curName = prev.get(curName);
            }
            for(int j=backwardsPath.size()-1; j>=0; j--) {
                System.out.print(backwardsPath.get(j));
                if(j > 0) {
                    System.out.print(" -> ");
                }
            }
            System.out.println();
        }
        System.out.println();
    }

    public void minimumSpanningTree(AdjNode[] adjList) {
        PriorityQueue<NodeToNode> smallestEdge = adjNodeToPriorityQueue(adjList);
        ArrayList<HashSet<String>> subsets = new ArrayList<>(adjList.length);
        ArrayList<ArrayList<NodeToNode>> subsetEdges = new ArrayList<>(adjList.length);

        while(!smallestEdge.isEmpty()) {
            NodeToNode sml = smallestEdge.remove();
            int[] unionSets = new int[2];
            unionSets[0] = -1;
            unionSets[1] = -1;
            boolean isCircle = false;
            for(int i=0; i<subsets.size(); i++) {
                HashSet<String> set = subsets.get(i);
                if((set.contains(sml.startingNode) || set.contains(sml.endingNode)) && !(set.contains(sml.startingNode) && set.contains(sml.endingNode))) {
                    if(unionSets[0] == -1) {
                        unionSets[0] = i;
                    }
                    else if(unionSets[1] == -1) {
                        unionSets[1] = i;
                    }
                }
                if(set.contains(sml.startingNode) && set.contains(sml.endingNode)) {
                    isCircle = true;
                }
            }
            if(!isCircle) {
                if (unionSets[0] == -1 && unionSets[1] == -1) {
                    HashSet<String> set = new HashSet<>();
                    set.add(sml.startingNode);
                    set.add(sml.endingNode);
                    subsets.add(set);
                    ArrayList<NodeToNode> node = new ArrayList<>();
                    node.add(sml);
                    subsetEdges.add(node);
                } else if (unionSets[0] != -1 && unionSets[1] == -1) {
                    subsets.get(unionSets[0]).add(sml.startingNode);
                    subsets.get(unionSets[0]).add(sml.endingNode);
                    subsetEdges.get(unionSets[0]).add(sml);
                } else if (unionSets[0] != -1 && unionSets[1] != -1) {
                    subsets.get(unionSets[0]).addAll(subsets.get(unionSets[1]));
                    subsets.remove(unionSets[1]);
                    subsetEdges.get(unionSets[0]).add(sml);
                    subsetEdges.get(unionSets[0]).addAll(subsetEdges.get(unionSets[1]));
                    subsetEdges.remove(unionSets[1]);
                }
            }
        }
        // Prints the output
        for(int i=0; i<subsets.size(); i++) {
            HashSet<String> set = subsets.get(i);
            ArrayList<NodeToNode> edgeInSet = subsetEdges.get(i);
            System.out.print("Minimum Spanning Tree: Total weights on MST edges = ");

            System.out.print("Node Set = {");
            int count = 0;
            for(String setNode: set) {
                System.out.print(setNode);
                count++;
                if(count != set.size()) {
                    System.out.print(", ");
                }
            }
            System.out.print("), Edge Set = {");
            count = 0;
            for(NodeToNode edge: edgeInSet) {
                System.out.print(edge.startingNode + "-" + edge.endingNode);
                count++;
                if(count != edgeInSet.size()) {
                    System.out.print(", ");
                }
            }
            System.out.println("}");
        }

        System.out.println();
    }

    private PriorityQueue<NodeToNode> adjNodeToPriorityQueue(AdjNode[] adjList) {
        HashSet<String> seeIfExist = new HashSet<>();
        PriorityQueue<NodeToNode> priorityQueue = new PriorityQueue<>(new Comparator<NodeToNode>() {
            @Override
            public int compare(NodeToNode o1, NodeToNode o2) {
                return o1.weight - o2.weight;
            }
        });
        for(int i=0; i<adjList.length; i++) {
            String atNode = adjList[i].nodeName;
            for(Edge edge : adjList[i].adjNodes) {
                if(seeIfExist.contains(atNode + edge.nodeName) || seeIfExist.contains(edge.nodeName + atNode)) {
                    continue;
                }
                else {
                    seeIfExist.add(atNode + edge.nodeName);
                    priorityQueue.add(new NodeToNode(adjList[i].nodeName, edge.nodeName, edge.weight));
                }
            }
        }
        return priorityQueue;
    }

}

class AdjNode {
    String nodeName;
    LinkedList<Edge> adjNodes;

    AdjNode(String nodeName) {
        this.nodeName = nodeName;
        this.adjNodes = new LinkedList<Edge>();
    }
}
class Edge {
    String nodeName;
    Integer weight;
    Edge(String nodeName, Integer weight) {
        this.nodeName = nodeName;
        this.weight = weight;
    }
}
class NodeToNode {
    String startingNode;
    String endingNode;
    Integer weight;

    NodeToNode(String startingNode, String endingNode, Integer weight) {
        this.startingNode = startingNode;
        this.endingNode = endingNode;
        this.weight = weight;
    }
}
