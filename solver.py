from parse import read_input_file, write_output_file
import os
import itertools
import math
import pickle as pkl
import random
import time

def preprocess_into_intervals(tasks, num_intervals, less_than = lambda task1, task2: task1.get_deadline() < task2.get_deadline()):
    """[summary]
    Sorts all tasks into intervals based on deadline of task
    Args:
        tasks ([type]): [description]
        num_intervals ([type]): [description]
    """
    interval_length = 1440 / num_intervals
    I = [[] for _ in range(num_intervals)]
    for task in tasks:
        index = min(math.floor(task.get_deadline() / interval_length), num_intervals - 1)
        #print(task.get_deadline(), index)
        I[index].append(task)
    return I  

def brute_force_solve(tasks):
    """
    Args:
        tasks: list[Task], list of igloos to polish
    Returns:
        output: list of igloos in order of polishing  
    """
    n = len(tasks)
    permutations = list(itertools.permutations([i+1 for i in range(n)]))
    
    best = 0
    best_perm = []
    for p in permutations:
        current = compute_total(tasks, p)
        if current > best:
            best_perm = p
            best = current
    return best_perm

def greedy_solve(tasks, c1, c2, c3):
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

def greedy_solve_intervals(I, num_intervals, c1, c2, c3):
    time = 0
    interval_length = 1440 / num_intervals
    best_task = None
    best_weight = 0
    time_index = 0
    answer = []
    while time <= 1440 and time_index < num_intervals:
        while time <= (time_index + 1) * interval_length:
            best_weight = -1
            best_task = None
            print("time index is ", time_index)
            print([task.get_task_id() for task in I[time_index]])
            for task in I[time_index]:
                current_weight = task.calculate_weight_1(time)
                if best_weight < current_weight:
                    best_weight = current_weight
                    best_task = task
            time += best_task.get_duration()
            if time > 1440:
                return answer
            answer.append(best_task.get_task_id())
            #print(best_task.get_task_id()) 
            I[time_index].remove(best_task)
        time_index += 1
        if (time_index < num_intervals):
            I[time_index] += I[time_index - 1]
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
        
def annealing(tasks, solution):
    num_tasks = len(tasks)
    is_used = [False for _ in range(num_tasks)]
    for index in solution:
        is_used[index - 1] = True
    is_used_original = [b for b in is_used]
        
    # give a random annealing instance  
    new_solution = solution
    is_used = [b for b in is_used_original]
    random_task_index = random.randint(0, len(solution) - 1)
    random_swap_index = random.randint(0, len(is_used) - 1)
    while (is_used[random_swap_index]):
        random_swap_index = random.randint(0, len(is_used) - 1)
        
    new_solution[random_task_index] = random_swap_index + 1 # making the swap
    is_used[random_swap_index] = True
    is_used[random_task_index] = False
    while(calculate_duration(tasks, new_solution) > 1440):
        if (random_task_index < len(new_solution) - 2):
            new_solution.pop(random_task_index + 1)
            is_used[random_task_index + 1] = False
        elif (random_task_index > 0):
            new_solution.pop(random_task_index - 1)
            is_used[random_task_index - 1] = False
            
    current_duration = calculate_duration(tasks, new_solution)
    # current_index = 0
    # for i in range(is_used):
    #     if is_used[i] == 0:
    #         if current_duration + tasks[i].get_duration() <= 1440:
    #             if current_value + tasks[i].hypothetical_gain(current_duration):
    #                 current_value = compute_total(tasks, new_solution) + tasks[i].hypothetical_gain(current_duration)
    
    while current_duration <= 1440 and not all(is_used):
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
        new_solution.append(max_index + 1)
        is_used[max_index] = True
                                    
    return new_solution
           
def anneal(tasks, solution, randomness = 0):
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
            while current_duration <= 1440 and not all(is_used):
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
            
            # Return this new solution if it is better
            if compute_total(tasks, solution_new) > value_original:
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
        
    for i in range(len(solution_swap)):
        for j in range(i, len(solution_swap)):
            solution_swap = [x for x in solution_swap_original]
            temp = solution_swap[i]
            solution_swap[i] = solution_swap[j]
            solution_swap[j] = temp
            if compute_total(tasks, solution_swap) > value_original:
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

def run_all_trials(in_directory, number_inputs, c1 = 0, c2 = 0, c3 = 0):
    count = 0
    average = 0         
    answers = []                                                                                                                        
    for input_path in os.listdir(in_directory + number_inputs):
        tasks = read_input_file(in_directory + number_inputs + input_path)
        # output = greedy_solve_intervals(preprocess_into_intervals(tasks, 1), 1, c1, c2, c3)
        output = greedy_solve(tasks, c1, c2, c3)
        value = compute_total(tasks, output)
        
        output.append(value)
        answers.append(output)
        # print(input_path)
        # print(output)
        
        average += value
        count += 1
        # output_path = "C:/CS170_Final/outputs/large/" + input_path[:-3] + '.out'
        # write_output_file(output_path, output)
        # print("Average is", average/count, "for ", number_inputs)
        
    with open('array_outputs/calculate_weight_2_large.pkl', 'wb') as f:
        pkl.dump(answers, f)
    
    return average/count
     
def run_trial(trial_name, c1 = 0, c2 = 0, c3 = 0):
    tasks = read_input_file("C:/CS170_Final/inputs/small/" + trial_name)
    # I = preprocess_into_intervals(tasks, 10)
    # size = 0
    # print(I)
    # for L in I:
    #     size += size(L)
    # print(size)
    # output = greedy_solve_intervals(I ,10 , c1, c2, c3)
    # output = greedy_solve(tasks, c1, c2, c3)
    
    # output = greedy_solve(tasks, c1, c2, c3)
    print("greedy solve: ", compute_total(tasks, greedy_solve(tasks, c1, c2, c3)))
    output = initial_solve(tasks)
    output_original = [x for x in output]
    value = compute_total(tasks, output)
    initial_value = value
    print("initial value: ", initial_value)
    new_value = 0
    for _ in range(120):
        output = annealing(tasks, output)
        new_value = compute_total(tasks, output)
        while value >= new_value:
            output = annealing(tasks, [x for x in output_original])
            new_value = compute_total(tasks, output)
            # print(new_value, output == output_original)
        value = new_value
        output_original = [x for x in output]
        # print(value)
    print("final value: ", compute_total(tasks, output))
    print("improvement from greedy: ", compute_total(tasks, output) - compute_total(tasks, greedy_solve(tasks, c1, c2, c3)))
    return output
    
    # output = greedy_solve(tasks, c1, c2, c3)
    # value = compute_total(tasks, output)
    # print(value)
    # for i in range(1):
    #     output = annealing(tasks, output)
    # return compute_total(tasks, output)    
    
def run_anneal(trial_name, iterations, verbose = False, c1 = 0, c2 = 0, c3 = 0):
    # Benchmark from greedy
    tasks = read_input_file("C:/CS170_Final/inputs/" + trial_name)
    greedy_output = greedy_solve(tasks, c1, c2, c3)
    if verbose:
        print("greedy value: ", compute_total(tasks, greedy_output))
    
    # Initial naive solve
    # output = initial_solve(tasks)
    output = [x for x in greedy_output]
    value = compute_total(tasks, output)
    initial_value = value
    if verbose:
        print("initial value: ", initial_value)
    
    previous = None
    for i in range(iterations):
        output = anneal(tasks, output)
        check_solution(output, trial_name)
        if verbose:
            print(compute_total(tasks, output))
        if previous == compute_total(tasks, output):
            break
        previous = compute_total(tasks, output)
    
    if verbose:
        print("final value: ", compute_total(tasks, output))
        print("improvement from greedy: ", compute_total(tasks, output) - compute_total(tasks, greedy_output))
        
    output_path = "C:/CS170_Final/outputs/" + trial_name[:-3] + '.out'
    write_output_file(output_path, output)
    
    return output

def check_solution(output, trial_name = ""):
    for i in range(len(output)):
        for j in range(i + 1, len(output)):
            if output[i] == output[j]:
                # print("duplicate output", output[i], trial_name)
                # print(output)
                return False
 
def run_anneal_all(size, iterations = 1000, c1 = 0, c2 = 0, c3 = 0):
    average = 0
    count = 1
    for input_path in os.listdir("C:/CS170_Final/inputs/" + size):
        if int(input_path[6:][:-3]) in range(3, 10) or int(input_path[6:][:-3]) in range(25, 100) or int(input_path[6:][:-3]) in range(244, 301):
            tasks = read_input_file("C:/CS170_Final/inputs/" + size + input_path)
            
            # best = 0
            # best_output = []
            # for i in range(1):         
            #     current =  run_anneal(size + input_path, iterations)   
            #     print(compute_total(tasks, current))          
            #     if compute_total(tasks, current) > best:
            #         best = compute_total(tasks, current)
            #         best_output = current
            # output = best_output
            
            output = run_anneal(size + input_path, iterations)
            while check_solution(output) == False:
                output = run_anneal(size + input_path, iterations)
            
            value = compute_total(tasks, output)
            print(input_path + ": ", value)
            average += value
            count += 1
            
            output_path = "C:/CS170_Final/outputs/" + size + input_path[:-3] + '.out'
            write_output_file(output_path, output)
    return average/count


# RUNNING THE SOLVER
directory = "C:/CS170_Final/inputs/"
input_100 = "small/"
input_150 = "medium/"
input_200 = "large/"

# average = [0, 0, 0, 0]
# best = 0
# bound = 10
# for i in range(15, 1, -1):
#     for j in range(1, bound):
#         for k in range(1, bound):
#             current = run_500_trials(directory, input_100, i, j, k)
#             print(current, i, j, k)
#             if current > best:
#                 best = current 
#                 average[0] = best
#                 average[1] = i
#                 average[2] = j
#                 average[3] = k
# print(average)

# best = 0
# for i in range(10):         
#     current =  run_anneal("large/large-1.in", 150)   
#     print(current)          
#     if current > best:
#         best = current
# print("best is: ", best)

run_anneal("medium/medium-174.in", 1000, True)

# size = "large/"
# print("running ", size)
# run_anneal_all(size)
        
# print(run_all_trials(directory, input_100))
# print(run_all_trials(directory, input_150))
# print(run_all_trials(directory, input_200))
