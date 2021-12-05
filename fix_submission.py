import os
from solver import compute_total
from parse import read_input_file, write_output_file

OUTPUT_DIRECTORY = "C:/CS170_Final/all_outputs/"

def read_array(output_file):
    with open(output_file) as file:
        lines = file.readlines()
    output = []
    for i in range(len(lines)):
        output.append(int(lines[i][:-1]))
    return output

def fix_solution(tasks, solution):
    used_original = [x for x in solution]
    unused_original = [] # List of task IDs unused in the original solution
    for task in tasks:
        if task.get_task_id() not in used_original:
            unused_original.append(task.get_task_id())
    value_original = compute_total(tasks, solution) # Total value of the original solution
    
    unused = [x for x in unused_original] # List of unused task IDs that will be updated
    solution_new = [x for x in solution]
    
