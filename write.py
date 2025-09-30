#!/usr/bin/env python3
"""
Write output file for Go game
"""
def write_output(move, file_path="output.txt"):
    """Write move to output file"""
    with open(file_path, 'w') as f:
        if move == "PASS" or move == (-1, -1):
            f.write("PASS")
        else:
            i, j = move
            f.write(f"{i},{j}")

def main():
    """Test writing output"""
    # Test different move formats
    write_output((2, 3), "test_output.txt")
    write_output("PASS", "test_pass.txt")
    
    print("Test outputs written to test_output.txt and test_pass.txt")

if __name__ == "__main__":
    main()
