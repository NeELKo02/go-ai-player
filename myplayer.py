#!/usr/bin/env python3
import copy
import random
import time
import math

GRID = 5
EMPTY = 0
FILE_STEP = 'step_num.txt'
MAX_MOVES = (GRID * GRID) - 1
KOMI = 2.5

def read_input(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    color = int(lines[0])
    prev_board = [list(map(int, list(lines[i]))) for i in range(1, 6)]
    curr_board = [list(map(int, list(lines[i]))) for i in range(6, 11)]
    return color, prev_board, curr_board

def write_output(move, file_path):
    with open(file_path, 'w') as f:
        if move == "PASS" or move == (-1, -1):
            f.write("PASS")
        else:
            i, j = move
            f.write(f"{i},{j}")

def steps_count(prev_board, curr_board):
    initial_prev = all(cell == EMPTY for row in prev_board for cell in row)
    initial_curr = all(cell == EMPTY for row in curr_board for cell in row)
    step_mapping = {(True, True): 0, (True, False): 1}
    current_step = step_mapping.get((initial_prev, initial_curr))
    if current_step is None:
        try:
            with open(FILE_STEP, 'r') as f:
                current_step = int(f.readline().strip())
            current_step += 2
        except FileNotFoundError:
            current_step = 2
    with open(FILE_STEP, 'w') as f:
        f.write(str(current_step))
    return current_step

def get_neighbors(i, j):
    neighbors = []
    if i > 0:
        neighbors.append((i - 1, j))
    if i < GRID - 1:
        neighbors.append((i + 1, j))
    if j > 0:
        neighbors.append((i, j - 1))
    if j < GRID - 1:
        neighbors.append((i, j + 1))
    return neighbors

def get_group_and_liberties(board, i, j):
    color = board[i][j]
    group = set()
    liberties = set()
    stack = [(i, j)]
    while stack:
        ci, cj = stack.pop()
        if (ci, cj) in group:
            continue
        group.add((ci, cj))
        for ni, nj in get_neighbors(ci, cj):
            if board[ni][nj] == EMPTY:
                liberties.add((ni, nj))
            elif board[ni][nj] == color and (ni, nj) not in group:
                stack.append((ni, nj))
    return group, liberties

def remove_group(board, group):
    for i, j in group:
        board[i][j] = EMPTY
    return board

def simulate_move(board, move, color, prev_board):
    new_board = copy.deepcopy(board)
    enemy = 1 if color == 2 else 2
    if move == "PASS":
        return new_board
    i, j = move
    if new_board[i][j] != EMPTY:
        return None
    new_board[i][j] = color
    captured = False
    for ni, nj in get_neighbors(i, j):
        if new_board[ni][nj] == enemy:
            group, liberties = get_group_and_liberties(new_board, ni, nj)
            if len(liberties) == 0:
                new_board = remove_group(new_board, group)
                captured = True
    group, liberties = get_group_and_liberties(new_board, i, j)
    if len(liberties) == 0 and not captured:
        return None
    if prev_board is not None and new_board == prev_board:
        return None
    return new_board

def forced_capture_move(state):
    enemy = 1 if state.player == 2 else 2
    best_move = None
    best_capture = 0
    current_enemy_count = sum(row.count(enemy) for row in state.board)
    for move in legal_moves(state):
        if move == "PASS":
            continue
        new_board = simulate_move(state.board, move, state.player, state.prev_board)
        if new_board is None:
            continue
        new_enemy_count = sum(row.count(enemy) for row in new_board)
        capture_gain = current_enemy_count - new_enemy_count
        if capture_gain > best_capture:
            best_capture = capture_gain
            best_move = move
    return best_move

def heuristic_score(state, move, color):
    if move == "PASS":
        return -1000
    score = 0
    enemy = 1 if color == 2 else 2
    for ni, nj in get_neighbors(move[0], move[1]):
        if state.board[ni][nj] == enemy:
            group, liberties = get_group_and_liberties(state.board, ni, nj)
            if len(liberties) == 1:
                score += 100
    center = GRID // 2
    dist = abs(move[0] - center) + abs(move[1] - center)
    score += (GRID - dist)
    return score

def select_heuristic_move(state):
    moves = legal_moves(state)
    if not moves:
        return "PASS"
    best_capture = -1
    best_move = None
    enemy = 1 if state.player == 2 else 2
    for move in moves:
        if move == "PASS":
            continue
        new_board = simulate_move(state.board, move, state.player, state.prev_board)
        if new_board is None:
            continue
        new_enemy_count = sum(row.count(enemy) for row in new_board)
        current_enemy_count = sum(row.count(enemy) for row in state.board)
        capture_gain = current_enemy_count - new_enemy_count
        if capture_gain > best_capture:
            best_capture = capture_gain
            best_move = move
    if best_move is not None and best_capture > 0 and random.random() < 0.8:
        return best_move
    scored_moves = []
    for move in moves:
        s = heuristic_score(state, move, state.player)
        scored_moves.append((move, s))
    weights = [max(s, 0.1) for _, s in scored_moves]
    total = sum(weights)
    if total <= 0:
        return random.choice(moves)
    moves_only = [m for m, _ in scored_moves]
    return random.choices(moves_only, weights=weights, k=1)[0]

class State:
    def __init__(self, board, prev_board, player, last_pass, move_count):
        self.board = board
        self.prev_board = prev_board
        self.player = player
        self.last_pass = last_pass
        self.move_count = move_count

    def clone(self):
        return State(copy.deepcopy(self.board),
                     copy.deepcopy(self.prev_board),
                     self.player,
                     self.last_pass,
                     self.move_count)

def legal_moves(state):
    moves = ["PASS"]
    for i in range(GRID):
        for j in range(GRID):
            if state.board[i][j] == EMPTY:
                if simulate_move(state.board, (i, j), state.player, state.prev_board) is not None:
                    moves.append((i, j))
    return moves

def is_terminal(state):
    if state.last_pass:
        if legal_moves(state) == ["PASS"]:
            return True
    if state.move_count >= MAX_MOVES:
        return True
    return False

def game_result(state, my_color):
    black_stones = sum(row.count(1) for row in state.board)
    white_stones = sum(row.count(2) for row in state.board)
    if my_color == 1:
        return 1 if black_stones > white_stones else 0
    else:
        return 1 if (white_stones + KOMI) > black_stones else 0

def apply_move(state, move):
    new_state = state.clone()
    if move == "PASS":
        new_state.prev_board = copy.deepcopy(new_state.board)
        new_state.last_pass = True
        new_state.move_count += 1
    else:
        new_board = simulate_move(new_state.board, move, new_state.player, new_state.prev_board)
        if new_board is None:
            return None
        new_state.prev_board = new_state.board
        new_state.board = new_board
        new_state.last_pass = False
        new_state.move_count += 1
    new_state.player = 1 if new_state.player == 2 else 2
    return new_state

class Node:
    def __init__(self, state, parent, move, player_just_moved):
        self.state = state
        self.parent = parent
        self.move = move
        self.player_just_moved = player_just_moved
        self.children = []
        self.untried_moves = legal_moves(state)
        self.visits = 0
        self.wins = 0.0
        self.hscore = 0

    def uct_select_child(self, exploration=1.41, bias=0.005):
        return max(self.children, key=lambda c: (c.wins / c.visits) + exploration * math.sqrt(math.log(self.visits) / c.visits) + bias * c.hscore)

    def add_child(self, move, state):
        child = Node(state, self, move, self.state.player)
        child.hscore = heuristic_score(self.state, move, self.state.player)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def update(self, result, my_color):
        self.visits += 1
        if self.player_just_moved == my_color:
            self.wins += result
        else:
            self.wins += (1 - result)

def mcts(root_state, my_color, time_limit):
    root_node = Node(root_state, None, None, 1 if my_color == 2 else 2)
    end_time = time.time() + time_limit
    while time.time() < end_time:
        node = root_node
        state = root_state.clone()
        while not node.untried_moves and node.children:
            node = node.uct_select_child()
            state = apply_move(state, node.move)
            if state is None:
                break
        if state is None:
            continue
        if node.untried_moves:
            move = max(node.untried_moves, key=lambda m: heuristic_score(state, m, state.player))
            next_state = apply_move(state, move)
            if next_state is None:
                node.untried_moves.remove(move)
                continue
            node = node.add_child(move, next_state)
            state = next_state
        while not is_terminal(state):
            move = select_heuristic_move(state)
            next_state = apply_move(state, move)
            if next_state is None:
                state = None
                break
            state = next_state
        if state is None:
            result = 0
        else:
            result = game_result(state, my_color)
        while node is not None:
            node.update(result, my_color)
            node = node.parent
    if root_node.children:
        best_child = max(root_node.children, key=lambda c: c.visits)
        return best_child.move
    return "PASS"

def main():
    color, prev_board, curr_board = read_input("input.txt")
    move_count = steps_count(prev_board, curr_board)
    initial_state = State(curr_board, prev_board, color, False, move_count)
    forced_move = forced_capture_move(initial_state)
    if forced_move is not None:
        write_output(forced_move, "output.txt")
        return
    best_move = mcts(initial_state, color, time_limit=7.5)
    write_output(best_move, "output.txt")

if __name__ == "__main__":
    main()
