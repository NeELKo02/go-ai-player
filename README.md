# Go AI Player

A sophisticated Go AI player that uses Monte Carlo Tree Search (MCTS) with heuristic evaluation for 5x5 Go games.

## Files

• **myplayer.py** - Main AI player implementation
• **input.txt** - Game state input file (format: player_color, previous_board, current_board)
• **output.txt** - AI's move output file
• **step_num.txt** - Move counter tracking file
• **test_inputs/** - Test scenarios for different game situations

## Input Format

The `input.txt` file contains:
- Line 1: Player color (1 for Black, 2 for White)
- Lines 2-6: Previous board state (5x5 grid, 0=empty, 1=black, 2=white)
- Lines 7-11: Current board state (5x5 grid, 0=empty, 1=black, 2=white)

## Output Format

The `output.txt` file contains:
- Move coordinates as "row,col" (e.g., "2,3")
- "PASS" if no legal moves available

## How to Run

```bash
python myplayer.py
```

## AI Strategy

• **Forced Capture Detection**: Prioritizes moves that capture enemy stones
• **Monte Carlo Tree Search**: Main decision-making algorithm with 7.5-second time limit
• **Heuristic Evaluation**: Scores moves based on threats and board position
• **UCT Selection**: Balances exploration vs exploitation in tree search

## Game Rules

• 5x5 Go board
• Black plays first (color 1)
• White gets 2.5 komi points
• Maximum 24 moves per game
• Standard Go rules: capture, ko rule, suicide prevention

## Test Scenarios

Use the test input files to verify AI behavior in different situations:
- Opening moves
- Capture opportunities
- Endgame positions
- Edge cases and corner scenarios
