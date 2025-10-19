import subprocess
import sys

if len(sys.argv) != 3:
    print("Usage: python counter.py <filename> <processor>")
    sys.exit(1)

filename = sys.argv[1]
processor = sys.argv[2]

try:
    with open(filename, 'r') as file:
        content = file.read()
        print("File content successfully read.")

    result = subprocess.run([processor], input=content, text=True, capture_output=True)

    print()
    print("Processed Output:")
    print(result.stdout)

except FileNotFoundError:
    print(f"Error: The file '{filename}' was not found.")
    sys.exit(1)