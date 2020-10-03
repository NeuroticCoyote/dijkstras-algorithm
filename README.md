# dijkstras-algorithm

## How to run
apt-get install python3-pyside
python3 dijkstras-algorithm.py

If there are issues connecting to X server:
apt install xvfb
xvfb-run python3 dijkstras-algorithm.py

## Introduction
This implementation is one of three classes: graph, vertex and edge. The import sys
library had to be imported in order to carry out the fastest and cheapest path algorithms. A dictionary named "mode"
was used to simplify the process of having to type "train", "ferry" and "plane".

Note that the graph class has functions such as vertices and edges, and this is merely to report all of the
vertices and edges that are in the graph.

The findAllPaths function was implemented to help visualise all of the different paths that are available from
one vertex to another. This helped the process for finding the cheapest and shortest path methods.

Three distint graphs were implemented, one for the type of transport, the cost and the time 
it took to get from one vertex to another. These were called graphType, graphCost and graphTime respectively. 
An instance of one of the graphs was created called "maingraph", and this was to help discover what vertices
exist, all of the possible edges that exist as well as all the paths that exist from one vertex to another.

Originally, only one method was created called shortestPath, but there were some complications when asking to 
find the shortest route for two separate graphs: graphCost and graphDistance. Note that graphType was ignored. The issue was after it found the shortest path for one
graph, it would produce the SAME answer regardless if you asked it to find the shortest path for the other
graph mentioned above. So I needed to find a way of resetting most of the variables and memory of the paths
that the method had found. This was proven complicated. Instead, the same method was duplicated, but altered 
slightly to cater to two separate types of graph data. Therefore, cheapestPath was created for graphCost, and
fastestPath was created for graphTime. Below is an example of the issue I had before creating two separate 
method:

def shortestPath(G1,start_vertex,end_vertex,visited=[],distances={},predecessors={}):
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
        return shortestPath(G1,x,end_vertex,visited,distances,predecessors)

print(shortestPath(graphCost, "Stoke", "Rome", visited=[]))
print(shortestPath(graphTime, "Stoke", "Rome", visited=[]))
print(shortestPath(graphTime, "Berlin", "Calais", visited=[]))

After running the above code, the error lies in the third print line, with the result as:
(165, ['Stoke', 'London', 'Dover', 'Calais'])
We do not want this, we want from Berlin to Calais. The issue lies with resetting former states and
memory which I had difficulty doing.

The gui was more straight forward in the sense of creating objects, resizing them and positioning them in 
certain locations. The harder challenge was recognising the two selected inputs from the two lists, 
and placing them in the method call that was placed behind the two buttons. In the end, the variables
self.startvertex and self.endvertex were the two "clicked" items in the list, and these were then passed
as parameters to the method call behind each button. These are shown in the onfastest and oncheapest method
calls. These are executed once the buttons have been clicked.

Finally, if we extend the graph and add more vertices (towns and cities). The algorithm would remain intact, 
and the functions would still work. The only extra bit of work we need to do is to update the lists in the gui 
so they hold information on all of the vertices. Developing the cude further for future work, teh list could 
automatically update itself as it would recogise the vertices in the graph by a method.




















