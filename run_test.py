#!/usr/bin/env python3
"""
Test runner for the Go AI player
"""
import os
import shutil
import subprocess
import sys

def run_test(test_file, description):
    """Run a single test case"""
    print(f"\n=== {description} ===")
    
    # Copy test input to main input file
    shutil.copy(test_file, "input.txt")
    
    # Reset step counter
    with open("step_num.txt", "w") as f:
        f.write("0")
    
    try:
        # Run the AI player
        result = subprocess.run([sys.executable, "myplayer.py"], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            # Read the output
            with open("output.txt", "r") as f:
                move = f.read().strip()
            print(f"AI Move: {move}")
        else:
            print(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("AI timed out")
    except Exception as e:
        print(f"Error running test: {e}")

def main():
    """Run all test cases"""
    print("Go AI Player Test Suite")
    print("=" * 30)
    
    test_cases = [
        ("test_inputs/opening_move.txt", "Opening Move Test"),
        ("test_inputs/capture_opportunity.txt", "Capture Opportunity Test"),
        ("test_inputs/mid_game.txt", "Mid-Game Test"),
        ("test_inputs/endgame.txt", "Endgame Test")
    ]
    
    for test_file, description in test_cases:
        if os.path.exists(test_file):
            run_test(test_file, description)
        else:
            print(f"Test file {test_file} not found")
    
    print("\n" + "=" * 30)
    print("Test suite completed")

if __name__ == "__main__":
    main()
