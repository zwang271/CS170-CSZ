from parse import read_input_file, write_output_file
import os

def solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    pass


# Here's an example of how to run your solver.
# if __name__ == '__main__':
in_directory = "C:/CS170_Final/inputs/"
for input_path in os.listdir(in_directory):
    output_path = 'outputs/' + input_path[:-3] + '.out'
    tasks = read_input_file(in_directory + input_path)
    output = solve(tasks)
    write_output_file(output_path, output)