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
    
    value = compute_total(tasks, solution)
    
    improved = False
    
    j = 0
    # MAX_ITERATIONS = math.inf
    MAX_ITERATIONS = 1
    while(not improved and j < MAX_ITERATIONS):
        # print(is_used)
        
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
                                    
        if (compute_total(tasks, new_solution) > value):
            improved = True
        j += 1
    
    return new_solution
                
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

def run_sample_trial(c1 = 0, c2 = 0, c3 = 0):
    tasks = read_input_file("C:/CS170_Final/inputs/small/small-3.in")
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
    print(value)
    new_value = 0
    for _ in range(110):
        output = annealing(tasks, output)
        new_value = compute_total(tasks, output)
        while value >= new_value:
            output = annealing(tasks, [x for x in output_original])
            new_value = compute_total(tasks, output)
            # print(new_value, output == output_original)
        value = new_value
        output_original = [x for x in output]
        # print(value)
    return compute_total(tasks, output)
    
    # output = greedy_solve(tasks, c1, c2, c3)
    # value = compute_total(tasks, output)
    # print(value)
    # for i in range(1):
    #     output = annealing(tasks, output)
    # return compute_total(tasks, output)    
    
# Here's an example of how to run your solver.
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
                       
print(run_sample_trial())
# print(run_all_trials(directory, input_100))
# print(run_all_trials(directory, input_150))
# print(run_all_trials(directory, input_200))
