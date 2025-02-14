import fire
import random
from typing import List

def process_line(line: str) -> str:
    """Process a single line to add a random probability."""
    edge1, edge2 = line.strip().split(' ')
    prob = random.random()
    return f"{edge1} {edge2} {prob:.4f}"

def convert_dataset(filename: str) -> None:
    """Convert a dataset file by adding random probabilities to each line.

    Args:
        filename (str): Path to the input file.

    Creates a new file with the same name plus ".convert" appended.
    """
    try:
        with open(filename, 'r') as file:
            lines = (process_line(line) for line in file)

            new_filename = f"{filename}.convert"
            with open(new_filename, 'w') as outfile:
                outfile.write('\n'.join(lines))
        print(f"Converted file saved as: {new_filename}")
    except FileNotFoundError:
        print(f"Error: The file {filename} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    fire.Fire(convert_dataset)