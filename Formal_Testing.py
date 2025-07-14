def is_safe(state, name):
    if name == "alice":
        if state["blue_key"] == "alice" or state["green_key"] == "alice" and state["blue_key"] != state["bob_room"] or state["blue_key"] == state["green_key"] != state["bob_room"] and state["blue_key"] == state["green_key"] != "bob" or state["bob_room"] == state["blue_key"] == "west_room" and (state["green_key"] == "east_room" or state["green_key"] == "alice"):
            return False
        else:
            return True
    else:
        if state["red_key"] == "bob" or state["green_key"] == "bob" and state["red_key"] != state["alice_room"] or state["red_key"] == state["green_key"] != state["alice_room"] or state["alice_room"] == state["red_key"] == "east_room" and (state["green_key"] == "west_room" or state["green_key"] == "bob"):
            return False
        else:
            return True

def change_character():
    def func(state):
        if state["player"] == "alice":
            return dict(state, player="bob")
        else:
            return dict(state, player="alice")
    return func


def go_through(door_color):
    def func(state):
        if state[f"{door_color}_key"] == state["player"]:
            if door_color in ["red", "blue"]:
                if state["player"] == "alice" and door_color == "red" and is_safe(state, "alice"):
                    return dict(state, alice_room=f"{door_color}_room")
                elif state["player"] == "bob" and door_color == "blue" and is_safe(state, "bob"):
                    return dict(state, bob_room=f"{door_color}_room")
                else:
                    return state
            else:
                if state["player"] == "alice":
                    if state["alice_room"] == "west_room":
                        return dict(state, alice_room="east_room")
                    else:
                        return dict(state, alice_room="west_room")
                else:
                    if state["bob_room"] == "west_room":
                        return dict(state, bob_room="east_room")
                    else:
                        return dict(state, bob_room="west_room")
        else:
            return state
    return func


def pick(key_color):
    def func(state):
        if state[f"{key_color}_key"] == get_current_room(state):
            match key_color:
                case "red":
                    return dict(state, red_key=state["player"])
                case "blue":
                    return dict(state, blue_key=state["player"])
                case "green":
                    return dict(state, green_key=state["player"])
        else:
            return state
    return func


def drop(key_color):
    def func(state):
        if state[f"{key_color}_key"] == state["player"]:
            match key_color:
                case "red":
                    return dict(state, red_key=get_current_room(state))
                case "blue":
                    return dict(state, blue_key=get_current_room(state))
                case "green":
                    return dict(state, green_key=get_current_room(state))
        else:
            return state
    return func


# Структура игры. Комнаты и допустимые в них действия
game = {
    'west_room': [
        go_through("red"),
        go_through("green"),
        change_character(),
        pick("green"),
        pick("red"),
        pick("blue"),
        drop("green"),
        drop("red"),
        drop("blue")
    ],
    'east_room': [
        go_through("blue"),
        go_through("green"),
        change_character(),
        pick("green"),
        pick("red"),
        pick("blue"),
        drop("green"),
        drop("red"),
        drop("blue")
    ],
    'red_room': [
        change_character()
    ],
    'blue_room': [
        change_character()
    ],
}


class StatesGraph:
    def __init__(self):
        self.graph = []

    def add_state(self, state):
        self.graph.append((state, []))

    def add_connection(self, state, connection):
        self.get_connections(state).append(connection)

    def get_connections(self, state, default=None):
        for s, c in self.graph:
            if state == s:
                return c
        return default

    def size(self):
        return len(self.graph)

    def states(self):
        return [state for state, connections in self.graph]

    def connections(self):
        return [connections for state, connections in self.graph]

    def get_accessible_states(self, starting_state):
        reached_states = []
        state_queue = [starting_state]
        while len(state_queue) > 0:
            curr_state = state_queue.pop(0)
            reached_states.append(curr_state)
            for new_state in self.get_connections(curr_state):
                if new_state not in reached_states and new_state not in state_queue:
                    state_queue.append(new_state)
        return reached_states


# Стартовое состояние
START_STATE = dict(
    player='alice',
    alice_room='west_room',
    bob_room='east_room',
    red_key='east_room',
    blue_key='west_room',
    green_key='east_room'
)


def is_goal_state(state):
    '''
    Проверить, является ли состояние целевым.
    '''
    return state["alice_room"] == "red_room" and state["bob_room"] == "blue_room"


def get_current_room(state):
    '''
    Выдать комнату, в которой находится игрок.
    '''
    return state[f"{state['player']}_room"]


def create_state_graph(game_struct, starting_state):
    state_graph = StatesGraph()
    state_queue = [starting_state]
    while len(state_queue) > 0:
        curr_state = state_queue.pop(0)
        state_graph.add_state(curr_state)
        curr_room = get_current_room(curr_state)
        for func in game_struct[curr_room]:
            new_state = func(curr_state)
            if new_state not in state_graph.states() and new_state not in state_queue:
                state_queue.append(new_state)
            if new_state != curr_state:
                state_graph.add_connection(curr_state, new_state)
    return state_graph


def find_dead_ends(graph: StatesGraph):
    states_to_check = graph.states()
    dead_ends = []
    while len(states_to_check) > 0:
        curr_state = states_to_check.pop(0)
        acc_states = graph.get_accessible_states(curr_state)
        if not any((is_goal_state(state) for state in acc_states)):
            dead_ends.extend(acc_states)
            states_to_check = [state for state in states_to_check if state not in acc_states]
    return dead_ends


def print_dot(graph: StatesGraph, start_key):
    dead_ends = find_dead_ends(graph)
    print('digraph {')
    graph_keys = graph.states()
    for x in graph_keys:
        n = graph_keys.index(x)
        if x == start_key:
            print(f'n{n} [style="filled",fillcolor="dodgerblue",shape="circle"]')
        elif is_goal_state(x):
            print(f'n{n} [style="filled",fillcolor="green",shape="circle"]')
        elif x in dead_ends:
            print(f'n{n} [style="filled",fillcolor="red",shape="circle"]')
        else:
            print(f'n{n} [shape="circle"]')
    for x in graph_keys:
        n1 = graph_keys.index(x)
        for y in graph.get_connections(x):
            n2 = graph_keys.index(y)
            print(f'n{n1} -> n{n2}')
    print('}')


def find_shortest_solution(graph, starting_state):
    reached_states = []
    state_queue = [(starting_state, 0)]
    while len(state_queue) > 0:
        curr_state, dist = state_queue.pop(0)
        if is_goal_state(curr_state):
            return dist
        reached_states.append(curr_state)
        for new_state in graph.get_connections(curr_state):
            if new_state not in reached_states and new_state not in state_queue:
                state_queue.append((new_state, dist + 1))
    return 0


ans = create_state_graph(game, START_STATE)
print(print_dot(ans, START_STATE))
print(find_shortest_solution(ans, START_STATE))
print(ans.states()[90], ans.states()[160])
