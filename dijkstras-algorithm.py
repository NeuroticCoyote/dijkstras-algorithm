import sys
from PySide import QtGui, QtCore


mode = {"T":"Train", "P":"Plane", "F":"Ferry" }

class Graph(object):
    def __init__(self, graph_dict={}):
        self.__graph_dict = graph_dict
        self.num_vertices = 0

    def vertices(self):
        return list(self.__graph_dict.keys())

    def edges(self):
        return self.__generate_edges()

    def addVertex(self, vertex):
        self.num_vertices = self.num_vertices + 1
        if vertex not in self.__graph_dict:
            self.__graph_dict[vertex] = []

    def addEdge(self, edge):
        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)
        if vertex1 in self.__graph_dict:
            self.__graph_dict[vertex1].append(vertex2)
        else:
            self.__graph_dict[vertex1] = [vertex2]
            
    def __contains__(self,n):
        return n in self.__graph_dict

    def __generate_edges(self):
        edges = []
        for vertex in self.__graph_dict:
            for neighbour in self.__graph_dict[vertex]:
                if {neighbour, vertex} not in edges:
                    edges.append({vertex, neighbour})
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self.__graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res
    
    def findAllPaths(self, start_vertex, end_vertex, path=[]):
        graph = self.__graph_dict 
        path = path + [start_vertex]
        if start_vertex == end_vertex:
            return [path]
        if start_vertex not in graph:
            return []
        paths = []
        for vertex in graph[start_vertex]:
            if vertex not in path:
                extended_paths = self.findAllPaths(vertex, end_vertex, path)
                for p in extended_paths: 
                    paths.append(p)
        return paths

class Vertex(object):
    def __init__(self, vertex):
        self.id = vertex
        self.adjacent = {}
        
    def addNeighbor(self, neighbor, route):
        self.adjacent[neighbor] = route

    def __str__(self): 
        return str(self.id) + ' adjacent: ' + str([x.id for x in self.adjacent])

    def getConnections(self):
        return self.adjacent.keys()  

    def getId(self):
        return self.id

    def getWeight(self, neighbor):
        return self.adjacent[neighbor]

class Edge(object):
    def __init__(self, type, cost, distance):
        self.type = type
        self.cost = cost
        self.distance = distance
        
           
testOperformance = Graph()
testOperformance.addVertex("Vertex1")  
print(testOperformance)                   
"""method addVertex checks to see if vertex is present in the graph.
if vertex does not exist, add it to the graph, therefore function has complexity
O(n), as it checks the n number of items in the graph before adding a new vertex, in this case, there are 0 vertices
so the method simply adds the vertex to the graph"""
testOperformance.addVertex("Vertex2")   
print(testOperformance)                                        
"""the method now checks 1 vertex, and then adds it if the vertex does not exist"""
testOperformance.addVertex("Vertex3")   
print(testOperformance)
"""the method now checks 2 vertices, and then adds it if the vertex does not exist, we can now see the 0(n) pattern"""

if __name__ == "__main__":
    
    graphType  = { "Stoke" : {"London": mode["T"]},
          "London" : {"Stoke": mode["T"], "Berlin":mode["P"], "Rome":mode["P"], "Dover":  mode["T"]},
          "Berlin" : {"Rome": mode["P"], "Rome": mode["T"], "London": mode["P"]},
          "Rome" : {"Berlin":mode["T"], "London":mode["P"], "Calais":mode["T"]},
          "Dover" : {"London":mode["T"], "Calais":mode["F"]},
          "Calais" : {"Rome":mode["T"], "Dover":mode["F"]}
        }

    graphCost = { "Stoke" : {"London": 100},
          "London" : {"Stoke":100, "Berlin":200, "Rome":120, "Dover":50},
          "Berlin" : {"Rome":160, "Rome":120, "London":200},
          "Rome" : {"Berlin":120, "London":120, "Calais":250},
          "Dover" : {"London":50, "Calais":50},
          "Calais" : {"Rome":250, "Dover":50}
        }
        
    graphTime = { "Stoke" : {"London":90},
          "London" : {"Stoke":90, "Berlin":90, "Rome":90, "Dover":40},
          "Berlin" : {"Rome":110, "Rome":180, "London":90},
          "Rome" : {"Berlin":180, "London":90, "Calais":240},
          "Dover" : {"London":40, "Calais":35},
          "Calais" : {"Rome":240, "Dover":35}
        }
        
    maingraph = Graph(graphTime)

print("Vertices of graph:")
print(maingraph.vertices())
print("")
print("Edges of graph:")
print(maingraph.edges())
print("")
print("All paths from Stoke to Rome: ")
print( maingraph.findAllPaths( "Stoke", "Rome" ))
print("")

class GuiClass(QtGui.QMainWindow):  
    def __init__(self):
        super(GuiClass, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.startvertex = None
        self.endvertex = None

        self.setGeometry(	250, 250, 400, 350)
        self.setWindowTitle("Travel Planning")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setMouseTracking(True)

        self.intro = QtGui.QLabel("Select a start destination, end destination, then a path. Then press OK.", self)
        self.intro.resize(500, 12)
        self.intro.move(5, 2)
        self.label1 = QtGui.QLabel("Start Destination:", self)
        self.label1.move(5, 10)
        self.label2 = QtGui.QLabel("End Destination:", self)
        self.label2.move(100, 10)
        self.label6 = QtGui.QLabel("               ", self)
        self.label6.move(280, 250)

        cancelButton = QtGui.QPushButton('Exit', self)
        cancelButton.clicked.connect(self.onCancel)
        cancelButton.setAutoDefault(True)
        cancelButton.move(280, 300)
               
        endvertex=QtGui.QListWidget(self)
        for end_text in ["Stoke", "London", "Berlin", "Rome", "Dover", "Calais"]:
            end = QtGui.QListWidgetItem(end_text)
            endvertex.addItem(end)     
        endvertex.resize(60,120)
        endvertex.move(110, 35)    
        endvertex.itemClicked.connect(self.end_click)
                
        self.resultbox=QtGui.QTextEdit(self)
        self.resultbox.resize(250,150)
        self.resultbox.move(15, 180) 
        
        fastestButton = QtGui.QPushButton('Fastest Path', self)
        fastestButton.clicked.connect(self.onfastest)
        fastestButton.move(230, 35)

        cheapestButton = QtGui.QPushButton('Cheapest Path', self)
        cheapestButton.clicked.connect(self.oncheapest)
        cheapestButton.move(230, 65)

        startvertex=QtGui.QListWidget(self)   #major shortcoming with selecting of starting vertex, see report below
        for start_text in ["Stoke", "London", "Berlin", "Rome", "Dover", "Calais"]:
            start = QtGui.QListWidgetItem(start_text)
            startvertex.addItem(start)     
        startvertex.resize(60,120)
        startvertex.move(15, 35)    
        startvertex.itemClicked.connect(self.start_click)

        self.show()

    def onCancel(self):
        self.close()
        
    def onfastest(self):
            self.resultbox.append("The FASTEST path from " + self.startvertex + " to " + self.endvertex + " is the following route and TIME in MINUTES: ")
            resultfast = fastestPath(graphTime, self.startvertex, self.endvertex, visited=[])
            self.resultbox.append(str(resultfast))
            self.resultbox.append(" ")
    
    def oncheapest(self):
            self.resultbox.append("The CHEAPEST path from " + self.startvertex + " to " + self.endvertex + " is the following route and COST in POUNDS: ")
            resultcheap = cheapestPath(graphCost, self.startvertex, self.endvertex, visited=[])
            self.resultbox.append(str(resultcheap))
            self.resultbox.append(" ")
            
    def start_click(self,start):
        self.startvertex = start.text()
        
    def end_click(self,end):
        self.endvertex = end.text()
     
    def mouseMoveEvent(self,event):
        self.label6.setText("X: "+str(event.x()) + " Y: "+str(event.y()))

def fastestPath(G1,start_vertex,end_vertex,visited=[],distances={},predecessors={}):
    if not visited: distances[start_vertex]=0
    if start_vertex==end_vertex:
        path=[]
        pred=end_vertex
        while end_vertex != None:
            path.append(end_vertex)
            end_vertex=predecessors.get(end_vertex,None)
        return distances[start_vertex], path[::-1]
    else :     
        if not visited: distances[start_vertex]=0
        for neighbor in G1[start_vertex] :
            if neighbor not in visited:
                new_distance = distances[start_vertex] + G1[start_vertex][neighbor]
                if new_distance < distances.get(neighbor,float('inf')):
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = start_vertex
        visited.append(start_vertex)
        unvisited={}
        for k in G1:
            if k not in visited:
                unvisited[k] = distances.get(k,float('inf'))        
        x=min(unvisited, key=unvisited.get)
        return fastestPath(G1,x,end_vertex,visited,distances,predecessors)

def cheapestPath(G2,start_vertex,end_vertex,visited=[],distances={},predecessors={}):
    if not visited: distances[start_vertex]=0
    if start_vertex==end_vertex:
        path=[]
        pred=end_vertex
        while end_vertex != None:
            path.append(end_vertex)
            end_vertex=predecessors.get(end_vertex,None)
        return distances[start_vertex], path[::-1]
    else :     
        if not visited: distances[start_vertex]=0
        for neighbor in G2[start_vertex] :
            if neighbor not in visited:
                new_distance = distances[start_vertex] + G2[start_vertex][neighbor]
                if new_distance < distances.get(neighbor,float('inf')):
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = start_vertex
        visited.append(start_vertex)
        unvisited={}
        for k in G2:
            if k not in visited:
                unvisited[k] = distances.get(k,float('inf'))        
        x=min(unvisited, key=unvisited.get)
        return cheapestPath(G2,x,end_vertex,visited,distances,predecessors)

global userCancelled, userOK
userCancelled		= "Cancelled"
userOK			= "OK"


app = QtGui.QApplication(sys.argv)
form = GuiClass()

print(cheapestPath(graphCost, "Stoke", "Rome"))
print(fastestPath(graphTime, "Berlin", "Calais"))
