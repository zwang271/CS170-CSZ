from parse import read_input_file, write_output_file
import os
import itertools
import math
import pickle as pkl
import random
import time

DIRECTORY = "C:/CS170_Final/"

def greedy_solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing
    """
    num_tasks = len(tasks)
    time = 0
    max_weight = 0
    max_index = 0
    used = [False for _ in range(num_tasks)]
    answer = []
    while time <= 1440 and not all(used):
        max_weight = -1
        max_index = -1
        for task in tasks:
            if not used[task.get_task_id() - 1]:
                current_weight = task.calculate_weight_2(time)
                if max_weight < current_weight:
                    max_weight = current_weight
                    max_index = task.get_task_id() - 1 #smol egg
        time += tasks[max_index].get_duration()
        if time > 1440:
            return answer
        answer.append(max_index + 1)
        used[max_index] = True
    return answer

def initial_solve(tasks):
    solution = []
    used = [False for _ in range(len(tasks))]
    time = 0
    
    i = 0
    while time <= 1440 and not all(used):
        time += tasks[i].get_duration()
        if time > 1440:
            return solution
        solution.append(tasks[i].get_task_id())
        i += 1
    return solution
       
def anneal(tasks, solution, p, toggle = False, i_c = 0):
    used_original = [x for x in solution]
    unused_original = [] # List of task IDs unused in the original solution
    for task in tasks:
        if task.get_task_id() not in used_original:
            unused_original.append(task.get_task_id())
    value_original = compute_total(tasks, solution) # Total value of the original solution
    
    unused = [x for x in unused_original] # List of unused task IDs that will be updated
    solution_new = [x for x in solution] # List of task IDs in the solution that will be updated
    locations_to_try = [i for i in range(len(solution))] # Locations to try external swaps for
    
    # Search for a swap that improves the original solution
    # Stop searching if there are no more unused tasks (we ran out of tasks)
    while_break_flag = False
    while len(unused) > 0 and len(locations_to_try) > 0:
        # set stuff up again
        chosen_index = random.choice(locations_to_try) # Choose a random index in location_to_try
        locations_to_try.remove(chosen_index) # Remove the chosen index from locations_to_try
        solution_new = [x for x in solution] # Reset the new_solution between iterations
        unused = [x for x in unused_original] # Reset the unused tasks between iterations
        
        for task_id in unused:
            solution_new = [x for x in solution] # Reset the new_solution between iterations
            unused = [x for x in unused_original] # Reset the unused tasks between iterations
            task_index = task_id - 1
            unused.append(solution_new[chosen_index])
            solution_new[chosen_index] = task_id # Make the swap
            unused.remove(task_id) # Remove ID of task chosen
            while(calculate_duration(tasks, solution_new) > 1440):
                if (chosen_index < len(solution_new) - 2):
                    unused.append(solution_new[chosen_index + 1])
                    solution_new.pop(chosen_index + 1)
                elif (chosen_index > 0):
                    unused.append(solution_new[chosen_index - 1])
                    solution_new.pop(chosen_index - 1)
                    
            current_duration = calculate_duration(tasks, solution_new)
            
            # Greedy add things back into solution_new
            is_used = [False for _ in range(len(tasks))]
            for index in solution_new:
                is_used[index - 1] = True
                #boost = random.randint(0,30000//(i_c+1))
            while current_duration <= 1440:
                max_weight = -1
                max_index = -1
                for task in tasks:
                    if not is_used[task.get_task_id() - 1]:
                        current_weight = task.calculate_weight_1(current_duration)
                        if max_weight < current_weight:
                            max_weight = current_weight
                            max_index = task.get_task_id() - 1 #smol egg
                current_duration += tasks[max_index].get_duration()
                if current_duration > 1440:
                    break
                solution_new.append(max_index + 1)
                is_used[max_index] = True
            
            total_computed =compute_total(tasks, solution_new)
            # Return this new solution if it is better
            if  total_computed > value_original or ((toggle and random.randint(0, 0.8*p) > i_c) and (total_computed/value_original  > (i_c+0.2*p)/(i_c+0.2*p+1))):
                while_break_flag = True
                break
        if while_break_flag:
            break
    
    # Internal swap
    if while_break_flag:
        solution_swap = [x for x in solution_new]
    else:
        solution_swap = [x for x in solution]
    solution_swap_original = [x for x in solution_swap]
        
    i_set = [i for i in range(len(solution_swap))]
    j_set = [j for j in range(len(solution_swap))]
    while len(i_set) > 0:
        i = random.choice(i_set)
        i_set.remove(i)
        while len(j_set) > 0:
            j = random.choice(j_set)
            j_set.remove(j)
                        
            solution_swap = [x for x in solution_swap_original]
            temp = solution_swap[i]
            solution_swap[i] = solution_swap[j]
            solution_swap[j] = temp
            total_computed = compute_total(tasks, solution_swap)
            if total_computed > value_original or ((toggle and random.randint(0, 0.8*p) > i_c) and (total_computed/value_original  > (i_c+0.2*p)/(i_c+0.2*p+1))):
                return solution_swap
    
    if while_break_flag:
        return solution_new
        
    return solution # Return the original solution if no advantageous swap is found

def calculate_duration(tasks, solution):
    duration = 0
    for index in solution:
        index = index -1
        duration += tasks[index].get_duration()
    return duration

def compute_total(all_tasks, tasks_list):
        total = 0
        time = 0
        for task_id in tasks_list:
            time += all_tasks[task_id-1].get_duration()
            assert time <= 1440, "Can't schedule task beyond 1440 minutes."
            total += all_tasks[task_id-1].get_late_benefit(time - all_tasks[task_id-1].get_deadline())
        return total

def check_solution(output, trial_name = ""):
    if len(output) != len(set(output)):
        return False

def read_array(output_file):
    print(output_file)
    with open(output_file) as file:
        lines = file.readlines()
    output = []
    for i in range(len(lines)):
        output.append(int(lines[i][:-1]))
        
    return output

def run_anneal(trial_name, iterations, verbose = True, c1 = 0, c2 = 0, c3 = 0):
    # Benchmark from greedy
    tasks = read_input_file(DIRECTORY + "inputs/" + trial_name)
    greedy_output = greedy_solve(tasks)
    if verbose:
        print("greedy value: ", compute_total(tasks, greedy_output))
    
    # Initial naive solve
    # output = initial_solve(tasks)
    # output = [x for x in greedy_output]
    output = read_array(DIRECTORY + "all_outputs/random_annealing/" + trial_name[:-3] + ".out")
    best_output = [x for x in output]
    initial_total = compute_total(tasks, output)
    
    value = compute_total(tasks, output)
    initial_value = value
    if verbose:
        print("input" + trial_name + "initial value: ", initial_value)
    previous = None
    toggle = False
    
    for i in range(iterations):
        output = anneal(tasks, output, iterations, toggle, i)
        output_total = compute_total(tasks, output)
        best_output_total = compute_total(tasks, best_output)
        if output_total > best_output_total:
            best_output = output
            output_path = DIRECTORY + "all_outputs/random_annealing/" + trial_name[:-3] + ".out"
            write_output_file(output_path, best_output)
            
            
        if verbose:
            print(i, output_total)
        if previous == output_total:
            toggle = True
        else:
            toggle = False
        previous = output_total

    if verbose:
        t = best_output_total
        print("final value: ", t)
        print("improvement from previous: ", t - initial_total)
    return output

def run_anneal_all(size, iterations = 1250, c1 = 0, c2 = 0, c3 = 0):
    average = 0
    count = 0
    for input_path in os.listdir(DIRECTORY + "inputs/" + size):
        tasks = read_input_file(DIRECTORY + "inputs/" + size + input_path)
        output = run_anneal(size + input_path, iterations)
        value = compute_total(tasks, output)
        print(input_path + ": ", value)
        average += value
        count += 1
        
        output_path = DIRECTORY + "outputs/" + size + input_path[:-3] + '.out'
        write_output_file(output_path, output)
    return average/count

# RUNNING THE SOLVER

size = "small"

i = 185
while True:
    while i <= 300:
        run_anneal(size + "/" + size + "-" + str(i) + ".in", 1000)
        i += 1

# run_anneal(size + "/" + size + "-" + str(4) + ".in", 100)

# run_anneal_all("small/")
        
