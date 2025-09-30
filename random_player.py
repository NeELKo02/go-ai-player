#!/usr/bin/env python3
"""
Random Go player for testing
"""
import random
import copy
from read import read_input
from write import write_output

GRID = 5
EMPTY = 0

def get_neighbors(i, j):
    """Get valid neighbors of a position"""
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
    """Get group and liberties for a position"""
    color = board[i][j]
    if color == EMPTY:
        return set(), set()
    
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
    """Remove a group from the board"""
    for i, j in group:
        board[i][j] = EMPTY

def simulate_move(board, move, color, prev_board):
    """Simulate a move and return the resulting board"""
    new_board = copy.deepcopy(board)
    enemy = 1 if color == 2 else 2
    
    if move == "PASS":
        return new_board
    
    i, j = move
    if new_board[i][j] != EMPTY:
        return None
    
    new_board[i][j] = color
    
    # Capture enemy groups
    captured = False
    for ni, nj in get_neighbors(i, j):
        if new_board[ni][nj] == enemy:
            group, liberties = get_group_and_liberties(new_board, ni, nj)
            if len(liberties) == 0:
                new_board = remove_group(new_board, group)
                captured = True
    
    # Check for suicide
    group, liberties = get_group_and_liberties(new_board, i, j)
    if len(liberties) == 0 and not captured:
        return None
    
    # Check for ko rule
    if prev_board is not None and new_board == prev_board:
        return None
    
    return new_board

def get_legal_moves(board, color, prev_board):
    """Get all legal moves for a player"""
    moves = ["PASS"]
    
    for i in range(GRID):
        for j in range(GRID):
            if board[i][j] == EMPTY:
                if simulate_move(board, (i, j), color, prev_board) is not None:
                    moves.append((i, j))
    
    return moves

def main():
    """Random player main function"""
    try:
        color, prev_board, curr_board = read_input()
        legal_moves = get_legal_moves(curr_board, color, prev_board)
        
        if legal_moves:
            move = random.choice(legal_moves)
        else:
            move = "PASS"
        
        write_output(move)
        print(f"Random player move: {move}")
        
    except Exception as e:
        print(f"Error: {e}")
        write_output("PASS")

if __name__ == "__main__":
    main()
