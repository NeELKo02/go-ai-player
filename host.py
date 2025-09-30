#!/usr/bin/env python3
"""
Host program for Go game simulation
"""
import subprocess
import time
import os

def run_player(player_script, input_file="input.txt", output_file="output.txt"):
    """Run a player script and return the move"""
    try:
        result = subprocess.run(
            ["python", player_script],
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0:
            with open(output_file, 'r') as f:
                move = f.read().strip()
            return move
        else:
            print(f"Error running {player_script}: {result.stderr}")
            return "PASS"
    except subprocess.TimeoutExpired:
        print(f"Player {player_script} timed out")
        return "PASS"
    except Exception as e:
        print(f"Error: {e}")
        return "PASS"

def main():
    """Main host function"""
    print("Go Game Host")
    print("=" * 20)
    
    # Test the AI player
    move = run_player("myplayer.py")
    print(f"AI Move: {move}")

if __name__ == "__main__":
    main()
