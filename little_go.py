#!/usr/bin/env python3
"""
Little Go game implementation
"""
import copy
import random

GRID = 5
EMPTY = 0
BLACK = 1
WHITE = 2
KOMI = 2.5

class LittleGo:
    def __init__(self):
        self.board = [[EMPTY for _ in range(GRID)] for _ in range(GRID)]
        self.prev_board = None
        self.current_player = BLACK
        self.move_count = 0
        self.max_moves = GRID * GRID - 1
    
    def get_neighbors(self, i, j):
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
    
    def get_group_and_liberties(self, i, j):
        """Get group and liberties for a position"""
        color = self.board[i][j]
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
            
            for ni, nj in self.get_neighbors(ci, cj):
                if self.board[ni][nj] == EMPTY:
                    liberties.add((ni, nj))
                elif self.board[ni][nj] == color and (ni, nj) not in group:
                    stack.append((ni, nj))
        
        return group, liberties
    
    def remove_group(self, group):
        """Remove a group from the board"""
        for i, j in group:
            self.board[i][j] = EMPTY
    
    def is_legal_move(self, i, j):
        """Check if a move is legal"""
        if self.board[i][j] != EMPTY:
            return False
        
        # Make a copy and test the move
        test_board = copy.deepcopy(self.board)
        test_board[i][j] = self.current_player
        
        # Check for captures
        enemy = WHITE if self.current_player == BLACK else BLACK
        captured = False
        
        for ni, nj in self.get_neighbors(i, j):
            if test_board[ni][nj] == enemy:
                group, liberties = self.get_group_and_liberties(ni, nj)
                if len(liberties) == 0:
                    for gi, gj in group:
                        test_board[gi][gj] = EMPTY
                    captured = True
        
        # Check for suicide
        group, liberties = self.get_group_and_liberties(i, j)
        if len(liberties) == 0 and not captured:
            return False
        
        # Check for ko rule
        if self.prev_board is not None and test_board == self.prev_board:
            return False
        
        return True
    
    def make_move(self, i, j):
        """Make a move on the board"""
        if not self.is_legal_move(i, j):
            return False
        
        self.prev_board = copy.deepcopy(self.board)
        self.board[i][j] = self.current_player
        
        # Capture enemy groups
        enemy = WHITE if self.current_player == BLACK else BLACK
        for ni, nj in self.get_neighbors(i, j):
            if self.board[ni][nj] == enemy:
                group, liberties = self.get_group_and_liberties(ni, nj)
                if len(liberties) == 0:
                    self.remove_group(group)
        
        self.current_player = WHITE if self.current_player == BLACK else BLACK
        self.move_count += 1
        return True
    
    def pass_move(self):
        """Pass the current turn"""
        self.prev_board = copy.deepcopy(self.board)
        self.current_player = WHITE if self.current_player == BLACK else BLACK
        self.move_count += 1
    
    def is_game_over(self):
        """Check if the game is over"""
        return self.move_count >= self.max_moves
    
    def get_score(self):
        """Calculate final score"""
        black_stones = sum(row.count(BLACK) for row in self.board)
        white_stones = sum(row.count(WHITE) for row in self.board)
        return black_stones, white_stones + KOMI
    
    def print_board(self):
        """Print the current board"""
        print("Current Board:")
        for row in self.board:
            print(" ".join(str(cell) for cell in row))
        print()

def main():
    """Test the Little Go implementation"""
    game = LittleGo()
    game.print_board()
    
    # Test a few moves
    game.make_move(2, 2)
    game.print_board()
    
    game.make_move(1, 1)
    game.print_board()

if __name__ == "__main__":
    main()
