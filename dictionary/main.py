import sys
import os
from text_processing import process_input

if __name__ == "__main__":
    # Check if the input file is provided as a command-line argument
    if len(sys.argv) != 2:
        print("Usage: python main.py input_file.txt")
        sys.exit(1)

    input_file = sys.argv[1]

    # Read the content of the input file
    with open(input_file, 'r', encoding='utf-8') as file:
        input_text = file.read()

    translation_df = process_input(input_text)

    # Print the DataFrame
    print(translation_df)

    # Save the output to a new file
    output_directory = '../data'
    output_file = os.path.join(output_directory, os.path.splitext(os.path.basename(input_file))[0] + '.dict.csv')
    translation_df.to_csv(output_file, index=False)
