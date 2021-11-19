import os
import random
cwd = os.path.abspath(os.getcwd())

TOTAL_MINUTES = 1440
MAX_DURATION = 60
MAX_PROFIT = 100 #exclusively

def create_file(num_tasks):
    path = cwd + "/inputs/" + str(num_tasks) + "-Inputs"
    if not os.path.isdir(path):
        os.mkdir(path)

    file_counter = len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
    file_name = str(num_tasks) + "_" + str(file_counter + 1) + ".in"
    file_path = path + "/" + file_name
    generate_content(file_path, num_tasks)


def generate_content(file_path, num_tasks):
    # each task has a format of : (int)taskId (int)taskDeadline (int)taskDuration (float)taskProfit
    f = open(file_path, "w")

    #first line indicates how many tasks there is
    f.write("%d" % (num_tasks))

    for taskId in range(1, num_tasks + 1):
        f.write("\n")
        taskDeadline = random.randint(1, TOTAL_MINUTES)
        taskDuration = random.randint(1, MAX_DURATION)
        taskProfit = random.random() * MAX_PROFIT
        f.write("%d %d %d %.3f" % (taskId, taskDeadline, taskDuration, taskProfit))

    f.close()

#create_file(200)