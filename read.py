#!/usr/bin/env python3
"""
Read input file for Go game
"""
def read_input(file_path="input.txt"):
    """Read game state from input file"""
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    color = int(lines[0])
    prev_board = [list(map(int, list(lines[i]))) for i in range(1, 6)]
    curr_board = [list(map(int, list(lines[i]))) for i in range(6, 11)]
    
    return color, prev_board, curr_board

def main():
    """Test reading input"""
    try:
        color, prev_board, curr_board = read_input()
        print(f"Player color: {color}")
        print("Previous board:")
        for row in prev_board:
            print(" ".join(str(cell) for cell in row))
        print("Current board:")
        for row in curr_board:
            print(" ".join(str(cell) for cell in row))
    except Exception as e:
        print(f"Error reading input: {e}")

if __name__ == "__main__":
    main()
