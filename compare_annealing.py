import os
from solver import *
from parse import read_input_file, write_output_file

OUTPUT_DIRECTORY = "C:/CS170_Final/"

def read_array(output_file):
    print(output_file)
    with open(output_file) as file:
        lines = file.readlines()
    output = []
    for i in range(len(lines)):
        output.append(int(lines[i][:-1]))
        
    for i in range(len(output)):
        for j in range(i + 1, len(output)):
            if output[i] == output[j]:
                print("duplicate output", output[i], output_file)
                print(output)
                break
    return output

input = "medium/medium-26.in"
run_anneal(input, 2000, True)
print(read_array(OUTPUT_DIRECTORY + "outputs/" + input[:-3] + '.out'))

# for input_path in os.listdir("C:/CS170_Final/inputs/large/"):
#     tasks = read_input_file("C:/CS170_Final/inputs/large/" + input_path)
#     output1 = read_array("C:/CS170_Final/all_outputs/zili_large_annealing_once/" + input_path[:-3] + ".out")
#     output2 = read_array("C:/CS170_Final/all_outputs/large_combined/" + input_path[:-3] + ".out")
#     if compute_total(tasks, output1) > compute_total(tasks, output2):
#         output = output1
#     else:
#         output = output2
#     write_output_file("C:/CS170_Final/outputs/large/" + input_path[:-3] + '.out', output)
    
        