from parse import read_input_file, write_output_file
import os
import itertools
import math
import pickle as pkl

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
        max_weight = 0
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
        
        average += value
        count += 1
        # output_path = "C:/CS170_Final/outputs/large/" + input_path[:-3] + '.out'
        # write_output_file(output_path, output)
        # print("Average is", average/count, "for ", number_inputs)
        
    with open('array_outputs/calculate_weight_2_large.pkl', 'wb') as f:
        pkl.dump(answers, f)
    
    return average/count

def run_sample_trial(c1 = 0, c2 = 0, c3 = 0):
    tasks = read_input_file("C:/CS170_Final/all_inputs/sample.in")
    I = preprocess_into_intervals(tasks, 10)
    size = 0
    print(I)
    # for L in I:
    #     size += size(L)
    # print(size)
    #output = greedy_solve_intervals(I ,10 , c1, c2, c3)
    output = greedy_solve(tasks, c1, c2, c3)
    return compute_total(tasks, output)

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
                       
# print(run_sample_trial())
# print(run_all_trials(directory, input_100))
# print(run_all_trials(directory, input_150))
print(run_all_trials(directory, input_200))
