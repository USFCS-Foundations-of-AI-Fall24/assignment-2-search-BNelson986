## actions:
## pick up tool
## move_to_sample
## use_tool
## move_to_station
## drop_tool
## drop_sample
## move_to_battery
## charge

## locations: battery, sample, station
## holding_sample can be True or False
## holding_tool can be True or False
## Charged can be True or False

from copy import deepcopy

from search_algorithms import (breadth_first_search,
                               depth_first_search,
                               iterative_deepening_search)


class RoverState :
    def __init__(self, loc="station", holding_tool=False, sample_extracted=False, holding_sample=False, charged=False):
        self.loc = loc
        self.holding_tool = holding_tool
        self.sample_extracted = sample_extracted
        self.holding_sample = holding_sample
        self.charged = charged
        self.prev = None

    ## you do this.
    def __eq__(self, other):
        if not isinstance(other, RoverState):
            return False
        return (self.loc == other.loc and
                self.holding_tool == other.holding_tool and
                self.sample_extracted == other.sample_extracted and
                self.holding_sample == other.holding_sample and
                self.charged == other.charged)

    def __repr__(self):
        return (f"Location: {self.loc}\n" +
                f"Holding Tool?: {self.holding_tool}\n" +
                f"Sample Extracted?: {self.sample_extracted}\n"+
                f"Holding Sample?: {self.holding_sample}\n" +
                f"Charged? {self.charged}")

    def __hash__(self):
        return self.__repr__().__hash__()

    def successors(self, list_of_actions):

        ## apply each function in the list of actions to the current state to get
        ## a new state.
        ## add the name of the function also
        ## prevent addition of repeated states
        succ = [(item(self), item.__name__) for item in list_of_actions]

        ## remove actions that have no effect

        succ = [item for item in succ if not item[0] == self]
        return succ

## our actions will be functions that return a new state.

def move_to_sample(state) :
    r2 = deepcopy(state)
    r2.loc = "sample"
    r2.prev=state
    return r2
def move_to_station(state) :
    r2 = deepcopy(state)
    r2.loc = "station"
    r2.prev = state
    return r2

def move_to_battery(state) :
    r2 = deepcopy(state)
    r2.loc = "battery"
    r2.prev = state
    return r2
# add tool functions here

def pick_up_tool(state) :
    r2 = deepcopy(state)
    if not state.holding_tool and state.loc == "station":
        r2.holding_tool = True
    r2.prev = state
    return r2

def drop_tool(state) :
    r2 = deepcopy(state)
    if state.holding_tool and state.loc == "station":
        r2.holding_tool = False
    r2.prev = state
    return r2

def use_tool(state) :
    r2 = deepcopy(state)
    if not state.sample_extracted and state.loc == "sample" and state.holding_tool:
        r2.sample_extracted = True
        r2.holding_sample = True
    r2.prev = state
    return r2

def drop_sample(state) :
    r2 = deepcopy(state)
    if state.sample_extracted and state.loc == "station":
        r2.holding_sample = False
    r2.prev = state
    return r2

def charge(state) :
    r2 = deepcopy(state)
    if not state.charged and state.loc == "battery":
        r2.charged = True
    r2.prev = state
    return r2


action_list = [charge, pick_up_tool, drop_tool, use_tool, drop_sample,
               move_to_sample, move_to_battery, move_to_station]

def battery_goal(state) :
    return state.loc == "battery" and state.charged

def sample_goal(state) :
    return state.loc == "sample" and state.sample_extracted

def station_goal(state) :
    return (
        state.loc == "station" and
        state.sample_extracted and
        not state.holding_tool and
        not state.holding_sample
    )

def mission_complete(state) :
    """
    The mission is complete when the sample is dropped off at the station,
    rover is at the battery station, and the battery is fully charged.

    Parameters
    ----------
    state : RoverState
        Current state of the rover.

    Returns
    -------
    bool
        Is the mission complete?
    """
    sample_state = state.sample_extracted and not state.holding_sample
    
    return battery_goal(state) and state.charged and sample_state

## Starting states to break problem into 3 different parts
## Element layout:
## start_state_name: [
##     starting state,
##     goal test,
##     ]
sub_problems = {
    'get sample': [
        RoverState(
            loc="station",
            holding_tool=False,
            sample_extracted=False,
            holding_sample=False,
            charged=False
        ),
        sample_goal
    ],
    'drop sample': [
        RoverState(
            loc="sample",
            holding_tool=True,
            sample_extracted=True,
            holding_sample=True,
            charged=False
        ),
        station_goal
    ],
    'charge battery': [
        RoverState(
            loc="station",
            holding_tool=False,
            sample_extracted=True,
            holding_sample=False,
            charged=False
        ),
        battery_goal
    ]
}

if __name__=="__main__" :
    '''    ## BFS solution
    s = RoverState()
    result, states = breadth_first_search(s, action_list, mission_complete)
    print("BFS result:\n", result)
    print("States needed to reach goal: ", states)

    s = RoverState()
    ## DFS solution
    result, states = depth_first_search(s, action_list, mission_complete)
    print("DFS result:\n", result)
    print("States needed to reach goal: ", states)

    s = RoverState()
    ## DLS solution
    result, states = depth_first_search(s, action_list, mission_complete, limit=10)
    print("DLS result:\n", result)
    print("States needed to reach goal: ", states)

    s = RoverState()
    ## IDS solution
    result, states = iterative_deepening_search(s, action_list, mission_complete)
    print("IDS result:\n", result)
    print("States needed to reach goal: ", states)'''


    ## Sub problem Solutions - BFS
    print("Sub problem solutions:\n")
    print("BFS")
    for key, value in sub_problems.items() :
        result, states = breadth_first_search(value[0], action_list, value[1])
        print(key, " result:\n", result)
        print("States needed to reach goal: ", states)
        print("\n")


    ## Sub problem Solutions - DFS
    print("DFS")
    for key, value in sub_problems.items() :
        result, states = depth_first_search(value[0], action_list, value[1])
        print(key, " result:\n", result)
        print("States needed to reach goal: ", states)
        print("\n")


    ## Sub problem Solutions - DLS
    print("DLS")
    for key, value in sub_problems.items() :
        result, states = depth_first_search(value[0], action_list, value[1], limit=10)
        print(key, " result:\n", result)
        print("States needed to reach goal: ", states)
        print("\n")

    ## Sub problem Solutions - IDS
    print("IDS")
    for key, value in sub_problems.items() :
        result, states = iterative_deepening_search(value[0], action_list, value[1])
        print(key, " result:\n", result)
        print("States needed to reach goal: ", states)
        print("\n")

    '''result, states = breadth_first_search(sub_problems['drop sample'][0], action_list, sub_problems['drop sample'][1])
    print("drop sample result:\n", result)
    print("States needed to reach goal: ", states)'''