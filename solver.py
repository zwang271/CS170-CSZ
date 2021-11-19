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
    used = [False for i in range(num_tasks)]
    answer = []
    while time <= 1440 and not all(used):
        max_weight = 0
        for task in tasks:
            if not used[task.get_task_id() - 1]:
                current_weight = task.get_late_benefit(time + task.get_duration() - task.get_deadline())/task.get_duration()
                if max_weight < current_weight:
                    max_weight = current_weight 
                    max_index = task.get_task_id() - 1 #smol egg
        time += tasks[max_index].get_duration()
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

# Here's an example of how to run your solver.
in_directory = "C:/CS170_Final/inputs/"
for input_path in os.listdir(in_directory):
    output_path = 'outputs/' + input_path[:-3] + '.out'
    tasks = read_input_file(in_directory+input_path)
    output = brute_force_solve(tasks)
    print(output)
    write_output_file(output_path, output)
    
