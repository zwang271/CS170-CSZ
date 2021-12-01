import pickle as pkl
import os
from solver import compute_total
from parse import read_input_file, write_output_file

def calculate_average(array):
    count = 0
    average = 0   
    for output in array:
        average += output[-1]
        count += 1
    return average/count

def write_to_output(size, answers):
    i = 0
    in_directory = "C:/CS170_Final/inputs/" + size + "/"
    for input_path in os.listdir(in_directory):
        output = answers[i][0:len(answers[i]) - 1]
        output_path = "C:/CS170_Final/outputs/" + size + "/" + input_path[:-3] + '.out'
        write_output_file(output_path, output)
        i += 1

# Answer computed for all class inputs with the "calculate_weight_1" function as heuristic used
with open('array_outputs/calculate_weight_1_small.pkl', 'rb') as f:
    calculate_weight_1_small = pkl.load(f)   
with open('array_outputs/calculate_weight_1_medium.pkl', 'rb') as f:
    calculate_weight_1_medium = pkl.load(f)
with open('array_outputs/calculate_weight_1_large.pkl', 'rb') as f:
    calculate_weight_1_large = pkl.load(f)
    
calculate_weight_1 = [calculate_weight_1_small, calculate_weight_1_medium, calculate_weight_1_large]
print([calculate_average(calculate_weight_1[i]) for i in range(3)])

# Answer computed for all class inputs with the "calculate_weight_2" function as heuristic used
with open('array_outputs/calculate_weight_2_small.pkl', 'rb') as f:
    calculate_weight_2_small = pkl.load(f)   
with open('array_outputs/calculate_weight_2_medium.pkl', 'rb') as f:
    calculate_weight_2_medium = pkl.load(f)
with open('array_outputs/calculate_weight_2_large.pkl', 'rb') as f:
    calculate_weight_2_large = pkl.load(f)
    
calculate_weight_2 = [calculate_weight_2_small, calculate_weight_2_medium, calculate_weight_2_large]
print([calculate_average(calculate_weight_2[i]) for i in range(3)])

# Best results over all algorithms
best_small = []
best_medium = []
best_large = []
for i in range(299):
    if calculate_weight_1[0][i][-1] > calculate_weight_2[0][i][-1]:
        best_small.append(calculate_weight_1[0][i])
    else: 
        best_small.append(calculate_weight_2[0][i])

for i in range(300):
    if calculate_weight_1[1][i][-1] > calculate_weight_2[1][i][-1]:
        best_medium.append(calculate_weight_1[1][i])
    else: 
        best_medium.append(calculate_weight_2[1][i])

for i in range(300):
    if calculate_weight_1[2][i][-1] > calculate_weight_2[2][i][-1]:
        best_large.append(calculate_weight_1[2][i])
    else: 
        best_large.append(calculate_weight_2[2][i])

print(calculate_average(best_small))
print(calculate_average(best_medium))
print(calculate_average(best_large))

write_to_output("small", best_small)
write_to_output("medium", best_medium)
write_to_output("large", best_large)



    


