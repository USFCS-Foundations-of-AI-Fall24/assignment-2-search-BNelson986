from queue import PriorityQueue
import docx

import Graph

dest = "8,8"
src = "1,1"

mars_graph = Graph.Graph()

class map_state() :
    ## f = total estimated cost
    ## g = cost so far
    ## h = estimated cost to goal
    def __init__(self, location="", mars_graph=None,
                 prev_state=None, g=0,h=0):
        self.location = location
        self.mars_graph = mars_graph
        self.prev_state = prev_state
        self.g = g
        self.h = h
        self.f = self.g + self.h

    def __eq__(self, other):
        return self.location == other.location

    def __hash__(self):
        return hash(self.location)

    def __repr__(self):
        return "(%s)" % (self.location)

    def __lt__(self, other):
        return self.f < other.f

    def __le__(self, other):
        return self.f <= other.f

    def is_goal(self):
        return self.location == '1,1'


def a_star(start_state, heuristic_fn, goal_test, use_closed_list=True) :
    search_queue = PriorityQueue()
    closed_list = {}
    search_queue.put(start_state)
    ## you do the rest.


## default heuristic - we can use this to implement uniform cost search
def h1(state) :
    return 0

## you do this - return the straight-line distance between the state and (1,1)
def sld(state) :
    '''sqt(a^ + b2)'''

## you implement this. Open the file filename, read in each line,
## construct a Graph object and assign it to self.mars_graph().
def read_mars_graph(filename):
    doc = docx.Document(filename)

    row_num = 8

    for table in doc.tables:
        for row in table.rows:
            cell_num = 1
            for cell in row.cells:
                # Inaccessible cells have no text
                if cell.text != '':
                    # Add the cell to the graph
                    node_index = f"{row_num},{cell_num}"
                    mars_graph.add_node(Graph.Node(node_index))

                    # Check for Horizontal edges
                    if cell_num > 1:
                        prev_node_index = f"{row_num},{cell_num-1}"

                        # Add undirected edge if the previous node exists
                        if mars_graph.has_node(prev_node_index):
                            mars_graph.add_edge(Graph.Edge(prev_node_index, node_index))
                            mars_graph.add_edge(Graph.Edge(node_index, prev_node_index))

                    # Check for Vertical edges
                    if row_num < 8:
                        prev_node_index = f"{row_num+1},{cell_num}"

                        # Add undirected edge if the previous node exists
                        if mars_graph.has_node(prev_node_index):
                            mars_graph.add_edge(Graph.Edge(prev_node_index, node_index))
                            mars_graph.add_edge(Graph.Edge(node_index, prev_node_index))

                cell_num += 1
            row_num -= 1

    return mars_graph

if __name__ == '__main__':
    mars_graph = read_mars_graph("marsmap.docx")

    for i in range(1, 8):
        for j in range(1, 8):
            if mars_graph.get_node(f"{i},{j}"):
                print(mars_graph.get_node(f"{i},{j}").value)
                print(mars_graph.get_edges(f"{i},{j}"))