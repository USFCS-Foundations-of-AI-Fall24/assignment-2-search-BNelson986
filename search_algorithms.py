from collections import deque



## We will append tuples (state, "action") in the search queue
def breadth_first_search(startState, action_list, goal_test, use_closed_list=True) :
    search_queue = deque()
    closed_list = {}
    num_states = 0

    search_queue.append((startState,""))
    if use_closed_list :
        closed_list[startState] = True
    while len(search_queue) > 0 :
        ## this is a (state, "action") tuple
        next_state = search_queue.popleft()
        if goal_test(next_state[0]):
            print("Goal found")
            print(next_state)
            ptr = next_state[0]
            while ptr is not None :
                ptr = ptr.prev
                print(ptr)
                num_states += 1
            print("States needed to reach goal: ", num_states)
            return next_state
        else :
            successors = next_state[0].successors(action_list)
            if use_closed_list :
                successors = [item for item in successors
                                    if item[0] not in closed_list]
                for s in successors :
                    closed_list[s[0]] = True
            search_queue.extend(successors)

### Note the similarity to BFS - the only difference is the search queue

## use the limit parameter to implement depth-limited search
def depth_first_search(startState, action_list, goal_test, use_closed_list=True, limit=None) :
    search_queue = deque()
    closed_list = {}
    num_states = 0

    # Adjust search queue to use state tuple and track depth of search
    search_queue.append((startState,"", 0))
    if use_closed_list :
        closed_list[startState] = True
    while len(search_queue) > 0 :
        ## this is a (state, "action") tuple
        next_state = search_queue.pop()
        if goal_test(next_state[0]):
            print("Goal found")
            print(next_state)
            ptr = next_state[0]
            while ptr is not None :
                ptr = ptr.prev
                num_states += 1
                print(ptr)
            print("States needed to reach goal: ", num_states)
            return next_state
        if limit is None or next_state[2] < limit :
            successors = next_state[0].successors(action_list)
            if use_closed_list :
                successors = [item for item in successors
                                    if item[0] not in closed_list]
                for s in successors :
                    closed_list[s[0]] = True

            # Add successors to search queue and track depth
            search_queue.extend((s[0], s[1], next_state[2]+1) for s in successors)

    ### Finishing up Iterative Deepening Search
    ### Q4-5
    if limit is not None :
        print("Exceeded depth limit: ", limit)
    else:
        print("No solution found")

## add iterative deepening search here


def iterative_deepening_search(startState, action_list, goal_test) :
    """
    Perform an iterative deepening search. By adjusting depth limits until a solution is found.

    Parameters
    ----------
    startState : state
        The starting state of the search.
    action_list : list of functions
        Each function takes a state and returns a new state.
    goal_test : function
        Takes a state and returns a boolean indicating whether the state is a goal state.

    Returns
    -------
    result : state
        The state that satisfies the goal test. If no solution is found, None is returned.
    """
    limit = 0
    while True :
        result = depth_first_search(startState, action_list, goal_test, limit)
        if result :
            return result
        limit += 1