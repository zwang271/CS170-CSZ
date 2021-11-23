from parse import read_input_file, write_output_file
import os
import itertools

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
    used = [False for i in range(num_tasks)]
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


def compute_total(all_tasks, tasks_list):
        total = 0
        time = 0
        for task_id in tasks_list:
            time += all_tasks[task_id-1].get_duration()
            assert time <= 1440, "Can't schedule task beyond 1440 minutes."
            total += all_tasks[task_id-1].get_late_benefit(time - all_tasks[task_id-1].get_deadline())  
        return total

def run_500_trials(in_directory, number_inputs, c1 = 0, c2 = 0, c3 = 0):
    count = 0
    average = 0
    for input_path in os.listdir(in_directory + number_inputs):
        output_path = 'outputs/' + input_path[:-3] + '.out'
        tasks = read_input_file(in_directory + number_inputs + input_path)
        output = greedy_solve(tasks, c1, c2, c3)
        value = compute_total(tasks, output)
        average += value
        count += 1
        #write_output_file(output_path, output)
    #print("Average is", average/count, "for ", number_inputs)
    return average/count

# Here's an example of how to run your solver.
directory = "C:/CS170_Final/inputs/"
input_100 = "100-Inputs/"
input_150 = "150-Inputs/"
input_200 = "200-Inputs/"

# average = [0, 0, 0, 0]
# best = 0
# bound = 4
# for i in range(1, 15):
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
                       
print(run_500_trials(directory, input_100))
print(run_500_trials(directory, input_150))
print(run_500_trials(directory, input_200))