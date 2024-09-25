from queue import PriorityQueue
import docx
from math import sqrt

import Graph

src = "8,8"
dest = "1,1"

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
    """
    Perform an A* search to find the shortest path from start_state to the goal state.

    Parameters
    ----------
    start_state : map_state
        The starting state of the search.
    heuristic_fn : function
        A function that takes a state and returns an estimated cost to the goal.
    goal_test : function
        A function that takes a state and returns a boolean indicating whether the state is a goal state.
    use_closed_list : boolean
        If true, use a closed list to keep track of visited states and prevent revisiting them.

    Returns
    -------
    result :
        num_states: int
            The number of states visited during the search.
    """
    search_queue = PriorityQueue()
    closed_list = {}
    search_queue.put(start_state)
    num_states = 0

    while not search_queue.empty() :
        curr_state = search_queue.get()

        # Check if goal reached
        if goal_test(curr_state) :
            return curr_state, num_states

        if use_closed_list :
            closed_list[curr_state.location] = curr_state.g

        next_states = curr_state.mars_graph.get_edges(curr_state.location)
        num_states += len(next_states)

        for edge  in next_states :
            next_loc = edge.dest
            cost = edge.val

            if next_loc in closed_list :
                continue

            g = curr_state.g + cost
            h = heuristic_fn(map_state(next_loc, curr_state.mars_graph))

            search_queue.put(map_state(next_loc, curr_state.mars_graph, curr_state, g, h))

    return None, num_states

## default heuristic - we can use this to implement uniform cost search
def h1(state) :
    return 0

## you do this - return the straight-line distance between the state and (1,1)
def sld(state) :
    """
    Calculate the straight line distance from the state to the charger location (1,1).

    Parameters
    ----------
    state : map_state
        The state for which to calculate the distance.

    Returns
    -------
    dist : int
        The straight line distance from the state to (1,1).
    """
    p2 = [1,1]
    p1 = list(map(float, state.location.split(",")))

    # Calculate the straight line distance between p1 and p2
    return int (sqrt((float(p2[0]) - float(p1[0]))**2 + (float(p2[1]) - float(p1[1]))**2))

## you implement this. Open the file filename, read in each line,
## construct a Graph object and assign it to self.mars_graph().
def read_mars_graph(filename):
    """
    Read a .docx file and create a Graph object.

    Parameters
    ----------
    filename : str
        The name of the file to read.

    Returns
    -------
    Graph
        The constructed Graph object.
    """
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

def print_solutions() :
    mars_graph = read_mars_graph("marsmap.docx")

    start_state = map_state(location=src, mars_graph=mars_graph, prev_state=None,
                            g=0, h=sld(map_state(src, mars_graph)))

    result, num_states = a_star(start_state=start_state, heuristic_fn=sld, goal_test=map_state.is_goal)

    print("Final State: ", result)
    print("States needed to reach goal: ", num_states)


if __name__ == '__main__':
    mars_graph = read_mars_graph("marsmap.docx")

    start_state = map_state(location=src, mars_graph=mars_graph, prev_state=None,
                            g=0, h=sld(map_state(src, mars_graph)))

    result, num_states = a_star(start_state=start_state, heuristic_fn=sld, goal_test=map_state.is_goal)

    print("Final State: ", result)
    print("States needed to reach goal: ", num_states)

    '''for i in range(1, 8):
        for j in range(1, 8):
            if mars_graph.has_node(f"{i},{j}"):
                print(mars_graph.has_node(f"{i},{j}").value)
                print(mars_graph.get_edges(f"{i},{j}"))'''